# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-12 04:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20160510_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='is_favorite',
            field=models.SmallIntegerField(default=1),
        ),
    ]