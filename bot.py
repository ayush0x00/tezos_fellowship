from dotenv import load_dotenv
import os
import tweepy
import json
import requests

class AuthHandler:
    def authenticate_twitter_app(self):
        auth=tweepy.OAuthHandler(os.environ.get('api_key'),os.environ.get('api_key_secret'))
        auth.set_access_token(os.environ.get('access_token'),os.environ.get('access_token_secret'))
        api=tweepy.API(auth)
        return api

class MyStreamListener(tweepy.StreamListener):

    def tokenizeAsset(self, data):
        
        pass
       

    def on_status(self, status):
        if(status.is_quote_status):
            print("Tokenizing tweet of user...",status.quoted_status.user.name)
            print("Tweet data is....",status.quoted_status.text)
            print("-------------------------")
            self.tokenizeAsset(status.quoted_status.text)
        else:
            print("Tokenizing a new tweet of user....",status.user.name)
            print("Tweet data is....",status.text)
            print("-------------------------")
            self.tokenizeAsset(status.text)
    
    def on_error(self, status_code):
        print(status_code)
    

class Streamer:
    def __init__(self):
        self.authenticate=AuthHandler()

    def streamTweets(self,rule):
        listener=MyStreamListener()
        api=self.authenticate.authenticate_twitter_app()
        myStream = tweepy.Stream(auth = api.auth, listener=listener)
        myStream.filter(track=rule,is_async=True)


if __name__== "__main__":
    load_dotenv()
    rule=["tokenTezos"]
    stream=Streamer()
    stream.streamTweets(rule)
    