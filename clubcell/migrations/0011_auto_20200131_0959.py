# Generated by Django 3.0.2 on 2020-01-31 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubcell', '0010_events_parent_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='user',
        ),
        migrations.RemoveField(
            model_name='group_event',
            name='user',
        ),
    ]
