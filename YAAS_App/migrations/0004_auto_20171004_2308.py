# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-04 20:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('YAAS_App', '0003_auto_20171004_2059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='starting_price',
            new_name='start_price',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='auction_endtime',
        ),
        migrations.AddField(
            model_name='auction',
            name='endtime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 10, 4, 20, 8, 13, 81292, tzinfo=utc)),
        ),
    ]
