# Generated by Django 3.0.2 on 2020-01-31 08:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('clubcell', '0005_auto_20200131_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alerts',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 57, 7, 899587, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comments',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 57, 7, 914196, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event_participants',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 57, 7, 912094, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='like',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 57, 7, 913791, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 57, 7, 899170, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='posts',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 57, 7, 913154, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='review',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 57, 7, 912635, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='team',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 57, 7, 910365, tzinfo=utc)),
        ),
    ]
