# Generated by Django 3.0.2 on 2020-02-04 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubcell', '0025_auto_20200204_0507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='event_UAP',
        ),
        migrations.AddField(
            model_name='events',
            name='event_uen',
            field=models.CharField(default=' ', max_length=30, unique=True),
            preserve_default=False,
        ),
    ]