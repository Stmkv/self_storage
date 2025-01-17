
from storage import views
from django.urls import path
app_name = "storage"
urlpatterns = [
    path("", views.boxes, name="boxes"),
    path("faq/", views.faq, name="faq"),
    path("index/", views.index, name="index"),
    path("my-rent/", views.my_rent, name="my-rent"),
    path("my-rent-empty/", views.my_rent_empty, name="my-rent-empty"),
]