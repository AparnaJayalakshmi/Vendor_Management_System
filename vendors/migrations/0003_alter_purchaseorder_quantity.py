# Generated by Django 5.0.6 on 2024-06-30 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_purchaseorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='quantity',
            field=models.IntegerField(blank=True),
        ),
    ]
