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
        params['max_id'] = tweets[-1]['id']
    return (user_tweets,max_id)