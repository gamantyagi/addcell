# Generated by Django 3.0.2 on 2020-01-31 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubcell', '0009_auto_20200131_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='parent_event',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='clubcell.group_event'),
        ),
    ]
