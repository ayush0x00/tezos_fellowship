import json
import requests

def tokenizeAsset(hashtags,tweet,tweetId):
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
        
tokenizeAsset(["invalid","invalid","tz1dtPTfhgLLHQfDmQXyoT4WMAEHJiTCHPoU"],"hello world","1234")