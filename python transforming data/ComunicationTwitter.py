#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys
import newspaper
from newspaper import Article

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'lE5d5fftU0sWk38JgIAcmPMvZ'
CONSUMER_SECRET = 'J9bDQleSnoh54peS3v0UjqtM58U9PI2nkMwBbSgbCGlKX4i8KS'
ACCESS_KEY = '1086852822-O6MBWpfC7GWoxmwJg7B3beaYc66vaWMwpA3EJ6O'
ACCESS_SECRET = 'y0CWTnjaxIGGupWCo2dctGMFr1dBhg3vTAlGuRw8Cwze7'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

count = 0

def format_data(data):
    data = data.replace("\n"," newlinechar ").replace("\r"," newlinechar ").replace('"',"'")
    return data

bbc_paper_saved = newspaper.build('http://www.bbc.com/', language='en', fetch_images=False)



while(True):
    #bbc_paper = newspaper.build('http://www.bbc.com/', language='en', fetch_images=False)
    print(bbc_paper_saved.size())
    first_article = bbc_paper_saved.articles[0]
    first_article.download()
    first_article.parse()
    text = format_data(article.text)
    print(text)
    text_reduced = (' '.join(text.split()[:300])
    time.sleep(30)#Tweet every x seconds

#for line in f:
    #api.update_status(line)
