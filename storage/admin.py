from django.contrib import admin

from storage.models import Warehouse, Box, Order, AboutUs, Text


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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'address', 'box', 'price', 'start_storage', 'end_storage', 'state',)
    search_fields = ('client', 'state',)
    list_filter = ('client', 'state',)


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('title', 'question', 'answer')
    search_fields = ('title',)
    list_filter = ('title',)
