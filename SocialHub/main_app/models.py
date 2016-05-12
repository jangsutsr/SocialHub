from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    fb_name = models.CharField(max_length=30,
                               default='')
    fb_token = models.TextField(default='')
    fb_id = models.TextField(default='')
    twitter_name = models.CharField(max_length=30,
                                    default='')
    resource_owner_key = models.TextField(default='')
    resource_owner_secret = models.TextField(default='')
    twitter_id = models.TextField(default='')
    last_query = models.DateTimeField(default=None)
    last_fetch = models.DateTimeField(default=None)

    class Meta(object):
        db_table = 'user_profile'
        unique_together = (
            ('user', ),
        )

    @staticmethod
    @receiver(post_save, sender=User)
    def create_profile(sender, **kwargs):
        if kwargs['created']:
            UserProfile.objects.create(user=kwargs['instance'],
                                       last_query=timezone.now(),
                                       last_fetch=timezone.now())

    @classmethod
    def insert_twitter_token(cls, form, user):
        cls.objects\
           .filter(user=user.id)\
           .update(resource_owner_key=form['oauth_token'],
                   resource_owner_secret=form['oauth_token_secret'])

    @classmethod
    def insert_account(cls, token, form, cate):
        if cate == 1:
            cls.objects\
               .filter(user=user.id)\
               .update(fb_name=form.cleaned_data['name'],
                       fb_token=form.cleaned_data['token'],
                       fb_id=form.cleaned_data['identity'])
        elif cate == 2:
            cls.objects\
               .filter(resource_owner_key=token)\
               .update(twitter_name=form['screen_name'],
                       twitter_id=form['user_id'],
                       resource_owner_key=form['oauth_token'],
                       resource_owner_secret=form['oauth_token_secret'])

    @classmethod
    def update_query_time(cls, user):
        cls.objects.filter(user=user.id)\
                   .update(last_query=timezone.now())

class Friend(models.Model):
    friendee = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=30,
                            default='')
    category = models.CharField(max_length=30,
                                default='')
    social_id = models.CharField(max_length=100,
                                 null=True)
    is_favorite = models.SmallIntegerField(default=1)
    tag = models.CharField(max_length=50,
                           default='other')
    img = models.URLField(default='')

    class Meta(object):
        db_table = 'friend'
        unique_together = (
            ('category', 'social_id', 'friendee'),
        )

    @classmethod
    def get_friends(cls, user):
        return list(cls.objects\
                       .filter(friendee=user)\
                       .values('name', 'is_favorite',
                               'category', 'social_id',
                               'img', 'tag'))

    @classmethod
    def update_favorite(cls, user, to_update):
        cls.objects.all().update(is_favorite=1)
        for item in to_update:
            cls.objects.filter(friendee=user,
                               category=item['category'],
                               social_id=item['social_id'])\
                       .update(is_favorite=0)

class Message(models.Model):
    category = models.CharField(max_length=30,
                                default='')
    message = models.TextField(default='')
    time = models.DateTimeField(default=None)
    author = models.ForeignKey(Friend,
                               on_delete=models.CASCADE)
    owner = models.ForeignKey(User,
                              default=None)
    social_id = models.CharField(max_length=100,
                                 null=True)
    class Meta(object):
        db_table = 'message'
        unique_together = (
            ('category', 'social_id', 'owner'),
        )

    @classmethod
    def get_posts(cls, user):
        last_query = UserProfile.objects.filter(user=user)\
                                        .get()\
                                        .last_query
        return list(cls.objects.filter(owner=user.id,
                                       time__gte=last_query)\
                               .order_by('time')\
                               .values('author__name', 'message',
                                       'author__tag', 'author__img',
                                       'time', 'category'))[-50:]

    @classmethod
    def get_offset_posts(cls, user, offset):
        return list(cls.objects.filter(owner=user.id)\
                               .order_by('time')\
                               .values('author__name', 'message',
                                       'author__tag', 'author__img',
                                       'time', 'category'))[offset:offset+50]

    @classmethod
    def get_favorite_posts(cls, user, offset):
        return list(cls.objects.filter(owner=user.id,
                                       author__is_favorite=0)\
                               .order_by('time')\
                               .values('author__name', 'message',
                                       'author__tag', 'author__img',
                                       'time', 'category'))[offset:offset+50]
