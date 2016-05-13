import requests
import json
from sqlalchemy import *
from datetime import datetime, timedelta
from time import sleep
import twitter_api, fb_api

DATABASEURI = "mysql+mysqldb://admin:foobar@ec2-54-210-25-209.compute-1.amazonaws.com:3306/SocialHub"
engine = create_engine(DATABASEURI)
conn = None

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

if __name__ == '__main__':

	while True:

		# connect to db
		try:
			conn = engine.connect()
		except:
			print "uh oh, problem connecting to database"
			import traceback; traceback.print_exc()
			continue

		users = get_sql('select id from auth_user')
		time_now = datetime.utcnow()

		for (user_id,) in users:
			# get twitter and fb credentials
			user_id = int(user_id)
			resource_owner_key, resource_owner_secret, access_token, last_fetch = get_sql('select resource_owner_key, resource_owner_secret, fb_token, last_fetch from user_profile where user_id=%s', user_id)[0]
			if last_fetch is None:
				print str(user_id) + ' hasn\'t been initilized.'
				continue
			print str(user_id) + ': ' + str(time_now - last_fetch)
			# if time_now - last_fetch < timedelta(minutes=16):
			# 	continue

			# update last_fetech
			sql("update user_profile set last_fetch=%s where user_id=%s", (time_now, user_id))
			print str(user_id) + ': ' + 'update last_fetch'

			if resource_owner_key and resource_owner_secret:
				print str(user_id) + ': twitter'
				twitter_poll(user_id, resource_owner_key, resource_owner_secret, last_fetch, time_now)
			if access_token:
				print str(user_id) + ': ' + access_token
				fb_poll(user_id, access_token, last_fetch, time_now)

		# disconnect from db
		try:
			conn.close()
		except Exception as e:
			print "uh oh, problem disconnecting from database"
			pass

		print 'go to sleep'
		# sleep for 20 mins
		for _ in range(20):
			sleep(60)


