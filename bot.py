#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys

argfile = str(sys.argv[1])

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'Akt8RpbTNFihflTXFx4bQ1yo1'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'C15m362GAv7yXcWpBo9Y4WTVJDnCSkTOkY4NkJ20e7nR9L2IzB'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '858407813185503237-Eq2prbWqMXaUe4VFZ6DNwnwwtb9HJCr'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'BKUBtkciZa0BhDeDB0fiskF4MHQSAuJTgniNHXzvXT6OL'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

filename=open(argfile,'r')
f=filename.readlines()
filename.close()

for line in f:
    api.update_status(line)
    time.sleep(60)#Tweet every 15 minutes