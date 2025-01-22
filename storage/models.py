from django.db import models

from users.models import CustomUser


class Warehouse(models.Model):
    address = models.CharField(max_length=100, unique=True, verbose_name="Адрес склада")
    temperature = models.IntegerField(verbose_name="Температура на складе")
    celling_height = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Высота потолка")
    total_boxes = models.PositiveIntegerField(default=0, verbose_name="Всего боксов")
    available_boxes = models.PositiveIntegerField(verbose_name="Доступные боксы")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за месяц от")

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return self.name


class Box(models.Model):
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="boxes", verbose_name="Склады"
    )
    number = models.CharField(max_length=99, unique=True, verbose_name="Номер бокса")
    floor = models.IntegerField(verbose_name="Этаж")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Цена"
    )
    release_date = models.DateField(blank=True, null=True, verbose_name="Дата создания")
    size = models.CharField(max_length=50, verbose_name="Размер бокса")
    dimensions = models.CharField(max_length=100, verbose_name="Габариты")
    is_available = models.BooleanField(default=True, verbose_name="Доступность")

    class Meta:
        verbose_name = "Бокс"
        verbose_name_plural = "Боксы"

    def __str__(self):
        return f"{self.warehouse.name} - {self.number}"

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
    box = models.OneToOneField(Box, on_delete=models.CASCADE, null=True, blank=True)
    price = models.PositiveIntegerField("цена", null=True, blank=True)
    state = models.CharField(
        "состояние", choices=ORDER_CHOICES, max_length=9, default="todo"
    )

    def __str__(self):
        return f"заказ {self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def save(self, *args, **kwargs):
        pass


class AboutUs(models.Model):
    title = models.TextField("заголовок")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заголовок"
        verbose_name_plural = "Заголовки"


class Text(models.Model):
    title = models.ForeignKey(
        AboutUs, verbose_name="название", on_delete=models.CASCADE, related_name="texts"
    )
    text = models.TextField("текст")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"
