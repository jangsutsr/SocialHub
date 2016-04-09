from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserRecord(models.Model):
    category = models.IntegerField()
    name = models.CharField(max_length=30, default='')
    passwd = models.CharField(max_length=30, default='')
    class Meta(object):
        db_table = 'user_record'
        unique_together = (
            ('name', ),
        )

class User(models.Model):
    name = models.CharField(max_length=30, default='')
    passwd = models.CharField(max_length=30, default='')
    twitter = models.ForeignKey('UserRecord', on_delete=models.CASCADE, related_name='+', null=True)
    facebook = models.ForeignKey('UserRecord', on_delete=models.CASCADE, related_name='+', null=True)
    class Meta(object):
        db_table = 'user'
        unique_together = (
            ('name', ),
        )

class FacebookMsg(models.Model):
    content = models.TextField(default='')
    time = models.DateTimeField(null=True)
    loc = models.CharField(max_length=30, default='')
    owner = models.ForeignKey('UserRecord', on_delete=models.CASCADE, null=True)
    class Meta(object):
        db_table = 'facebook_msg'

class TwitterMsg(models.Model):
    content = models.TextField(default='')
    time = models.DateTimeField(null=True)
    loc = models.CharField(max_length=30, default='')
    owner = models.ForeignKey('UserRecord', on_delete=models.CASCADE, null=True)
    class Meta(object):
        db_table = 'twitter_msg'
