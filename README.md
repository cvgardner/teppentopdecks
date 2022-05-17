# TEPPEN TOP DECKS
Automations for Teppentopdecks.com backend

# TODO
- Containerize Twitter Bot and host it onto an Amazon EC2 instance
- Create Tasks to process all the images from within the twitter-images s3 folder (only save deck images and create some metadata to sort/visualize them by)


### Twitter Bot

Automated Twitter account that retweets when a tweet has both "Teppen" and "deck" mentioned. If there are attached images it will pull them into amazon s3 for later processing. 

### Image Processing Tasks

TODO: Might try to do Amazon Lambda Functions with a scheduler

### Front End for Browsing Decks

TODO: Could try to use Notion API to get something or Python StreamLit

