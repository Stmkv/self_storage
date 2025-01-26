from django.contrib import admin
from django.utils.timezone import now

from storage.models import AboutUs, Box, Order, Text, Warehouse, WarehouseImage


class WarehouseImageInline(admin.TabularInline):
    model = WarehouseImage
    extra = 1


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("city", "address", "number_of_boxes", "creation_date")
    search_fields = ("address",)
    list_filter = ("creation_date",)
    ordering = ("-creation_date",)
    inlines = [WarehouseImageInline]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ("number", "area", "status", "price_per_month", "warehouse")
    list_filter = ("status", "area", "warehouse")
    search_fields = ("number",)
    ordering = ("number",)
    readonly_fields = ("number",)


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ("title", "question", "answer")
    search_fields = ("title",)
    list_filter = ("title",)


class ExpiredOrdersFilter(admin.SimpleListFilter):
    title = "Просроченные заказы"
    parameter_name = "expired"

    def lookups(self, request, model_admin):
        return [
            ("yes", "Просроченные"),
            ("no", "Не просроченные"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(end_storage__lt=now())
        if self.value() == "no":
            return queryset.filter(end_storage__gte=now())
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "address",
        "box",
        "price",
        "start_storage",
        "end_storage",
        "state",
    )
    search_fields = (
        "client",
        "state",
    )
    list_filter = (
        ExpiredOrdersFilter,
        "client",
        "state",
    )
