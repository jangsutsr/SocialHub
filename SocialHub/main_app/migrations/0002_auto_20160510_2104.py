# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-10 21:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='last_fetch',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_query',
            field=models.DateTimeField(default=None),
        ),
    ]