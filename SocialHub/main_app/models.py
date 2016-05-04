from __future__ import unicode_literals

from django.db import models
from django.db.utils import IntegrityError

class User(models.Model):
    name = models.CharField(max_length=30,
                            default='')
    passwd = models.CharField(max_length=30,
                              default='')
    last_access_time = models.DateTimeField(null=True)
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

    @classmethod
    def does_exist(cls, form):
        return (cls.objects.filter(name=form['name'].data,
                                   passwd=form['passwd'].data)
                           .exists())

    @classmethod
    def insert_user(cls, form):
        try:
            cls.objects.create(name=form['name'].data,
                               passwd=form['passwd'].data)
            return True
        except IntegrityError:
            return False

    @classmethod
    def attach_account(cls, obj, user_name, cate):
        if cate == 1:
            cls.objects.filter(name=user_name)\
                    .update(facebook=obj)
        elif cate == 2:
            cls.objects.filter(name=user_name)\
                    .update(twitter=obj)

class UserRecord(models.Model):
    category = models.IntegerField()
    name = models.CharField(max_length=30,
                            default='')
    passwd = models.CharField(max_length=30,
                              default='')
    class Meta(object):
        db_table = 'user_record'

    @classmethod
    def insert_user(cls, form, cate):
        obj, created = cls.objects\
                .update_or_create(category=cate,
                                  name=form['name'].data,
                                  passwd=form['passwd'].data)
        return obj

class FacebookMsg(models.Model):
    content = models.TextField(default='')
    time = models.DateTimeField(default=None)
    loc = models.CharField(max_length=30, default='')
    owner = models.ForeignKey('UserRecord',
                              default=None)
    class Meta(object):
        db_table = 'facebook_msg'

class TwitterMsg(models.Model):
    text = models.TextField(default='')
    created_at = models.DateTimeField(default=None)
    author = models.TextField(default='')
    owner = models.ForeignKey('UserRecord',
                              default=None)
    class Meta(object):
        db_table = 'twitter_msg'
