# Generated by Django 3.2.5 on 2021-07-24 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_orders_order_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_telling',
            field=models.CharField(blank=True, max_length=511),
        ),
    ]