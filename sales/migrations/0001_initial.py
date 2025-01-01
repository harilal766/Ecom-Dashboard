# Generated by Django 5.1.3 on 2024-12-27 08:21

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
            name='SPAPI_Credential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=500)),
                ('client_secret', models.CharField(max_length=500)),
                ('refresh_token', models.CharField(max_length=500)),
                ('access_token', models.CharField(max_length=500)),
                ('access_token_updation_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
