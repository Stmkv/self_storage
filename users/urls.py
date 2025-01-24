from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    confirm_order_inactive,
    edit_profile,
    login_view,
    logout_view,
    my_rent_view,
    password_reset,
    register_view,
    send_qr_code,
    upload_avatar,
)

app_name = "users"
urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("my-rent/", my_rent_view, name="my-rent"),
    path("logout/", logout_view, name="logout"),
    path("edit-profile/", edit_profile, name="edit-profile"),
    path("password_reset/", password_reset, name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path("upload_avatar/", upload_avatar, name="upload-avatar"),
    path("orders/<int:order_id>/send-qr/", send_qr_code, name="send_qr_code"),
    path(
        "orders/<int:order_id>/confirm/",
        confirm_order_inactive,
        name="confirm_order_inactive",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
