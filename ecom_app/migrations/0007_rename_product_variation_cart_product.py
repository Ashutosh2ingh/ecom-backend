# Generated by Django 5.0.7 on 2024-09-21 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_app', '0006_remove_cart_product_cart_product_variation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product_variation',
            new_name='product',
        ),
    ]
