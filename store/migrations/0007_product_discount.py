# Generated by Django 3.2.8 on 2021-10-19 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20211019_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Product Discount in %'),
            preserve_default=False,
        ),
    ]