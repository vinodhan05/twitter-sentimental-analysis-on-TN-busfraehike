
# coding: utf-8

import tweepy
import csv
import pandas as pd
from textblob import TextBlob
import re
import numpy as np

####input your credentials here
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#####United Airlines
# Open/Create a file to append data
csvFile = open('busfarehike1.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)
tweets = tweepy.Cursor(api.search,q="#BusFareHike",count=100,
                           lang="en",
                           since="2018-01-01").items()
for tweet in tweets:
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])

data = pd.read_csv('busfarehike1.csv', names=['dot','tweets'])

tweets = data['tweets']

def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing 
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1
    
data['polarity'] = np.array([ analize_sentiment(tweet) for tweet in data['tweets'] ])
#data.head()

pos_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['Polarity'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['Polarity'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['Polarity'][index] < 0]

print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data['tweets'])))
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data['tweets'])))
print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(data['tweets'])))

