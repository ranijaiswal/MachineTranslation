#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import json



# def process_or_store(tweet):
# 	print(json.dumps(tweet))

# for status in tweepy.Cursor(api.home_timeline).items():
# 	process_or_store(status._json)
#     # Process a single status
# 	print(status.text)

#get tweets from given username
def from_user(screen_name):

	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200, max_id=oldest)

		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))

	return alltweets

#get latest 1000 tweets with given hashtag
def with_hashtag(hashtag):
	alltweets=[]
	new_tweets= api.search(hashtag, rpp=15)
	alltweets.extend(new_tweets)
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until 1000 tweets
	while len(alltweets) < 1000:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.search(hashtag, rpp=15, since_id=oldest)

		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		print("%s tweets downloaded from hashtag %s" % (len(alltweets), hashtag))
	return alltweets



def get_all_tweets(screen_name, get_type):
	if get_type == "user":
		alltweets = from_user(screen_name)
	else:
		alltweets = with_hashtag(screen_name)

	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.entities['hashtags'], tweet.entities['user_mentions']] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	
	pass



if __name__ == '__main__':
	#Twitter API credentials
	consumer_key = "wHkpnhdvxiwxb5SkVmvX04nd7"
	consumer_secret = "M7fL2HJQ0DY9wmXGHPSwFdwW9nJ45CGKftWwny8J33PEZx3zLG"
	access_key = "857925427326836738-YKuPsNeO4TiQ3q1QxBclYTb4IiorWSV"
	access_secret = "mu5XMh4UY6ChwFrbJkt1SEMDM48je0xjrc2bpWG0rsJSE"

	#Twitter only allows access to a users most recent 3240 tweets with this method
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#pass in the username of the account you want to download
	get_all_tweets("","user")

	#pass in the hashtag you want to download
	get_all_tweets("#","hashtag")


