# Generated by Django 5.0.7 on 2024-10-12 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_app', '0009_order_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='customer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
