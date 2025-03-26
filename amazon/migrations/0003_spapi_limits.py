# Generated by Django 5.1.6 on 2025-03-26 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0002_alter_spapi_credential_access_token_updation_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='SPAPI_Limits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True)),
                ('burst', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
