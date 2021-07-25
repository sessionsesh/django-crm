from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print(User.objects.all().first())
    print("Request finished!")