from django.db import models
from django.utils import timezone


class RequestCalculation(models.Model):
    email = models.EmailField()
    create_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return self.email
