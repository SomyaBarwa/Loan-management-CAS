# Generated by Django 5.0 on 2023-12-14 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_crs', '0002_alter_customer_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='approved_limit',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
