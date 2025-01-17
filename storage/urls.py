from django.urls import path

from storage import views

app_name = "storage"
urlpatterns = [
    path("", views.index, name="boxes"),
    path("faq/", views.faq, name="faq"),
    path("boxes/", views.boxes, name="index"),
    path("my-rent/", views.my_rent, name="my-rent"),
    path("my-rent-empty/", views.my_rent_empty, name="my-rent-empty"),
]
