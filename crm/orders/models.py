from django.db import models

# Create your models here.


class OrderType(models.Model):
    order_type = models.CharField(max_length=255, blank=True)


class OrderStatus(models.Model):
    order_status = models.CharField(max_length=255, blank=True)


class Order(models.Model):
    request_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now=True)
    orders = models.ManyToManyField(OrderType)
    statuses = models.ManyToManyField(OrderStatus)
