# Generated by Django 3.0.2 on 2020-02-09 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubcell', '0036_auto_20200209_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event_participants',
            old_name='event',
            new_name='events',
        ),
    ]
