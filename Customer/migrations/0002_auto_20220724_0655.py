# Generated by Django 3.2.14 on 2022-07-24 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
