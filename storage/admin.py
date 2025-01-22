from django.contrib import admin

from storage.models import Warehouse, Box


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('address', 'temperature', 'celling_height', 'total_boxes', 'available_boxes', 'price_per_month', 'creation_date')
    list_filter = ('temperature', 'celling_height', 'creation_date')
    search_fields = ('address',)
    ordering = ('-creation_date',)

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'number', 'floor', 'price', 'size', 'dimensions', 'is_available', 'release_date')
    list_filter = ('warehouse', 'floor', 'is_available', 'release_date')
    search_fields = ('number', 'warehouse__address')
    ordering = ('warehouse', 'number')