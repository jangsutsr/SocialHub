import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import json
from datetime import datetime, timedelta
import pytz
from dateutil.parser import parse as datetime_parse

client_key = '1VjKOBZr4k8cRycT05PNyXj2i'
client_secret = 'QIIfKQjaGYdBZB1jL1lzGRgNFXCfk87AyyLr8uliHuPLFsYKSo'
home_timeline_url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
friends_ids_url = 'https://api.twitter.com/1.1/friends/ids.json'
lookup_url = 'https://api.twitter.com/1.1/users/lookup.json'

def parse_posts(content, start_time, end_time):
	'''
	Return only the posts between a certain time range
	'''
	posts = list()
	try:
		for post in json.loads(content):

			tmp_time = datetime.strptime(post['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
			if not (start_time < tmp_time <= end_time):
				continue

			tmp = dict()
			tmp['created_time'] = tmp_time
			tmp['meg'] = post['text']
			tmp['post_id'] = post['id']
			tmp['tags'] = list()
			try:
				for tag in post['entities']['hashtags']:
					tmp['tags'].append(tag['text'])
			except KeyError:
				pass
			tmp['user_id'] = post['user']['id']
			tmp['user_img'] = post['user']['profile_image_url_https']
			posts.append(tmp)
	except:
		print 'twitter home_timeline request excesses rate limit'
	return posts

def get_timeline(resource_owner_key, resource_owner_secret, start_time, end_time):
	'''
	Get the home_timeline.
	See: https://dev.twitter.com/rest/reference/get/statuses/home_timeline
	'''

	oauth = OAuth1(client_key=client_key,
				   client_secret=client_secret,
				   resource_owner_key=resource_owner_key,
				   resource_owner_secret=resource_owner_secret)

	r = requests.get(home_timeline_url, auth=oauth, params={'count': 199})
	posts = parse_posts(r.content, start_time, end_time)
	if len(posts) == 0:
		return posts
	else:
		last_id = posts[-1]['post_id']

	while True:
		r = requests.get(home_timeline_url, auth=oauth, params={'count': 199, 'max_id': last_id-1})
		tmp = parse_posts(r.content, start_time, end_time)
		if len(tmp) == 0:
			break
		else:
			posts += tmp
			last_id = tmp[-1]['post_id']

	return posts

def get_friends(resource_owner_key, resource_owner_secret, friendslist=None):
	'''

	Get the friends of an user.
	Note: this api can specific a list of screen_name, which can be used to retrieve only the tweets that one is interested in
	'''
	oauth = OAuth1(client_key=client_key,
				   client_secret=client_secret,
				   resource_owner_key=resource_owner_key,
				   resource_owner_secret=resource_owner_secret)

	friends = list()
	r = requests.get(friends_ids_url, auth=oauth)
	try:
		friends_ids = json.loads(r.content)['ids']

		for friend_id in friends_ids:
			r = requests.get(lookup_url, auth=oauth, params={'user_id': str(friend_id)})
			friend = json.loads(r.content)[0]
			tmp = dict()
			tmp['id'] = friend['id']
			tmp['screen_name'] = friend['screen_name']
			if friend['profile_image_url']:
				tmp['image'] = friend['profile_image_url']
			else:
				tmp['image'] = None
			if friend['url']:
				tmp['url'] = friend['url']
			else:
				tmp['url'] = None
			friends.append(tmp)
	except:
		print 'twitter friends request excesses rate limit'

	return friends

# a = get_timeline('718865201123168256-obsAg2PAjpTvaSr70B4UWVybBSAfs5S','Wssq0oEU6eNp9whollPlAtiDJZn9nVhz7Keag5tplu3y7', time_now-timedelta(days=1), time_now)	
