# Generated by Django 5.0.6 on 2024-06-30 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_alter_purchaseorder_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='quantity',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
