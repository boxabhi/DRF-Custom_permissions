# Generated by Django 4.2.8 on 2024-12-18 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_fileuploader'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date_of_sale',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_sale_value',
        ),
    ]
