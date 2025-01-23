from django.contrib import admin

from .models import RequestCalculation


@admin.register(RequestCalculation)
class RequestCalculationAdmin(admin.ModelAdmin):
    pass
