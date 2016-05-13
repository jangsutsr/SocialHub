import requests
import json
from sqlalchemy import *
from datetime import datetime, timedelta
import twitter_api, fb_api

DATABASEURI = "mysql+mysqldb://admin:foobar@ec2-54-210-25-209.compute-1.amazonaws.com:3306/SocialHub"
engine = create_engine(DATABASEURI)
conn = None

kws = {
'Technology': set(['techstars', 'IBM Research', 'Red Hat, Inc.', 'OSXDaily', 'Post World', '60 Minutes', 'Think with Google', 'NYT Technology', 'Y Combinator', 'Mary Jo Foley', 'Mark Suster', 'TechCrunch']),
'Sport': set(['USGA', 'Fox News Alert', 'Manchester United', 'Memphis', 'The Golf Fix', 'New York Yankees']),
'Science': set(['The NPR Science Desk', 'WIRED Science', 'NASA History Office', 'Science Magazine']),
'News': set(['Ayman Mohyeldin', 'Nicholas Kristof', 'Eyewitness News', 'Brian Tong', 'Tim Stevens', 'CNBC\'s Closing Bell Verified account', 'BuzzFeed Politics', 'Ainsley Earhardt', 'ABC News Live', 'WSJ Business News', 'ISS Research', 'CBS Sunday Morning', 'Fox News', 'The New York Times', 'CNN']),
'Music': set(['HOT 97', 'The Rolling Stones', 'Cody Simpson', 'Ellie Goulding', 'Jordin Sparks', 'Nick Jonas', 'Eminem', 'Ed Sheeran', 'Taylor Swift', 'Lorde', 'Lana Del Rey', 'Manchester United'])
}

fb_img = 'http://popo.or.jp/images/amc/bnr_facebook.jpg'
twitter_img = 'https://lh3.ggpht.com/lSLM0xhCA1RZOwaQcjhlwmsvaIQYaP3c5qbDKCgLALhydrgExnaSKZdGa8S3YtRuVA=w300'

def get_tag(name):

	name = name.encode('utf-8')
	global kws
	for tag in kws:
		if name in kws[tag]:
			return tag
	return 'Other'

def get_sql(command, args=None):

	global conn
	if args:
		cursor = conn.execute(command, args)
	else:
		cursor = conn.execute(command)
	res = [event for event in cursor]
	cursor.close()

	return res

def sql(command, args=None):

	global conn
	if args:
		conn.execute(command, args)
	else:
		conn.execute(command)

def twitter_poll(user_id, resource_owner_key, resource_owner_secret, start_time, end_time):

	assert type(user_id) == int

	tmp_friends = get_sql("select social_id, id from friend where friendee_id=%s and category='twitter'", user_id)
	friends = dict()
	for (social_id, friend_id) in tmp_friends:
		friends[int(social_id)] = friend_id

	posts = twitter_api.get_timeline(resource_owner_key, resource_owner_secret, start_time, end_time)
	for post in posts:
		try:
			sql("insert into message(category, message, time, social_id, author_id, owner_id) values('twitter',%s,%s,%s,%s,%s)", 
				(post['meg'].encode('utf-8'), post['created_time'], post['post_id'], friends[post['user_id']], user_id))
		except:
			print 'uh oh, twitter message insert conflict'
			pass

def fb_poll(user_id, access_token, start_time, end_time):

	assert type(user_id) == int

	tmp_friends = get_sql("select social_id, id, name from friend where friendee_id=%s and category='facebook'", user_id)
	friends = dict()
	likes = list()
	for (social_id, friend_id, name) in tmp_friends:
		friends[social_id] = friend_id
		likes.append((social_id, name))

	posts = fb_api.get_posts(likes, access_token, start_time, end_time)
	for post in posts:
		try:
			sql("insert into message(category, message, time, social_id, author_id, owner_id) values('facebook',%s,%s,%s,%s,%s)", 
				(post['meg'].encode('utf-8'), post['created_time'], post['post_id'], friends[post['page_id']], user_id))
		except:
			print 'uh oh, facebook message insert conflict'
			pass

def social_init(user_id, resource_owner_key=None, resource_owner_secret=None, access_token=None):
	'''
	Left the twitter/facebook tokens blank if you only want to call one of them. e.g. social_init(1, access_token='xxxxxx')
	Input:
		user_id: the primary key of auth_user table
	'''

	assert type(user_id) == int

	# connect to db
	global conn
	try:
		conn = engine.connect()
	except:
		print "uh oh, problem connecting to database"
		import traceback; traceback.print_exc()


	time_now = datetime.utcnow()
	sql("update user_profile set last_fetch=%s where user_id=%s", (time_now, user_id))

	# inserts twitter friends and posts
	if resource_owner_key and resource_owner_secret:
		friends = twitter_api.get_friends(resource_owner_key, resource_owner_secret)
		for friend in friends:
			tag = get_tag(friend['name'])
			image = friend['image'] if friend['image'] else twitter_img
			try:
				sql("insert into friend(name,category,social_id,friendee_id, tag, img, is_favorite) values(%s,'twitter',%s,%s,%s,%s,1)", (friend['name'].encode('utf-8'), friend['id'], user_id, tag, image))
			except:
				print 'uh oh, twitter friend insert conflict'
				pass
		twitter_poll(user_id, resource_owner_key, resource_owner_secret, time_now - timedelta(hours=12), time_now)

	# inserts fb friends and posts
	if access_token:
		friends = fb_api.get_friends(access_token)
		for friend in friends:
			tag = get_tag(friend['name'])
			# try:
			sql("insert into friend(name,category,social_id,friendee_id, tag, img, is_favorite) values(%s,'facebook',%s,%s,%s,%s,1)", (friend['name'].encode('utf-8'), friend['id'].encode('utf-8'), user_id, tag, fb_img))
			# except:
			# 	print 'uh oh, facebook friend insert conflict'
			# 	pass
		fb_poll(user_id, access_token, time_now - timedelta(days=1), time_now)

	# disconnect from db
	try:
		conn.close()
	except Exception as e:
		print "uh oh, problem disconnecting from database"
		pass





