# Generated by Django 3.2.8 on 2021-10-20 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_alter_vendor_business_name'),
        ('store', '0014_alter_product_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='store_product_related', to='vendor.vendor'),
            preserve_default=False,
        ),
    ]
