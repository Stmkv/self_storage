from django.db import models

from self_storage.settings import BASE_URL
from users.models import CustomUser


class Warehouse(models.Model):
    city = models.CharField(max_length=20, verbose_name="Город")
    address = models.CharField(max_length=100, unique=True, verbose_name="Адрес")
    number_of_boxes = models.PositiveIntegerField(
        default=0, verbose_name="Всего боксов"
    )
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    price_per_month = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за месяц от"
    )
    preview_image = models.ImageField(
        upload_to="warehouse_preview_images/", verbose_name="Изображение"
    )
    description = models.CharField(
        max_length=200, verbose_name="Описание (например Рядом с метро)"
    )
    temperature = models.IntegerField(verbose_name="Температура")
    ceiling_height = models.PositiveIntegerField(verbose_name="Высота потолка")
    full_description = models.TextField(verbose_name="Полное описание")

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return f"Склад по адресу {self.address}"


class WarehouseImage(models.Model):
    warehouse = models.ForeignKey(
        Warehouse, related_name="images", on_delete=models.CASCADE
    )
    full_image = models.ImageField(
        upload_to="warehouse_full_images/", verbose_name="Полное изображение"
    )

    def __str__(self):
        return f"Изображение для {self.warehouse.address}"


class Box(models.Model):
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="boxes", verbose_name="Склад"
    )
    floor = models.CharField(max_length=1, verbose_name="Этаж")
    area = models.FloatField(verbose_name="Площадь (м²)", editable=False)
    length = models.FloatField(verbose_name="Длина (м)")
    width = models.FloatField(verbose_name="Ширина (м)")
    height = models.FloatField(verbose_name="Высота (м)")
    number = models.CharField(max_length=99, unique=True, verbose_name="Номер бокса")
    status = models.CharField(
        max_length=20,
        choices=[
            ("свободен", "Свободен"),
            ("занят", "Занят"),
            ("в обработке", "В обработке"),
        ],
        default="свободен",
        verbose_name="Статус",
    )
    price_per_month = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Цена в месяц в рублях",
        verbose_name="Цена за месяц",
    )
    release_date = models.DateField(blank=True, null=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Бокс"
        verbose_name_plural = "Боксы"

    def __str__(self):
        return f"Бокс #{self.number} ({self.area} м²)"

    def save(self, *args, **kwargs):
        self.area = self.length * self.width
        if not self.pk:
            last_number = Box.objects.filter(warehouse=self.warehouse).count()
            self.number = f"{self.warehouse.id} - {last_number + 1}"

        super().save(*args, **kwargs)


ORDER_CHOICES = (
    ("todo", "принять в работу"),
    ("true", "подтвержден"),
    ("topay", "выставить счет"),
    ("false", "отменен"),
    ("inactive", "неактивен"),
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
    address = models.TextField("адрес", null=True, blank=True)
    box = models.ForeignKey(
        Box, on_delete=models.CASCADE, null=True, blank=True, related_name="order"
    )
    price = models.PositiveIntegerField("цена", null=True, blank=True)
    state = models.CharField(
        "состояние", choices=ORDER_CHOICES, max_length=9, default="todo"
    )

    def __str__(self):
        return f"заказ {self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class AboutUs(models.Model):
    title = models.CharField(verbose_name="заголовок", max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заголовок"
        verbose_name_plural = "Заголовки"


class Text(models.Model):
    title = models.ForeignKey(
        AboutUs, verbose_name="название", on_delete=models.CASCADE, related_name="texts"
    )
    question = models.CharField(verbose_name="вопрос", max_length=200)
    answer = models.TextField("ответ")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"


class Link(models.Model):
    original_url = models.URLField()
    click_count = models.PositiveIntegerField(default=0)
    link_number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"{self.link_number} -> {self.original_url}"

    @property
    def shortened_url(self):
        return f"http://{BASE_URL}/track/{self.link_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
