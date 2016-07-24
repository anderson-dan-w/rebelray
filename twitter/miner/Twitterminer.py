# -*- coding: utf-8 -*-
"""
Twitter miner
"""

import os
import json
import twitter

auth_path = os.path.join(os.path.dirname(__file__), "twitter_auth")
auth_json = json.load(open(auth_path))

auth = twitter.oauth.OAuth(**auth_json)
twitter_api = twitter.Twitter(auth=auth)

MAX_REQUESTS_PER_15_MIN = 180
def get_tweets_for(user, ntweets=200, max_id=None, since_id=None):
    """ Return about @ntweets for a specified user, prior to max_id if provided
        and after since_id if provided.
        If @user is malformed, raises TwitterHTTPError.
        I say "about ntweets" because calls to user_timeline counts retweets
            before filtering, so it usually overshoots by 0 < x < 200.
        Short results may be a factor of rate-limiting; since the function
            runs quickly enough, we limit by the reqs-per-15-min limit.
    """
    params = {}
    if max_id:
        params['max_id'] = max_id
    if since_id:
        params['since_id'] = since_id
    user_tweets, iters = [], 0
    while len(user_tweets) < ntweets and iters < MAX_REQUESTS_PER_15_MIN:
        nrequested = min(200, ntweets - len(user_tweets))
        tweets = twitter_api.statuses.user_timeline(screen_name=user,
                count=nrequested, include_rts=0, **params)
        user_tweets.extend(tweets)
        iters += 1
        if len(tweets) ==  0:
            ## got no results: maybe hit limit, or ran out of tweets, or error
            break
        params['max_id'] = tweets[-1]['id']
    return user_tweets

def get_trump_tweets(nreqs=180, max_id=None, since_id=None):
    """Gets tweets from Donald Trump, asking for the maximum of 200 tweets each
    time. nreqs specifies the number of requests to make, up to a max of 180. 
    180 is the number of requests allowable by API every 15 minutes with 
    current auth type. Excludes retweets, but includes replies. Returns a tuple
    containing a list of the tweets returned and the id of the last retrieved 
    tweet.
    """
    params = {}
    if max_id:
        params['max_id'] = max_id
    if since_id:
        params['since_id'] = since_id
    user_tweets, iters = [], 0
    nreqs = min(180,nreqs)
    while iters < nreqs:
        tweets = twitter_api.statuses.user_timeline(screen_name='realDonaldTrump',
                count=200, include_rts=0, **params)
        user_tweets.extend(tweets)
        iters += 1
        if len(tweets) ==  0:
            ## got no results: maybe hit limit, or ran out of tweets, or error
            break
        params['max_id'] = tweets[-1]['id']
    return (user_tweets,max_id)
    
## to create database of tweets:
## note, doesn't probably directly, but encoding some knowledge
def fill_db():
    tweets = get_trump_tweets()
    from data_processor import storer as Storer
    for tweet in tweets:
        ## for some reason dan doesn't understand, this not only stores the
        ## entities, it also stores the tweeter and the tweet
        Storer.store_entity(tweet)
        ## NB this may take a while - something like 3000-4000 tweets

## to generate ngrams/nonsense
## note, doesn't probably directly, but encoding some knowledge
def get_trump_nonsense(run_fill_db=False):
    if run_fill_db:
        fill_db()
    from data_controller import storer as Storer
    from text_processor.markov import ngrams
    from data_controller import db_setup as DB
    session, _ = DB.get_session()
    tweets = (t.text for t in session.query(Storer.Tweet).all())
    ndict = ngrams.generate_all_ngrams(tweets, 3) ## or however many words
    print(ngrams.generate_nonsense(ndict, 20))