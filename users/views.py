from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from .forms import UserLoginForm, UserRegisterForm


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
        form = UserLoginForm(request.POST)
        if form.is_valid():
            print("Я тут")
            user = authenticate(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return JsonResponse({"success": True, "redirect_url": "/my-rent/"})
            else:
                return JsonResponse(
                    {"success": False, "message": "Неверные учетные данные"}, status=400
                )
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
