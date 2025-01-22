from django.urls import path

from .views import login_view, my_rent_view, register_view

app_name = "users"
urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("my-rent/", my_rent_view, name="my-rent"),
]
