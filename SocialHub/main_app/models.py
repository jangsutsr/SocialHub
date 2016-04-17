from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30,
                            default='')
    passwd = models.CharField(max_length=30,
                              default='')
    twitter = models.ForeignKey('UserRecord',
                                related_name='+',
                                null=True)
    facebook = models.ForeignKey('UserRecord',
                                 related_name='+',
                                 null=True)
    class Meta(object):
        db_table = 'user'
        unique_together = (
            ('name', ),
        )

class UserRecord(models.Model):
    category = models.IntegerField()
    name = models.CharField(max_length=30,
                            default='')
    passwd = models.CharField(max_length=30,
                              default='')
    class Meta(object):
        db_table = 'user_record'
        unique_together = (
            ('name', ),
        )

class FacebookMsg(models.Model):
    content = models.TextField(default='')
    time = models.DateTimeField(default=None)
    loc = models.CharField(max_length=30, default='')
    owner = models.ForeignKey('UserRecord',
                              default=None)
    class Meta(object):
        db_table = 'facebook_msg'

class TwitterMsg(models.Model):
    content = models.TextField(default='')
    time = models.DateTimeField(default=None)
    loc = models.CharField(max_length=30,
                           default='')
    owner = models.ForeignKey('UserRecord',
                              default=None)
    class Meta(object):
        db_table = 'twitter_msg'
