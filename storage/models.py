from django.db import models


class Warehouse(models.Model):
    address = models.CharField(max_length=100, unique=True)
    total_area = models.FloatField(help_text="Общая площадь склада в квадратных метрах")
    number_of_boxes = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return f"Склад по адресу {self.address}"


class Box(models.Model):
    TYPES = [
        ("маленький до 3м", "Маленький до 3м"),
        ("стандартный от 3м до 10м", "Стандартный от 3м до 10м"),
        ("большой от 10м", "Большой от 10м"),
    ]

    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="boxes"
    )
    number = models.CharField(max_length=99, unique=True)
    box_type = models.CharField(max_length=30, choices=TYPES)
    status = models.CharField(
        max_length=20,
        choices=[
            ("свободен", "Свободен"),
            ("занят", "Занят"),
        ],
        default="свободен",
    )
    price_per_month = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Цена в месяц в рублях"
    )
    release_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Бокс"
        verbose_name_plural = "Боксы"

    def __str__(self):
        return f"Бокс #{self.number} ({self.box_type}"

    def save(self, *args, **kwargs):
        if not self.number:
            last_number = Box.objects.filter(warehouse=self.warehouse).count()
            self.number = f"{self.warehouse.id} - {last_number + 1}"
        super(Box, self).save(*args, **kwargs)


class Order(models.Model):
    pass
