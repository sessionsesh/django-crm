from django.db import models
from accounts.models import User

# Create your models here.


class OrderType(models.Model):
    order_type = models.CharField(max_length=255, blank=True)


class OrderStatus(models.Model):
    order_status = models.CharField(max_length=255, blank=True)


class Order(models.Model):
    customer = models.ForeignKey(
        User, related_name='customer', on_delete=models.DO_NOTHING, null=False, blank=False)

    employee = models.ForeignKey(
        User, related_name='employee', on_delete=models.DO_NOTHING, blank=True, null=True)

    customer_telling = models.CharField(max_length=511, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    order_type = models.ForeignKey(OrderType, on_delete=models.DO_NOTHING)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING)

