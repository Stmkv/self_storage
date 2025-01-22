from django.shortcuts import render
from storage.models import AboutUs


# Create your views here.
def boxes(request):
    context = {
        "user_auth": request.user.is_authenticated,
    }
    return render(request, "boxes.html", context)


def faq(request):
    about_us_data = AboutUs.objects.all()
    context = {
        "user_auth": request.user.is_authenticated,
        "about_us_data": about_us_data
    }
    return render(request, "faq.html", context)


def index(request):
    context = {
        "user_auth": request.user.is_authenticated,
    }
    if request.user.is_authenticated:
        context["user"] = request.user
    return render(request, "index.html", context)


def my_rent(request):
    return render(request, "my-rent.html")


def my_rent_empty(request):
    return render(request, "my-rent-empty.html")
