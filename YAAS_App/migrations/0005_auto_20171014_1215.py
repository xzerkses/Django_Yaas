# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-14 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YAAS_App', '0004_auto_20171013_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='latest_pid',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='auction',
            name='start_price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
