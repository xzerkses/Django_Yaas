# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-19 05:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YAAS_App', '0009_auto_20171014_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='auction_status',
            field=models.CharField(default='A', max_length=1),
        ),
    ]
