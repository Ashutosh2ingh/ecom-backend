# Generated by Django 5.0.7 on 2024-09-21 15:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_app', '0005_rename_product_variation_cart_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
        migrations.AddField(
            model_name='cart',
            name='product_variation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecom_app.productvariation'),
        ),
    ]
