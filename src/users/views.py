from io import BytesIO

import phonenumbers
import qrcode
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail
from django.core.validators import validate_email
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from phonenumber_field.phonenumber import PhoneNumber

from self_storage.settings import VPS_ADDRESS
from storage.models import Order
from users.models import CustomUser

from .forms import UserRegisterForm


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({"success": True, "redirect_url": "/my-rent/"})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    return JsonResponse(
        {"success": False, "message": "Invalid request method"}, status=405
    )


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Пользователь с таким Email не найден"},
                status=405,
            )

        user = authenticate(request, email=user.email, password=password)
        if user:
            login(request, user)
            return JsonResponse({"success": True, "redirect_url": "/my-rent/"})
        else:
            return JsonResponse(
                {"success": False, "message": "Неверные учетные данные"},
                status=405,
            )


@login_required
def my_rent_view(request):
    user = CustomUser.objects.get(email=request.user.email)
    user_orders = (
        Order.objects.filter(client=user)
        .exclude(state="inactive")
        .select_related("box", "box__warehouse")
    )

    orders_data = []
    for order in user_orders:
        time_left = (order.end_storage - now()).days
        if order.box:
            orders_data.append(
                {
                    "warehouse_address": order.box.warehouse.address,
                    "box_number": order.box.number,
                    "rental_period": f"{order.start_storage.strftime('%d.%m.%Y')} - {order.end_storage.strftime('%d.%m.%Y')}",
                    "time_left": time_left,
                    "order_id": order.id,
                }
            )

    return render(
        request, "my-rent.html", {"user": request.user, "orders": orders_data}
    )


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse("storage:index"))


@login_required
@require_POST
def upload_avatar(request):
    user = CustomUser.objects.get(email=request.user.email)
    if request.FILES.get("avatar"):
        avatar = request.FILES["avatar"]
        user.avatar = avatar
        user.save()
        return JsonResponse({"success": True, "redirect_url": "/users/my-rent/"})

    return JsonResponse({"success": False, "errors": {"avatar": ["Файл не выбран"]}})


@login_required
def edit_profile(request):
    user = CustomUser.objects.get(email=request.user.email)

    new_email = request.POST.get("EMAIL_EDIT")
    new_phone_number = request.POST.get("PHONE_EDIT")

    try:
        validate_email(new_email)
    except ValidationError:
        return JsonResponse(
            {"success": False, "errors": {"email": ["Неверный формат"]}},
            status=400,
        )
    try:
        phone_number_obj = PhoneNumber.from_string(new_phone_number, region="RU")
        if not phonenumbers.is_valid_number(phone_number_obj):
            raise ValidationError("Неверный номер телефона")
    except (phonenumbers.phonenumberutil.NumberParseException, ValidationError):
        return JsonResponse(
            {"success": False, "errors": {"phone": ["Неверный формат телефона"]}},
            status=400,
        )

    user.email = new_email
    user.phone_number = phone_number_obj
    user.save()

    return JsonResponse({"success": True, "redirect_url": "/my-rent/"})


def password_reset(request):
    try:
        if request.method == "POST":
            email = request.POST.get("EMAIL_FORGET")
            user = CustomUser.objects.get(email=email)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            domain = get_current_site(request).domain
            reset_url = f"http://{domain}/users/reset/{uid}/{token}/"

            subject = "Восстановление пароля"
            message = render_to_string(
                "users/password_reset_message.html",
                {
                    "reset_url": reset_url,
                    "user": user,
                },
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=message,
            )
            return JsonResponse(
                {
                    "success": True,
                    "message": "Инструкции для восстановления пароля отправлены на вашу почту.",
                }
            )
    except CustomUser.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "message": "Пользователь с таким email не найден.",
            },
            status=400,
        )


def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


def send_qr_code(request, order_id):
    order = Order.objects.get(id=order_id, client=request.user)
    qr_data = f"http://{VPS_ADDRESS}/users/orders/{order.id}/confirm?user={order.client.email}"
    qr_image = generate_qr_code(qr_data)

    email = EmailMessage(
        subject="QR-код для доступа к боксу",
        body="Используйте QR-код, чтобы открыть ваш бокс. После использования статус заказа станет неактивным.",
        from_email="noreply@example.com",
        to=[order.client.email],
    )
    email.attach("qr_code.png", qr_image.getvalue(), "image/png")
    email.send()

    return JsonResponse({"message": "QR-код отправлен на вашу почту!"})


def confirm_order_inactive(request, order_id):
    try:
        order = Order.objects.get(id=order_id, client=request.user)
        order.state = "inactive"
        order.save()

        box = order.box
        box.status = "свободен"
        box.save()

        order.box = None
        order.save()

        return render(
            request,
            "open_box.html",
            {
                "order": order,
            },
        )
    except Order.DoesNotExist:
        raise Http404("Order not found")


def extend_rental(request, order_id):
    if request.method == "POST":
        new_end_date = request.POST.get("new_end_date")
        print(new_end_date)
        order = get_object_or_404(Order, id=order_id)
        order.end_storage = new_end_date
        order.save()
        return redirect("users:my-rent")
    return HttpResponse("Invalid request", status=400)
