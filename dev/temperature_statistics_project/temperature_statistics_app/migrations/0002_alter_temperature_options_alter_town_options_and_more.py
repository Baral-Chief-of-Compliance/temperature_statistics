# Generated by Django 4.2.16 on 2024-10-12 14:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temperature_statistics_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='temperature',
            options={'ordering': ['-tmp_date'], 'verbose_name': 'Температура', 'verbose_name_plural': 'Температуры'},
        ),
        migrations.AlterModelOptions(
            name='town',
            options={'ordering': ['-t_name'], 'verbose_name': 'Город', 'verbose_name_plural': 'Города'},
        ),
        migrations.RemoveField(
            model_name='temperature',
            name='tmp_hour',
        ),
        migrations.AddField(
            model_name='temperature',
            name='tmp_value',
            field=models.IntegerField(default=0, verbose_name='Значение по Цельсия'),
        ),
        migrations.AlterField(
            model_name='temperature',
            name='tmp_date',
            field=models.DateTimeField(default=datetime.datetime.today, verbose_name='Дата'),
        ),
    ]
