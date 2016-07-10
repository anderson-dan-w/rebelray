# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 13:01:27 2016

@author: Ted
"""
import re
import string
def tweet_parse(tweet_txt, nourl=1,noht=1,nouser=1):
    '''Function to turn tweet strings into strings usable by markov
    distribution function'''
    if nourl:
        tweet_txt=re.sub(r"http\S+", "", tweet_txt)
    if noht:
        tweet_txt=re.sub(r"#\S+", "", tweet_txt)
    if nouser:
        tweet_txt=re.sub(r"@\S+", "", tweet_txt)
    #strip punctuation
    exclude = set(string.punctuation)
    tweet_txt = ''.join(ch for ch in tweet_txt if ch not in exclude)
    #fix whitespace
    return ' '.join(tweet_txt.split())
