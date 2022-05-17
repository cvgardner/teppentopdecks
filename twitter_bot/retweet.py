#!/usr/bin/env python
# tweepy-bots/bots/favretweet.py

import tweepy
import logging
from config import create_scraper, create_user
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class RetweetListener(tweepy.StreamingClient):
    def __init__(self):
        self.user_api = create_user()
        self.scraper_api = create_scraper()
        self.me = self.user_api.get_me()

        #initialize with rules
        self.add_rules("teppen_deck OR teppendeck")

    def on_tweet(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")

        #retweet
        self.user_api.retweet(tweet.id)

        #check attachments
        if tweet.attachments is not None:
            print(tweet.attachements)

    def on_request_error(self, status_code):
        logging.error(status_code)

def main(bearer_token, keywords):
    stream = RetweetListener(bearer_token)
    stream.filter(track=keywords, languages=["en"])

if __name__ == "__main__":
    main(bearer_token, ["Python", "Tweepy"])