# Generated by Django 3.0.2 on 2020-02-09 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubcell', '0033_auto_20200209_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='parent_event',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='clubcell.group_event'),
        ),
    ]