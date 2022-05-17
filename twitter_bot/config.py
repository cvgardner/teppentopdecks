# tweepy-bots/bots/config.py
import tweepy
import logging
import os

logger = logging.getLogger()

def create_user():    
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    user_api = tweepy.Client(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
    )
    logger.info("API User created")
    return user_api

def create_scraper():
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    scraper_api = tweepy.Client(bearer_token)

    logger.info("API Bot created")
    return scraper_api

def test():
    scraper_api = create_scraper()

    query = "teppen deck OR deck from:PlayTeppen"
    tweet_fields = ['author_id',
              'context_annotations', 
              'created_at', 
              'attachments',
              'entities']
    expansions = ['author_id', 'attachments.media_keys']
    media_fields = ['preview_image_url','url']
    tweets = scraper_api.search_recent_tweets(query=query,
                                expansions=expansions,
                                tweet_fields=tweet_fields,
                                media_fields=media_fields,
                                max_results=100)
    for tweet in tweets.data:
        #print(tweet.text)
        if tweet.attachments is not None:
            print(tweet.attachments)