import os
import json
import csv
import time
import datetime
import tweepy
import bs4
import copy
import requests
from tweepy.tweet import Tweet
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import tweepy.errors

class multi_clienthandler:
    poll_fields = ["id","options","duration_minutes","end_datetime","voting_status"]
    place_fields = ["full_name","id","contained_within","country","country_code","geo","name","place_type"]
    tweet_fields = ["id","text","attachments","author_id","context_annotations","conversation_id","created_at","entities","geo","in_reply_to_user_id","lang","possibly_sensitive","public_metrics","referenced_tweets","reply_settings","source","withheld"]
    #organic_metrics, non_public_metrics, promoted_metrics
    # are left out. They require user context authentication
    media_fields = ["media_key","type","duration_ms","height","preview_image_url","public_metrics","width","url"]
    # again, non_public_metrics, promoted_metrics, organic_metrics is left out
    
    user_fields = ["id","name","username","created_at","description","entities","location","pinned_tweet_id","profile_image_url","protected","public_metrics","url","verified","withheld"]
    expansions =  ["author_id","referenced_tweets.id","referenced_tweets.id.author_id","entities.mentions.username","attachments.poll_ids","attachments.media_keys","in_reply_to_user_id","geo.place_id"]
    
    def __init__(self,appkeylist,global_pause=10,will_pull_media=False,global_max_results=100):
        self.clientlist = []
        self.appkeylist = appkeylist
        self.global_pause = global_pause
        self.will_pull_media=will_pull_media
        self.global_max_results=global_max_results
        
   
    def get_tweet(self,tweetid):
        current_bearer=0
        totaltries=0
        obtained_result = self.appkeylist[current_bearer].get_tweets(ids=tweetid,tweet_fields=self.tweet_fields)
        # print(type(obtained_result))
        z = obtained_result._asdict() # is a namedtuple
        outputdict = {}
        try:
            obtained = z["data"]
            for i in obtained:
                outputdict[i.id] = i.text # bruh id is a reserved word
        except KeyError:
            pass
        try:
            failed = z["errors"]
            for i in failed:
                outputdict[i["value"]] = None
        except KeyError:
            pass
        print(outputdict)
        return outputdict
        

    
   
            
if __name__=="__main__":    
    bearer_token  = ""
    app_key = ""
    app_secret = ""
    appkey = tweepy.client.Client(access_token=app_key, access_token_secret=app_secret, wait_on_rate_limit=False)
    parser = tweepy.parsers.JSONParser()
    bearer = tweepy.client.Client(bearer_token = bearer_token,wait_on_rate_limit=False)

    instance = multi_clienthandler([bearer,appkey],global_pause=10,global_max_results=100)
    outdict = {}
    try:
        with open("pulled_tweets.json","r",encoding="utf-8") as opened_files:
            outdict = json.load(opened_files)
    except FileNotFoundError:
        pass
    with open("unseentweetslist.txt","r",encoding="utf-8") as unseentweetlist:
        unseentweetlist = json.load(unseentweetlist)
    
    lastnum = 0
    for tests in range(0,len(unseentweetlist),76):
        if tests ==0:
            continue

        while True:
            try:
                latest = instance.get_tweet(unseentweetlist[lastnum:tests])
                outdict.update(latest)
                time.sleep(1)
                break
            except requests.exceptions.ConnectionError as e:
                print(e)
                time.sleep(2)
                
            
            except tweepy.errors.TooManyRequests as e:
                print("Rate limit exceeded. Sleeping for 10 seconds")
                time.sleep(10)
            
        lastnum = tests
        with open("pulled_tweets.json","w",encoding="utf-8") as opened_files:
            json.dump(outdict,opened_files,indent=4)
