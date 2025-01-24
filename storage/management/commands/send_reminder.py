import datetime
from django.utils import timezone
import smtplib
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from storage.models import Box
from django.db.models import Q
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Sends reminder emails for box storage'

    def handle(self, *args, **options):
        time_now = timezone.now()
        before_2_days = time_now + timedelta(days=2)
        before_4_days = time_now + timedelta(days=4)
        before_13_days = time_now + timedelta(days=13)
        before_15_days = time_now + timedelta(days=15)
        before_20_days = time_now + timedelta(days=20)
        before_22_days = time_now + timedelta(days=22)
        before_29_days = time_now + timedelta(days=29)
        before_31_days = time_now + timedelta(days=31)

        boxes_in_storage = Box.objects.filter(status='занят').prefetch_related('order').filter(
            Q(order__end_storage__gt=before_4_days) & Q(order__end_storage__lt=before_2_days) |
            Q(order__end_storage__gt=before_15_days) & Q(order__end_storage__lt=before_13_days) |
            Q(order__end_storage__gt=before_22_days) & Q(order__end_storage__lt=before_20_days) |
            Q(order__end_storage__gt=before_31_days) & Q(order__end_storage__lt=before_29_days)
        )
        for box in boxes_in_storage:
            try:
                send_mail(
                    # title:
                    'напоминание',
                    # message:
                    f'конец срока хранения {box.get_end_storage().date()}.\n'
                    f'Вы можете забрать вещи сами или заказать доставку.',
                    # from:
                    settings.EMAIL_HOST_USER,
                    # to:
                    [box.order.client.email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f'Reminder sent to {box.order.client.email}'))
            except smtplib.SMTPRecipientsRefused as e:
                self.stdout.write(self.style.ERROR(f'Error sending email:  {e}'))

        before_1_day = time_now + timedelta(days=2)
        after_1_day = time_now + timedelta(days=4)

        pick_up_today = Box.objects.filter(status='занят').prefetch_related('order').filter(
            Q(order__end_storage__gt=before_1_day) & Q(order__end_storage__lt=after_1_day))
        for box in pick_up_today:
            try:
                send_mail(
                    # title:
                    'напоминание',
                    # message:
                    f'Заберите вещи сегодня. Вы можете забрать вещи сами или заказать доставку.\n'
                    f'Если вы не заберете вещи, они будут храниться 6 месяцев, но тариф будет чуть выше.\n'
                    f' После чего вы их потеряете',
                    # from:
                    settings.EMAIL_HOST_USER,
                    # to:
                    [box.order.client.email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f'Reminder sent to {box.order.client.email}'))
            except smtplib.SMTPRecipientsRefused as e:
                self.stdout.write(self.style.ERROR(f'Error sending email:  {e}'))

        after_29_days = time_now - timedelta(days=29)
        after_31_days = time_now - timedelta(days=31)
        after_59_days = time_now - timedelta(days=59)
        after_61_days = time_now - timedelta(days=61)
        after_89_days = time_now - timedelta(days=89)
        after_91_days = time_now - timedelta(days=91)
        after_119_days = time_now - timedelta(days=119)
        after_121_days = time_now - timedelta(days=121)
        after_149_days = time_now - timedelta(days=149)
        after_151_days = time_now - timedelta(days=151)
        after_179_days = time_now - timedelta(days=179)
        after_181_days = time_now - timedelta(days=181)

        expired_boxes = Box.objects.filter(status='занят').prefetch_related('order').filter(
            Q(order__end_storage__gt=after_31_days) & Q(order__end_storage__lt=after_29_days) |
            Q(order__end_storage__gt=after_61_days) & Q(order__end_storage__lt=after_59_days) |
            Q(order__end_storage__gt=after_91_days) & Q(order__end_storage__lt=after_89_days) |
            Q(order__end_storage__gt=after_121_days) & Q(order__end_storage__lt=after_119_days) |
            Q(order__end_storage__gt=after_151_days) & Q(order__end_storage__lt=after_149_days) |
            Q(order__end_storage__gt=after_181_days) & Q(order__end_storage__lt=after_179_days)
        )
        for box in expired_boxes:
            pick_up_time = box.get_end_storage() + timedelta(days=180)
            try:
                send_mail(
                    # title:
                    'напоминание',
                    # message:
                    f'Хранение просрочено. Заберите вещи до {pick_up_time.date()}.\n'
                    f'Вы можете забрать вещи сами или заказать доставку',
                    # from:
                    settings.EMAIL_HOST_USER,
                    # to:
                    [box.order.client.email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f'Reminder sent to {box.order.client.email}'))
            except smtplib.SMTPRecipientsRefused as e:
                self.stdout.write(self.style.ERROR(f'Error sending email:  {e}'))
