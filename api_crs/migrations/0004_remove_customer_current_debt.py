# Generated by Django 5.0 on 2023-12-14 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_crs', '0003_alter_customer_approved_limit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='current_debt',
        ),
    ]