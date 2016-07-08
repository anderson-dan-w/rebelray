## so, why didn't all of this just go directly into the mapper/table files?
## because I don't get sqlalchemy well-enough yet. The issue is:
## I can't use the get_session() function until sessionmaker has been bound
##   and I can't bind sessionmaker until after all the tables have been created
##   with Base. So I do that almost-circular-import in db_setup.py, then I make
##   that the first import here, so now everything works happily

## NB2: I'm SUPER confused by how this is working, because when I try to load
##   in new tweets/entities, it somehow goes to the 'Already have...' line.
##   My thought is that python/sqlalchemy is SO SMART, that when I attach the
##   existing parent to the new object (entity.tweet = tweet, eg), it updates
##   the tables (though doesn't commit them until told to do so, of course).
##   I really just don't know. This might be 'cascade'?

from data_controller import db_setup
from data_controller import formatters
from data_controller.tables.tweeter_mapper import Tweeter
from data_controller.tables.tweet_mapper import Tweet
from data_controller.tables.entity_mapper import Entity

def store_tweeter(tweet_json, session=None):
    session, isSessionLocal = db_setup.get_session(session)

    tweeter = formatters.format_tweeter(tweet_json)
    haveTweeter = (session.query(Tweeter)
                          .filter_by(twitter_handle=tweeter.twitter_handle)
                          .first())
    if haveTweeter:
        print("Already have user {}".format(haveTweeter.twitter_handle))
        tweeter = haveTweeter
    else:
        print("Going to store user {}".format(tweeter.twitter_handle))
        session.add(tweeter)
    print()

    ## @TODO: this will commit all local sessions whether or not there's
    ## a change to commit. Does that matter? Is it smart enough to not bother?
    ## or does it also need a isSessionAltered attribute?
    if isSessionLocal:
        session.commit()
    return tweeter

def store_tweet(tweet_json, session=None):
    session, isSessionLocal = db_setup.get_session(session)
    isSessionLocal = False
    if session is None:
        session = Session()
        isSessionLocal = True
    ## first get the tweeter's database ID (so, store if we need to)
    ## @TODO: maybe the cascade does this for us? I'm not sure...
    tweeter = store_tweeter(tweet_json, session)
    tweet = formatters.format_tweet(tweet_json, tweeter.id)
    tweet.tweeter = tweeter

    ## check for duplication
    haveTweet = (session.query(Tweet)
                        .filter_by(text=tweet.text)
                        .filter_by(tweeter_id=tweeter.id)
                        .first())
    if haveTweet:
        print("Already have tweet {} by user {}".format(haveTweet.text,
                haveTweet.tweeter_id))
        tweet = haveTweet
    else:
        print("Going to store tweet {}".format(tweet.text))
        session.add(tweet)
    print()

    if tweet_json['id'] > tweeter.max_tweet_id:
        tweeter.max_tweet_id = tweet_json['id']
        session.add(tweeter)
    elif tweet_json['id'] < tweeter.min_tweet_id:
        tweeter.min_tweet_id = tweet_json['id']
        session.add(tweeter)

    if isSessionLocal:
        session.commit()
    return tweet


def store_entities(tweet_json, session=None):
    session, isSessionLocal = db_setup.get_session(session)

    ## @TODO: this may be taken care of by cascade? not sure...
    tweet = store_tweet(tweet_json, session)

    entities = formatters.format_entities(tweet_json, tweet.id)
    entitiesToAdd = []
    for entity in entities:
        entity.tweet = tweet
        haveEntity = (session.query(Entity)
                             .filter_by(tweet_id=entity.tweet_id)
                             .filter_by(starting_index=entity.starting_index)
                             .first())
        if haveEntity:
            print("Already have entity {} in tweet {}"
                  .format(haveEntity.text, haveEntity.tweet.text))
            entity = haveEntity
        else:
            print("Storing entity {} for tweet {}"
                  .format(entity.text, tweet.text))
            entitiesToAdd.append(entity)
        print()

    if entitiesToAdd:
        session.add_all(entitiesToAdd)
    if isSessionLocal == True:
        session.commit()

