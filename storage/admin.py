from django.contrib import admin
from django.db import models
from django.utils.timezone import now
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from storage.models import AboutUs, Box, Link, Order, Text, Warehouse, WarehouseImage


class WarehouseImageInline(admin.TabularInline):
    model = WarehouseImage
    extra = 1


@admin.register(Warehouse)
class WarehouseAdmin(ModelAdmin):
    list_display = ("city", "address", "number_of_boxes", "creation_date")
    search_fields = ("address",)
    list_filter = ("creation_date",)
    ordering = ("-creation_date",)
    inlines = [WarehouseImageInline]


@admin.register(Box)
class BoxAdmin(ModelAdmin):
    list_display = ("number", "area", "status", "price_per_month", "warehouse")
    list_filter = ("status", "area", "warehouse")
    search_fields = ("number",)
    ordering = ("number",)
    readonly_fields = ("number",)


@admin.register(AboutUs)
class AboutUsAdmin(ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Text)
class TextAdmin(ModelAdmin):
    list_display = ("title", "question", "answer")
    search_fields = ("title",)
    list_filter = ("title",)

    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }


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
class OrderAdmin(ModelAdmin):
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


@admin.register(Link)
class LinkAdmin(ModelAdmin):
    list_display = ("link_number", "shortened_url", "click_count")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
