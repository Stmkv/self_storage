from django.contrib import admin

from storage.models import Warehouse, Box, WarehouseImage


class WarehouseImageInline(admin.TabularInline):
    model = WarehouseImage
    extra = 1


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'number_of_boxes', 'creation_date')
    search_fields = ('address',)
    list_filter = ('creation_date',)
    ordering = ('-creation_date',)
    inlines = [WarehouseImageInline]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('number', 'box_type', 'status', 'price_per_month', 'warehouse')
    list_filter = ('status', 'box_type', 'warehouse')
    search_fields = ('number',)
    ordering = ('number',)
    readonly_fields = ('number',)