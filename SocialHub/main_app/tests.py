# -*- coding: UTF-8 -*-
from django.test import TestCase, Client
from django.contrib.auth.models import User
import datetime
from .models import TwitterMessage

# Create your tests here.
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
