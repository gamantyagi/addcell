# Generated by Django 3.0.2 on 2020-02-11 04:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clubcell', '0038_auto_20200210_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='typing_message',
            name='last_type',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]