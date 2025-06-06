# Generated by Django 5.1.5 on 2025-01-24 21:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AboutUs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="заголовок")),
            ],
            options={
                "verbose_name": "Заголовок",
                "verbose_name_plural": "Заголовки",
            },
        ),
        migrations.CreateModel(
            name="Box",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("floor", models.CharField(max_length=1, verbose_name="Этаж")),
                (
                    "area",
                    models.FloatField(editable=False, verbose_name="Площадь (м²)"),
                ),
                ("length", models.FloatField(verbose_name="Длина (м)")),
                ("width", models.FloatField(verbose_name="Ширина (м)")),
                ("height", models.FloatField(verbose_name="Высота (м)")),
                (
                    "number",
                    models.CharField(
                        max_length=99, unique=True, verbose_name="Номер бокса"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("свободен", "Свободен"),
                            ("занят", "Занят"),
                            ("в обработке", "В обработке"),
                        ],
                        default="свободен",
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "price_per_month",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Цена в месяц в рублях",
                        max_digits=10,
                        verbose_name="Цена за месяц",
                    ),
                ),
                (
                    "release_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Дата создания"
                    ),
                ),
            ],
            options={
                "verbose_name": "Бокс",
                "verbose_name_plural": "Боксы",
            },
        ),
        migrations.CreateModel(
            name="Text",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.CharField(max_length=200, verbose_name="вопрос")),
                ("answer", models.TextField(verbose_name="ответ")),
            ],
            options={
                "verbose_name": "Текст",
                "verbose_name_plural": "Тексты",
            },
        ),
        migrations.CreateModel(
            name="Warehouse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(max_length=20, verbose_name="Город")),
                (
                    "address",
                    models.CharField(max_length=100, unique=True, verbose_name="Адрес"),
                ),
                (
                    "number_of_boxes",
                    models.PositiveIntegerField(default=0, verbose_name="Всего боксов"),
                ),
                (
                    "creation_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "price_per_month",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Цена за месяц от"
                    ),
                ),
                (
                    "preview_image",
                    models.ImageField(
                        upload_to="warehouse_preview_images/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=200, verbose_name="Описание (например Рядом с метро)"
                    ),
                ),
                ("temperature", models.IntegerField(verbose_name="Температура")),
                (
                    "ceiling_height",
                    models.PositiveIntegerField(verbose_name="Высота потолка"),
                ),
                ("full_description", models.TextField(verbose_name="Полное описание")),
            ],
            options={
                "verbose_name": "Склад",
                "verbose_name_plural": "Склады",
            },
        ),
        migrations.CreateModel(
            name="WarehouseImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "full_image",
                    models.ImageField(
                        upload_to="warehouse_full_images/",
                        verbose_name="Полное изображение",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_storage", models.DateTimeField(verbose_name="начало хранения")),
                ("end_storage", models.DateTimeField(verbose_name="конец хранения")),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "address",
                    models.TextField(blank=True, null=True, verbose_name="адрес"),
                ),
                (
                    "price",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="цена"
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("todo", "принять в работу"),
                            ("true", "подтвержден"),
                            ("topay", "выставить счет"),
                            ("false", "отменен"),
                            ("inactive", "неактивен"),
                        ],
                        default="todo",
                        max_length=9,
                        verbose_name="состояние",
                    ),
                ),
                (
                    "box",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order",
                        to="storage.box",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
            },
        ),
    ]
