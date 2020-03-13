# Generated by Django 3.0.2 on 2020-01-31 08:31

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('clubcell', '0002_auto_20200131_0621'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubcell.clubcell'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='alerts',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 30, 50, 731823, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comments',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 30, 50, 746171, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event_participants',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 30, 50, 744089, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='like',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 30, 50, 745769, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 30, 50, 731359, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='posts',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 30, 50, 745106, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='review',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 30, 50, 744588, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='team',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 8, 30, 50, 742354, tzinfo=utc)),
        ),
    ]