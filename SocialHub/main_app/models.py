from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    fb_name = models.CharField(max_length=30,
                               default='')
    fb_passwd = models.CharField(max_length=30,
                                 default='')
    fb_last_query = models.DateTimeField(null=True)
    fb_last_fetch = models.DateTimeField(null=True)
    twitter_name = models.CharField(max_length=30,
                                    default='')
    twitter_passwd = models.CharField(max_length=30,
                                      default='')
    twitter_last_query = models.DateTimeField(null=True)
    twitter_last_fetch = models.DateTimeField(null=True)

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
                            fb_passwd=form['passwd'].data,
                            fb_last_query=timezone.now(),
                            fb_last_fetch=timezone.now())
        elif cate == 2:
            cls.objects.filter(user=user.id)\
                    .update(twitter_name=form['name'].data,
                            twitter_passwd=form['passwd'].data,
                            twitter_last_query=timezone.now(),
                            twitter_last_fetch=timezone.now())

    @classmethod
    def update_query_time(cls, user, cate):
        if cate == 1:
            cls.objects.filter(user=user.id)\
                       .update(fb_last_query=timezone.now())
        elif cate == 2:
            cls.objects.filter(user=user.id)\
                       .update(twitter_last_query=timezone.now())

class FacebookMessage(models.Model):
    message = models.TextField(default='')
    time = models.DateTimeField(default=None)
    page_name = models.TextField(default='')
    owner = models.ForeignKey(User,
                              default=None)
    class Meta(object):
        db_table = 'facebook_msg'

    @classmethod
    def get_posts(cls, user):
        fb_last_query = UserProfile.objects.filter(user=user)\
                                           .get()\
                                           .fb_last_query
        return list(cls.objects.filter(owner=user.id,
                                       time__gte=fb_last_query)\
                               .order_by('time')\
                               .values('page_name', 'message', 'time'))

class TwitterMessage(models.Model):
    text = models.TextField(default='')
    created_at = models.DateTimeField(default=None)
    author = models.TextField(default='')
    owner = models.ForeignKey(User,
                              default=None)
    class Meta(object):
        db_table = 'twitter_msg'

    @classmethod
    def get_tweets(cls, user):
        twitter_last_query = UserProfile.objects.filter(user=user)\
                                        .get()\
                                        .twitter_last_query
        return list(cls.objects.filter(owner=user.id,
                                       created_at__gte=twitter_last_query)\
                               .order_by('created_at')\
                               .values('author', 'text', 'created_at'))
