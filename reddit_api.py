import praw
import random as rn
import json


def reddit_instance():
    """
    I hid my credentials in a json file, the function won't run with them
    """
    with open('reddit_cred.json') as f:
        cred = json.load(f)
    reddit = praw.Reddit(client_id=cred['client_id'],
                         client_secret=cred['client_secret'],
                         password=cred['password'],
                         redirect_uri=cred['redirect_uri'],
                         user_agent=cred['user_agent'],
                         username=cred['username'])
    return reddit


def get_reddit(sub, when='all'):
    """
    the api is very complicated and the documentation is trash
    I mostly used the dir() function to know what I can do with
    the classes
    """
    reddit = reddit_instance()
    lst = list(reddit.subreddit(sub).top(when))
    submission = rn.choice(lst)
    if submission.is_self:
        return submission.title, submission.shortlink
    else:
        return submission.preview['images'][0]['source']['url'], submission.title, submission.shortlink
