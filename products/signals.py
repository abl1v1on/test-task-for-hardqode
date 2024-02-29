from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Lesson
from .tasks import send_mail_about_new_lessons


@receiver(post_save, sender=Lesson)
def send_mail(sender, instance, created, **kwargs):
    send_mail_about_new_lessons.delay()
