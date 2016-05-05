# -*- coding: UTF-8 -*-
from django.test import TestCase, Client
from django.contrib.auth.models import User
import datetime
from .models import TwitterMessage, FacebookMessage

class TwitterTestCase(TestCase):
    def setUp(self):
        self.browser = Client()

    def _store_dummy_tweet(self, username='name'):
        user = User.objects.filter(username=username)\
                           .get()
        TwitterMessage.objects.create(text='heheh',
                                      created_at=datetime.datetime.utcnow()
                                            + datetime.timedelta(2),
                                      author='haha',
                                      owner=user)
        TwitterMessage.objects.create(text=unicode('呵呵你一脸～', 'utf8'),
                                      created_at=datetime.datetime.utcnow()
                                            + datetime.timedelta(1),
                                      author='yes',
                                      owner=user)


    def test_twitter_listing(self):
        response = self.browser.post('/register', {'name': 'name',
                                                   'passwd': 'passwd'})
        response = self.browser.post('/login', {'name': 'name',
                                                'passwd': 'passwd'})
        self.assertEqual('User exists.', response.content)
        self._store_dummy_tweet()
        response = self.browser.post('/attach/twitter', {'name': 'hehe',
                                                        'passwd': 'haha'})
        self.assertEqual('twitter account attached', response.content)
        response = self.browser.get('/show/twitter')
        print(response.content)

class FbTestCase(TestCase):
    def setUp(self):
        self.browser = Client()

    def _store_dummy_post(self, username='name'):
        user = User.objects.filter(username=username)\
                           .get()
        FacebookMessage.objects.create(message='蛤蛤蛤',
                                       time=datetime.datetime.utcnow()
                                            + datetime.timedelta(2),
                                       page_name='暴力膜',
                                       owner=user)
        FacebookMessage.objects.create(message='exciting',
                                       time=datetime.datetime.utcnow()
                                            + datetime.timedelta(1),
                                       page_name='膜法师',
                                       owner=user)


    def test_fb_listing(self):
        response = self.browser.post('/register', {'name': 'name',
                                                   'passwd': 'passwd'})
        response = self.browser.post('/login', {'name': 'name',
                                                'passwd': 'passwd'})
        self.assertEqual('User exists.', response.content)
        self._store_dummy_post()
        response = self.browser.post('/attach/facebook', {'name': 'hehe',
                                                        ' passwd': 'haha'})
        self.assertEqual('facebook account attached', response.content)
        response = self.browser.get('/show/facebook')
        print(response.content)
