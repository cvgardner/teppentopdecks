#!/usr/bin/env python
# tweepy-bots/bots/favretweet.py

import tweepy
import logging
from config import create_scraper, create_user
import json
import boto3
import requests
import datetime
import mimetypes
import os
import ast


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class RetweetListener(tweepy.StreamingClient):
    def configure(self):
        self.user_api = create_user()
        self.scraper_api = create_scraper()
        self.author_id = '1526272248964849665'
        #self.me = self.user_api.get_me()

        #initialize with rules
        query = "teppen deck OR deck from:PlayTeppen"
        rule1 = tweepy.StreamRule(query)
        self.add_rules(rule1)

        #aws setup
        self.setup_aws()

    def setup_aws(self):
        #initialize AWS
        self.AWS_REGION = "us-east-1"
        self.S3_BUCKET_NAME = "teppentopdecks"
        self.s3_client = boto3.client("s3", region_name=self.AWS_REGION)

    def on_data(self, raw_data):
        tweet = ast.literal_eval(raw_data.decode("UTF-8"))
        tweet_id = tweet.get('data').get('id')
        logger.info(f"Processing Tweet ID {tweet_id}" )
        
        logging.info("Checking if we authored this tweet")
        if tweet.get('data').get('author_id') == self.author_id:
            logging.info("This is our tweet. Skipping.")
            return

        has_photo = False

        #check attachments
        if tweet.get('includes').get('media'):
            #loop over media
            for media in tweet.get('includes').get('media'):
                if media.get('type') == 'photo':
                    has_photo=True

                    #fetch image from url
                    url = media.get('url')
                    r = requests.get(url, stream=True)

                    #create file name
                    content_type = r.headers['content-type']
                    extension = mimetypes.guess_extension(content_type)

                    obj_name = url.split('/')[-1].split('.')[0] + extension
                    logging.info(f"Uploading {obj_name} to s3.")
                    #check if file exists
                    result = self.s3_client.list_objects_v2(Bucket=self.S3_BUCKET_NAME, Prefix=obj_name)
                    if result.get('KeyCount') > 0:
                        logger.info("File Already Exists")
                    else:
                        self.s3_client.upload_fileobj(
                                    r.raw,
                                    self.S3_BUCKET_NAME,
                                    obj_name
                        )
                        logger.info(f"'{obj_name}' has been uploaded to '{self.S3_BUCKET_NAME}'")
        
        #retweet if photo
        if has_photo:
            logging.info("Retweeting from TeppenTopDecks account")
            self.user_api.retweet(tweet_id)
        else:
            logging.info("Tweet did not have photo attached")


    def on_request_error(self, status_code):
        logging.error(status_code)

def main():
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    listener = RetweetListener(bearer_token)
    listener.configure()
    tweet_fields = ['author_id',
              'context_annotations', 
              'created_at', 
              'attachments',
              'entities']
    expansions = ['author_id', 'attachments.media_keys']
    media_fields = ['preview_image_url','url']
    listener.filter(
            tweet_fields=tweet_fields,
            expansions=expansions,
            media_fields=media_fields
    )
