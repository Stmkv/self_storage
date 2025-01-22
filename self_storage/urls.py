from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("storage.urls", namespace="storage")),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("users/", include("django.contrib.auth.urls")),
]
if settings.DEBUG:
    urlpatterns = [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
