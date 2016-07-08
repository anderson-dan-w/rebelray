from data_controller import db_setup
from data_controller.tables.tweeter_mapper import Tweeter
from data_controller.tables.tweet_mapper import Tweet
from data_controller.tables.entity_mapper import Entity

import datetime
try:
    from dateutil.parser import parse as dateparse
except ImportError:
    print("Can you get dateutil? I got it with: "
          "sudo apt-get install python3-dateutil ...")
    def dateparse(date_str):
        ## isn't this gross? god forbid it changes... go get dateutil
        ## Sun Jan 01 16:45:51 +0000 2015
        date_fmt = "%a %b %d %H:%M:%S %z %Y"
        return datetime.datetime.strptime(date_str, date_fmt)

def format_tweeter(tweet):
    t = dict( name = tweet['user']['name'],
              twitter_handle = tweet['user']['screen_name'],
              user_id = tweet['user']['id'],
              max_tweet_id = tweet['id'],
              min_tweet_id = tweet['id'] )
    return Tweeter(**t)

def format_tweet(tweet, tweeter_db_id):
    t = dict( text = tweet['text'],
              created_at = dateparse(tweet['created_at']),
              favorite_counts = tweet['favorite_count'],
              retweet_counts = tweet['retweet_count'],
              tweeter_id = tweeter_db_id )
    return Tweet(**t)

def format_entities(tweet, tweet_db_id):
    entities = []
    for entity_type, entity_list in tweet['entities'].items():
        for entry in entity_list:
            start, end = entry['indices']
            e = {'entity': entity_type,
                 'starting_index': start,
                 'ending_index': end,
                 'tweet_id': tweet_db_id }
            if entity_type == 'urls':
                e['text'] = entry['url']
            elif entity_type == 'user_mentions':
                e['text'] = entry['screen_name']
            elif entity_type in ('hashtags', 'symbols'):
                e['text'] = entry['text']
            entities.append(Entity(**e))
    return entities

