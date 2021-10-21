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

class MyStreamListener(tweepy.StreamListener,AuthHandler):

    def tokenizeAsset(self, hashtags,tweet,tweetId):
        print("Tokenizing tweet")
        payload={"address":hashtags,"tweet":tweet,"tweetId":tweetId}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r=requests.post("http://localhost:1234",data=json.dumps(payload),headers=headers)
        response=r.json()
        if(response["success"]):
            print("Successfully tokenized with transaction hash ",response["message"])
        else:
            print("Error while tokenizing")
            print(response["message"])

    def on_status(self, status):
        addressList=[]
        hashtags=status.entities["hashtags"]

        for i in hashtags:
            addressList.append(i['text'])

        if(status.in_reply_to_status_id_str):
            orig_tweetId=status.in_reply_to_status_id_str
            print("Tokenizing tweet of user...",status.user.name)
            print("-------------------------")
            api=AuthHandler.authenticate_twitter_app(self)
            tweet=api.get_status(int(orig_tweetId))
            self.tokenizeAsset(addressList,tweet.text,orig_tweetId)
        else:
            print("Tokenizing a new tweet of user....",status.user.name)
            print("-------------------------")
            self.tokenizeAsset(addressList,status.text,status.id_str)
    
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
    