# Generated by Django 5.0.7 on 2024-10-17 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_app', '0014_payment_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product_variation',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='customer',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
