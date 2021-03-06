# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-14 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YAAS_App', '0005_auto_20171014_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='auction_status',
            field=models.CharField(choices=[('A', 'Active'), ('BANNED', 'Banned'), ('DUE', 'Due'), ('ADJUDICATED', 'Adjudicated')], default='A', max_length=1),
        ),
        migrations.AlterField(
            model_name='auction',
            name='latest_pid',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='auction',
            name='start_price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
