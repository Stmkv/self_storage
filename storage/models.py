from django.db import models

from users.models import CustomUser


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


ORDER_CHOICES = (
    ("todo", "принять в работу"),
    ("true", "подтвержден"),
    ("topay", "выставить счет"),
    ("false", "отменен"),
)


class Order(models.Model):
    start_storage = models.DateTimeField("начало хранения")
    end_storage = models.DateTimeField("конец хранения")
    client = models.ForeignKey(
        CustomUser,
        verbose_name="клиент",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    date = models.DateField(auto_now_add=True)
    address = models.TextField("адрес")
    box = models.OneToOneField(
        Box,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    price = models.PositiveIntegerField(
        verbose_name="цена",
        null=True,
        blank=True)
    state = models.CharField(
        "состояние",
        choices=ORDER_CHOICES,
        max_length=9,
        default="todo"
    )

    def __str__(self):
        return f"заказ {self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def save(self, *args, **kwargs):
        pass


class AboutUs(models.Model):
    title = models.CharField(
        verbose_name="заголовок",
        max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заголовок"
        verbose_name_plural = "Заголовки"


class Text(models.Model):
    title = models.ForeignKey(
        AboutUs,
        verbose_name="название",
        on_delete=models.CASCADE,
        related_name="texts"
    )
    question = models.CharField(
        verbose_name="вопрос",
        max_length=200)
    answer = models.TextField("ответ")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"
