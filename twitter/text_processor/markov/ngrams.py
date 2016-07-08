import collections
import random

def generate_ngrams(words, n):
    """ Given a list of words, generate all ngrams possible: each key will be
        a tuple of words n-1 long, and the value will be a list of all words
        following that key in the given words list.
    """
    if isinstance(words, str):
        words = words.split(" ")
    word_dict = collections.defaultdict(list)
    offset = n - 1 ## how many words from the end to stop slicing
    for i in range(len(words) - offset):
        key = tuple(words[i:i+offset])
        value = words[i+offset]
        word_dict[key].append(value)
    return word_dict

def normalize_key(key, word_dict):
    ## pick random dict_key to determine len of ngram (less one)
    key_length = len(next(iter(word_dict)))

    ## allow other types than tuple for key
    if isinstance(key, str):
        key = tuple(key.split(" "))
    elif isinstance(key, list):
        key = tuple(key)

    ## if provided key is short, use it as a starting point
    if key and len(key) < key_length:
        possible_starts = [k for k in word_dict if k[:len(key)] == key]
        if possible_starts:
            key = random.choice(possible_starts)
        else:
            key = None
    elif key not in word_dict:
        key = None

    ## didn't have anything valid to start with, choose randomly
    if key is None:
        key = random.choice([k for k in word_dict.keys()])
    return key

def generate_nonsense(word_dict, n, key=None):
    """ Given a dictionary such as one produced by generate_ngrams(), it will
        produce @n random words of text, by picking a word, and then randomly
        choosing a following word. Returns a list of words
    """
    key = normalize_key(key, word_dict)
    words = list(key)
    for i in range(n-len(words)):
        next_word = random.choice(word_dict[key])
        ## keys need to be tuples, but can't append to tuples so temp-list
        key = tuple(list(key[1:]) + [next_word])
        words.append(next_word)
    return " ".join(words)
