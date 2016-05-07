from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    fb_name = models.CharField(max_length=30,
                               default='')
    fb_token = models.TextField(default='')
    twitter_name = models.CharField(max_length=30,
                                    default='')
    twitter_token = models.TextField(default='')
    last_query = models.DateTimeField(null=True)
    last_fetch = models.DateTimeField(null=True)

    class Meta(object):
        db_table = 'user_profile'
        unique_together = (
            ('user', ),
        )

    @classmethod
    def create_profile(cls, user):
        cls.objects.create(user=user,
                           last_query=timezone.now(),
                           last_fetch=timezone.now())

    @classmethod
    def insert_account(cls, form, user, cate):
        if cate == 1:
            cls.objects.filter(user=user.id)\
                    .update(fb_name=form['name'].data,
                            fb_token=form['passwd'].data)
        elif cate == 2:
            cls.objects.filter(user=user.id)\
                    .update(twitter_name=form['name'].data,
                            twitter_token=form['passwd'].data)

    @classmethod
    def update_query_time(cls, user):
        cls.objects.filter(user=user.id)\
                   .update(last_query=timezone.now())

class Friend(models.Model):
    friendee = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=30,
                            default='')

    class Meta(object):
        db_table = 'friend'

class Message(models.Model):
    category = models.CharField(max_length=30,
                                default='')
    message = models.TextField(default='')
    time = models.DateTimeField(default=None)
    author = models.ForeignKey(Friend,
                               on_delete=models.CASCADE)
    owner = models.ForeignKey(User,
                              default=None)
    class Meta(object):
        db_table = 'message'

    @classmethod
    def get_posts(cls, user):
        last_query = UserProfile.objects.filter(user=user)\
                                        .get()\
                                        .last_query
        return list(cls.objects.filter(owner=user.id,
                                       time__gte=last_query)\
                               .order_by('time')\
                               .values('author__name', 'message',
                                       'time', 'category'))

    @classmethod
    def get_offset_posts(cls, user, offset):
        return list(cls.objects.filter(owner=user.id)\
                               .order_by('time')\
                               .values('author__name', 'message',
                                       'time', 'category'))[offset:offset+10]
