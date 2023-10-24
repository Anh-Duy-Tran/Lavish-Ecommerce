from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("product", "0002_auto_20150722_0545")]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(verbose_name="description"),
        )
    ]
