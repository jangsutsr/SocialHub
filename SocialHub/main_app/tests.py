# -*- coding: UTF-8 -*-
from django.test import TestCase, Client
from django.contrib.auth.models import User
import datetime
from .models import Message, UserProfile
from time import sleep

class MsgTestCase(TestCase):
    def setUp(self):
        self.browser = Client()

    def _store_dummy_msg(self, username='name'):
        user = User.objects.filter(username=username)\
                           .get()
        Message.objects.create(message='heheh',
                               time=datetime.datetime.utcnow()
                                        + datetime.timedelta(2),
                               author='haha',
                               owner=user,
                               category='twitter')
        Message.objects.create(message=unicode('呵呵你一脸～', 'utf8'),
                               time=datetime.datetime.utcnow()
                                        + datetime.timedelta(1),
                               author='yes',
                               owner=user,
                               category='twitter')
        Message.objects.create(message='蛤蛤蛤',
                               time=datetime.datetime.utcnow()
                                    + datetime.timedelta(2),
                               author='暴力膜',
                               owner=user,
                               category='facebook')
        Message.objects.create(message='exciting',
                               time=datetime.datetime.utcnow()
                                    + datetime.timedelta(1),
                               author='膜法师',
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
                                                        'passwd': 'haha'})
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
