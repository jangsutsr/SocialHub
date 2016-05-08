# -*- coding: UTF-8 -*-
from django.test import TestCase, Client
from django.contrib.auth.models import User
import datetime
from .models import Message, UserProfile, Friend
from time import sleep

class MsgTestCase(TestCase):
    def setUp(self):
        self.browser = Client()

    def _store_dummy_msg(self, username='name'):
        user = User.objects.filter(username=username)\
                           .get()
        fb_friend = Friend.objects.create(friendee=user,
                                          name='暴力膜')
        twitter_friend = Friend.objects.create(friendee=user,
                                          name='膜法师')
        Message.objects.create(message='heheh',
                               time=datetime.datetime.utcnow()
                                        + datetime.timedelta(2),
                               author=twitter_friend,
                               owner=user,
                               category='twitter')
        Message.objects.create(message='呵呵你一脸～',
                               time=datetime.datetime.utcnow()
                                        + datetime.timedelta(1),
                               author=twitter_friend,
                               owner=user,
                               category='twitter')
        Message.objects.create(message='蛤蛤蛤',
                               time=datetime.datetime.utcnow()
                                    + datetime.timedelta(2),
                               author=fb_friend,
                               owner=user,
                               category='facebook')
        Message.objects.create(message='exciting',
                               time=datetime.datetime.utcnow()
                                    + datetime.timedelta(1),
                               author=fb_friend,
                               owner=user,
                               category='facebook')

    def test_twitter_listing(self):
        response = self.browser.post('/register', {'name': 'name',
                                                   'passwd': 'passwd'})
        response = self.browser.post('/login', {'name': 'name',
                                                'passwd': 'passwd'})
        self.assertEqual('User exists.', response.content)
        self._store_dummy_msg()
        response = self.browser.post('/attach/twitter', {'name': 'hehe',
                                                         'identity': 'haha',
                                                         'key': 'hoho',
                                                         'secret': 'heihei'})
        self.assertEqual('twitter account attached', response.content)
        user = User.objects.filter(username='name')\
                           .get()
        print(UserProfile.objects.filter(user=user)\
                         .get().last_query)
        sleep(5)
        response = self.browser.get('/show')
        print(response.content)
        print(UserProfile.objects.filter(user=user)\
                         .get().last_query)
        response = self.browser.get('/history/2')
        print(response.content)
