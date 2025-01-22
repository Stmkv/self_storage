from django.db import models

ORDER_CHOICES = (
    ('todo', 'принять в работу'),
    ('true', 'подтвержден'),
    ('topay', 'выставить счет'),
    ('false', 'отменен'),
)


class Order(models.Model):
    start_storage = models.DateTimeField('начало хранения')
    end_storage = models.DateTimeField('конец хранения')
    client = models.ForeignKey(Client,
                               verbose_name='клиент',
                               on_delete=models.CASCADE,
                               related_name='orders')
    date = models.DateField(auto_now_add=True)
    address = models.TextField('адрес')
    box = models.OneToOneField(Box, on_delete=models.CASCADE, null=True, blank=True)
    price = models.PositiveIntegerField('цена', null=True, blank=True)
    state = models.CharField('состояние', choices=ORDER_CHOICES, max_length=9, default='todo')

    def __str__(self):
        return f'заказ {self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save (self, *args, **kwargs):
        pass

class AboutUs(models.Model):
    title = models.TextField('заголовок')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заголовок'
        verbose_name_plural = 'Заголовки'


class Text(models.Model):
    title = models.ForeignKey(AboutUs,
                             verbose_name='название',
                             on_delete=models.CASCADE,
                             related_name='texts')
    text = models.TextField('текст')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексты'
