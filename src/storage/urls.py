from django.urls import path

from storage import views

app_name = "storage"
urlpatterns = [
    path("", views.index, name="index"),
    path("faq/", views.faq, name="faq"),
    path("boxes/", views.boxes, name="boxes"),
    path("my-rent/", views.my_rent, name="my-rent"),
    path("my-rent-empty/", views.my_rent_empty, name="my-rent-empty"),
    path("order/", views.order, name="order"),
    path("agreement/", views.agreement, name="agreement"),
    path("track/<int:link_number>/", views.track_link, name="track_link"),
]
