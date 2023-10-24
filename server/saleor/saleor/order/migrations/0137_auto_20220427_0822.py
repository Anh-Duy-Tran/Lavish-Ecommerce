# Generated by Django 3.2.12 on 2022-04-27 08:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0136_auto_20220414_1025"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderline",
            name="base_unit_price_amount",
            field=models.DecimalField(decimal_places=3, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="orderline",
            name="undiscounted_base_unit_price_amount",
            field=models.DecimalField(decimal_places=3, default=0, max_digits=12),
        ),
    ]
