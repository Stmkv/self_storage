from django.contrib import admin
from unfold.admin import ModelAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    pass
