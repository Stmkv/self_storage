from django.urls import path

from .views import login_view, register_view

app_name = "users"
urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
]
