from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from crm.telegram_notifications import bot


@receiver(post_save)
def update_order(sender, instance, **kwargs):
    print(User.objects.all().first())
    print("Request finished!")