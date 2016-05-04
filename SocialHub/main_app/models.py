from __future__ import unicode_literals

from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    fb_name = models.CharField(max_length=30,
                               default='')
    fb_passwd = models.CharField(max_length=30,
                                 default='')
    twitter_name = models.CharField(max_length=30,
                                    default='')
    twitter_passwd = models.CharField(max_length=30,
                                      default='')

    class Meta(object):
        db_table = 'user_profile'
        unique_together = (
            ('user', ),
        )

    @classmethod
    def create_profile(cls, user):
        cls.objects.create(user=user)

    @classmethod
    def insert_account(cls, form, user, cate):
        if cate == 1:
            cls.objects.filter(user=user.id)\
                    .update(fb_name=form['name'].data,
                            fb_passwd=form['passwd'].data)
        elif cate == 2:
            cls.objects.filter(user=user.id)\
                    .update(twitter_name=form['name'].data,
                            twitter_passwd=form['passwd'].data)

class FacebookMessage(models.Model):
    content = models.TextField(default='')
    time = models.DateTimeField(default=None)
    loc = models.CharField(max_length=30, default='')
    owner = models.ForeignKey(User,
                              default=None)
    class Meta(object):
        db_table = 'facebook_msg'

class TwitterMessage(models.Model):
    text = models.TextField(default='')
    created_at = models.DateTimeField(default=None)
    author = models.TextField(default='')
    owner = models.ForeignKey(User,
                              default=None)
    class Meta(object):
        db_table = 'twitter_msg'
