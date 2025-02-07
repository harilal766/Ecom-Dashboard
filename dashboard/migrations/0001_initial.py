# Generated by Django 5.1.3 on 2025-02-07 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(default='Ecom', max_length=200)),
                ('account_name', models.CharField(default='seller', max_length=400, unique=True)),
                ('total_orders', models.IntegerField(default=0)),
                ('last_schedule', models.DateTimeField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(default='seller', max_length=400, unique=True)),
                ('platform', models.CharField(default='Ecom', max_length=200)),
            ],
        ),
    ]
