# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-28 21:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YAAS_App', '0014_auto_20180428_2202'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserLanguageSelection',
            new_name='Profile',
        ),
    ]
