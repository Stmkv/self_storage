from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

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
