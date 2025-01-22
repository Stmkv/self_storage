from django.contrib import admin

from storage.models import Warehouse, Box


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('address', 'total_area', 'number_of_boxes', 'creation_date')
    search_fields = ('address', 'description')
    list_filter = ('creation_date',)
    ordering = ('-creation_date',)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('number', 'box_type', 'status', 'price_per_month', 'warehouse')
    list_filter = ('status', 'box_type', 'warehouse')
    search_fields = ('number',)
    ordering = ('number',)
    readonly_fields = ('number',)