# Generated by Django 5.1.6 on 2025-02-28 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spapi_credential',
            name='access_token',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='spapi_credential',
            name='access_token_updation_time',
            field=models.DateTimeField(default=None),
        ),
    ]
