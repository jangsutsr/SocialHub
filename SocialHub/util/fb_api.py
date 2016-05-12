import requests
import json
from datetime import datetime, timedelta

# Two ways to get the access token:
# 1: Gerenate an access token through: https://developers.facebook.com/tools/explorer/
# 2: implement facebook login(front end)
access_token = 'EAACEdEose0cBAGaTvTTisHQB1DRh3ZCZBIzxPZBxawzZCd3ZAjZB5YPMqXXP0D9QBwtjG0touqYx543WztxTvkgNwCHZBx8oL9vG8gSZC1DorZAJOGyEKMMDJTHgbeZB4nbjVBFBmukGL58nZBecoIDhEhzFaxJU3fPnVBuHbjUkR6lUAZDZD'
fb_url = 'https://graph.facebook.com/v2.6/'
likes_url = 'https://graph.facebook.com/v2.6/me/likes'

def get_friends(access_token):
	likes = list()
	try:
		r = requests.get(likes_url, params={'access_token': access_token})
		for like in json.loads(r.text)['data']:
			tmp = dict()
			tmp['id'] = like['id']
			tmp['name'] = like['name']
			likes.append(tmp)
	except:
		print r.content
		print 'facebook friends request excesses rate limit'
	return likes

def get_posts(likes, access_token, start_time, end_time):

	if end_time - start_time > timedelta(minutes=30):
		limit = 100
	else:
		limit = 20

	posts = list()
	try:
		for like in likes:
			posts_url = fb_url + like[0] + '/feed'
			r = requests.get(posts_url, params={'access_token': access_token, 'limit': limit})
			like_posts = json.loads(r.content)['data']

			for post in like_posts:
				if 'message' not in post:
					continue
				tmp_time = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
				if not (start_time < tmp_time <= end_time):
					continue

				tmp = dict()
				tmp['created_time'] = tmp_time
				tmp['meg'] = post['message']
				tmp['post_id'] = post['id']
				tmp['page_id'] = like[0]
				tmp['page_name'] = like[1]
				posts.append(tmp)
	except:
		print r.content
		print 'facebook posts request excesses rate limit'
	return posts

# tmp = get_friends(access_token)
# likes = [(i['id'],i['name']) for i in tmp]
# time_now = datetime.utcnow()




