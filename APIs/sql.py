import requests
import json
from sqlalchemy import *
from datetime import datetime, timedelta
import pytz
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



# connect to db
try:
	conn = engine.connect()
except:
	print "uh oh, problem connecting to database"
	import traceback; traceback.print_exc()

sql('update user_profile set fb_token=\'EAACEdEose0cBAPVNTu9gZBptC0Dd9S0i9jTNeLlhtnG5QzSZCIys68mOdu9Pq7iFGtirjggHSNQRrBgunXavVUBVvFWq4dXEprW9YphgWqMZAojHy1AN4EtyobBww2n9cfbix250YLp6cQWzz7AiZCZBuiO2cczJrTZCyMWMUHQwZDZD\' where id=2')


