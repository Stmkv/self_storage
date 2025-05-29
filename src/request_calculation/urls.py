from django.urls import path

from .views import get_request_email

app_name = "request_calculation"

urlpatterns = [
    path("get_request/", get_request_email, name="get_request"),
]
