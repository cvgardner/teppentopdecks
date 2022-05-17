#!/usr/bin/env python
# tweepy-bots/bots/favretweet.py

import tweepy
import logging
from config import create_scraper, create_user
import json
import boto3
import requests
import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class RetweetListener(tweepy.StreamingClient):
    def __init__(self):
        self.user_api = create_user()
        self.scraper_api = create_scraper()
        self.me = self.user_api.get_me()

        #initialize with rules
        self.add_rules("teppen_deck OR teppendeck")

        #aws setup
        self.setup_aws()

    def setup_aws(self):
        #initialize AWS
        self.AWS_REGION = "us-east-1"
        self.S3_BUCKET_NAME = "teppentopdecks"
        self.s3_client = boto3.client("s3", region_name=self.AWS_REGION)


    def on_tweet(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")

        #retweet
        self.user_api.retweet(tweet.id)

        #check attachments
        if tweet.attachements is not None:
            #fetch image from url
            url = tweet.includes['media']['url']
            r = requests.get(url, stream=True)

            #create file name
            name = tweet.includes['media']['media_key']
            ts = datetime.datetime.now().strftime("%m%d%Y_%H:%M:%S.%f")
            obj_name = name +'_' + ts

            self.s3_client.upload_fileobj(
                        r.raw,
                        self.S3_BUCKET_NAME,
                        obj_name
            )
            print(f"'{obj_name}' has been uploaded to '{self.S3_BUCKET_NAME}'")





    def on_request_error(self, status_code):
        logging.error(status_code)

def main(bearer_token, keywords):
    stream = RetweetListener(bearer_token)
    stream.filter(track=keywords, languages=["en"])