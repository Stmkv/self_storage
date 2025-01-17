from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("storage.urls", namespace="storage")),
    path('admin/', admin.site.urls),
]
