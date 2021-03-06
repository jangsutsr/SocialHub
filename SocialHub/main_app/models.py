from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from datetime import timedelta

class UserProfile(models.Model):
    '''Profile associated with actual users providing extra user info.

    Attributes:
        user: Foreign key associated with user.
        fb_name: Facebook user name attached by user.
        fb_token: Facebook token attached by user.
        fb_id: Facebook social id attached by user.
        twitter_name: Twitter user name attached by user.
        resource_owner_key: Twitter user key attached by user.
        resource_owner_secret: Twitter user secret attached by user.
        twitter_id: Twitter user id attached by user.
        last_query: Time of the last call of /show url. Used to segment
        messages by period.
        last_fetch: Time of the last execution of message fetch script.
        Used to avoid duplicate messages.
    '''
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
        '''Callback function triggered by creation of new user.
        '''
        if kwargs['created']:
            UserProfile.objects.create(user=kwargs['instance'],
                                       last_query=timezone.now(),
                                       last_fetch=timezone.now())

    @classmethod
    def insert_twitter_token(cls, form, user):
        '''Function for storing temporary token and secret.

        This function is needed because temporary token and secret are needed
        for fetching the corresponding user_profile when fetching the actual
        token and secret.
        '''
        cls.objects\
           .filter(user=user.id)\
           .update(resource_owner_key=form['oauth_token'],
                   resource_owner_secret=form['oauth_token_secret'])

    @classmethod
    def insert_account(cls, token, form, cate):
        '''Function for storing social network api authentication info.
        '''
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
        '''Function used for updating query_time when /show is called.
        '''
        cls.objects.filter(user=user.id)\
                   .update(last_query=timezone.now())

class Friend(models.Model):
    '''Table containing info of user's friends.

    Attributes:
        friendee: Foreign key pointing to the user whom the friend is associated.
        name: Friend name.
        catecory: Indicator of whether the friend is a fb friend or twitter friend.
        social_id: social_id associated with each fb/twitter user.
        is_favorite: Boolean indicating if the friend is a favorite one.
        tag: The category of the friend to be shown in front end.
        img: URL of the image used to identify friends in front end.
    '''
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
        '''Function for retriving the whole list of a user's friends.
        '''
        return list(cls.objects\
                       .filter(friendee=user)\
                       .values('name', 'is_favorite',
                               'category', 'social_id',
                               'img', 'tag'))

    @classmethod
    def update_favorite(cls, user, to_update):
        '''Function to update the is_favorite property of a user's friends.
        '''
        cls.objects.all().update(is_favorite=1)
        for item in to_update:
            cls.objects.filter(friendee=user,
                               category=item['category'],
                               social_id=item['social_id'])\
                       .update(is_favorite=0)

class Message(models.Model):
    '''Table containing general info of specific messages.

    Attributes:
        category: Whether this message is a tweet or fb message.
        time: Post time of the post.
        author: Foreign key pointing to the friend posting this message.
        owner: Foreign Key pointing to the user this message belongs to.
        social_id: The unique id pertaining to each message.
    '''
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
        '''Function for retriving the newest posts of a user.
        '''
        last_query = UserProfile.objects.filter(user=user)\
                                        .get()\
                                        .last_query
        return list(cls.objects.filter(owner=user.id,
                                       time__gte=last_query-timedelta(hours=4))\
                               .order_by('time')\
                               .values('author__name', 'message',
                                       'author__tag', 'author__img',
                                       'time', 'category'))[-50:]

    @classmethod
    def get_offset_posts(cls, user, offset):
        '''Function for retriving posts starting from a particular offest.
        '''
        return list(cls.objects.filter(owner=user.id)\
                               .order_by('time')\
                               .values('author__name', 'message',
                                       'author__tag', 'author__img',
                                       'time', 'category'))[offset:offset+50]

    @classmethod
    def get_favorite_posts(cls, user, offset):
        '''Function for retriving offsetted posts of only the favorite friends
        of a user.
        '''
        return list(cls.objects.filter(owner=user.id,
                                       author__is_favorite=0)\
                               .order_by('time')\
                               .values('author__name', 'message',
                                       'author__tag', 'author__img',
                                       'time', 'category'))[offset:offset+50]
