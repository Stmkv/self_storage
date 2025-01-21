from django.db import models

class Warehouse(models.Model):
    address = models.CharField(max_length=100, unique=True)
    total_area = models.FloatField(help_text='Общая площадь ангара в квадратных метрах')
    number_of_boxes = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f'Ангар по адресу {self.address}'

class Box(models.Model):
    TYPES = [
        ('маленький', 'маленький'),
        ('стандартный', 'Стандартный'),
        ('большой', 'Большой'),
    ]

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='boxes')
    number = models.CharField(max_length=99, unique=True)
    box_type = models.CharField(max_length=20, choices=TYPES)
    box_area = models.FloatField(help_text='Общая площадь бокса')
    status = models.CharField(max_length=20,
                              choices=[
                                  ('свободен', 'Свободен'),
                                  ('занят', 'Занят'),
                              ],
                              default='свободен')
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, help_text='Цена в месяц в рублях')
    release_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Бокс #{self.number} ({self.box_type}'

    def save (self, *args, **kwargs):
        if not self.number:
            last_number = Box.objects.filter(warehouse=self.warehouse).count()
            self.number = f'{self.warehouse.id} - {last_number + 1}'
        super(Box, self).save(*args, **kwargs)


class Order(models.Model):
    pass


