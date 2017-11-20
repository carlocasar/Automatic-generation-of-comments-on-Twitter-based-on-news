#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'lE5d5fftU0sWk38JgIAcmPMvZ'
CONSUMER_SECRET = 'J9bDQleSnoh54peS3v0UjqtM58U9PI2nkMwBbSgbCGlKX4i8KS'
ACCESS_KEY = '1086852822-O6MBWpfC7GWoxmwJg7B3beaYc66vaWMwpA3EJ6O'
ACCESS_SECRET = 'y0CWTnjaxIGGupWCo2dctGMFr1dBhg3vTAlGuRw8Cwze7'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

f='''Hello World! \n
Bye world!
'''

for line in f:
    api.update_status(line)
    time.sleep(900)#Tweet every 15 minutes
