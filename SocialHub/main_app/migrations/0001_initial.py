# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-06 21:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=30)),
                ('message', models.TextField(default='')),
                ('time', models.DateTimeField(default=None)),
                ('author', models.TextField(default='')),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_name', models.CharField(default='', max_length=30)),
                ('fb_token', models.TextField(default='')),
                ('twitter_name', models.CharField(default='', max_length=30)),
                ('twitter_token', models.TextField(default='')),
                ('last_query', models.DateTimeField(null=True)),
                ('last_fetch', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userprofile',
            unique_together=set([('user',)]),
        ),
    ]
