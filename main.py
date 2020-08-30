import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
import tweepy


token= os.getenv('token')
consumer_key= os.getenv('consumer_key')
consumer_secret= os.getenv('consumer_secret')
access_token= os.getenv('access_token')
access_token_secret= os.getenv('access_token_secret')

botsUrl= "https://api.telegram.org/bot{}".format(token)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)



def giveUpdate(offset=None):
	url = botsUrl+ "/getupdates?timeout=100"
	if offset:
		url = botsUrl+ "/getupdates?offset={}&timeout=100".format(offset+1)
	resp= requests.get(url)
	return json.loads(resp.content)

def sendMessage(msg, chat_id):
	url= botsUrl+ "/sendMessage?chat_id={}&text={}".format(chat_id,msg)
	resp= requests.get(url)
	return "sent message"


def getReply(msg):
	tweets= tweepy.Cursor(api.search, q= "#{}".format(msg), lang="en").items(5)
	all_tweets= [tw.user.screen_name+ ' - ' + tw.text for tw in tweets]
	return all_tweets



id_=None
while True:
	update= giveUpdate(offset=id_)
	update= update['result']

	if update:
		for item in update:
			id_= item['update_id']
			msg= item['message']['text']
			chat_id= item['message']['from']['id']
			if msg:
				reply= getReply(msg)
				for tw in reply:
					print(sendMessage(tw, chat_id))




