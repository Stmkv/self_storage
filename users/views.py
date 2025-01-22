import re
from math import e

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

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
    return render(request, "my-rent.html", {"user": request.user})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse("storage:index"))


@login_required
def edit_profile(request):
    user = CustomUser.objects.get(email=request.user.email)
    new_email = request.POST.get("EMAIL_EDIT")
    try:
        validate_email(new_email)
    except ValidationError:
        return JsonResponse(
            {
                "success": False,
                "errors": {"email": ["Неверный формат"]},
            },
            status=400,
        )
    else:
        user.email = request.POST.get("EMAIL_EDIT")
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
