import praw
import re
import json
import numpy as np
import pandas as pd
from copy import deepcopy
import pickle
#Account Age
import time
from datetime import datetime

reddit = praw.Reddit(client_id = "",
                    client_secret = "",
                    user_agent="",
                    username = "",
                    password = "")

# Below lists are used to determine who the buyer / seller was in a transaction
# Not a perfect system, but based on tests i ran it was picking up about 96% of the transactions correctly
buying_verbs = ['Bought', 'Boguht','bought', 'Bougth', 'Purchased',
                'brought', 'Purchase', 'purchased', 'Received',
                'received', 'Recieved', 'recieved' ]
selling_vergs = ['Gave', 'Sale', 'Sold', 'sold', 'Sold/Delivered']
traded = ['Trade', 'Traded']

# Gets the last 72 confirmed trade threads from hardwareswaps
# manually removed the oldest 5 as they were causing issues
subreddit = reddit.subreddit('hardwareswap')
url_list = []
for i in subreddit.search("confirmed trade thread", limit=72):
    url_list.append(i.url)

# to allow the list to scrape from oldest to newest
url_list = url_list[::-1]

relationships = {}
relationship_text = {}
user_grade = {}
# This function takes in the confirmed trade thread urls and calls the reddit API to get all of the comments from those
# threads.  From those Threads this Function grabs user grade, who transacted with who and what was transacted
# Scraping all confirmed trade threads will take roughly 18-20 hours with praw limitations
def grab_transactions_final(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)

    for comment in submission.comments.list():
        try:
            parent = str(comment.author)
            body_text = str(comment.body)
            flair_class = str(comment.author_flair_css_class)
            flair_text = str(comment.author_flair_text)

            if parent not in relationships and parent != 'None':
                relationships.setdefault(parent, [])
            # searches for a username in the comment to determine who transacted with who
            if re.search(r"u\/[A-Za-z0-9_-]+", body_text):
                child = re.search(r"u\/[A-Za-z0-9_-]+", body_text)
                if str(child.group()[2:]) != 'hwsbot':
                    relationships[parent].append([child.group()[2:], body_text])

            if parent not in relationship_text and parent != 'None':
                relationship_text.setdefault(parent, [])

            if re.search(r"u\/[A-Za-z0-9_-]+", body_text):
                child = re.search(r"u\/[A-Za-z0-9_-]+", body_text)
                if str(child.group()[2:]) != 'hwsbot':
                    relationship_text[parent].append([child.group()[2:], body_text])
            # adds user grade to dictionary of users, User grade is stored in the attribute flair_class
            if parent not in user_grade and parent != 'None':
                user_grade.setdefault(parent, [])
                user_grade[parent].append(flair_class)
                user_grade[parent].append(flair_text)
        except:
            continue

    # If the user has more then one post this will remove duplicate entries in the list for grade and Trades
    for key in user_grade.keys():
        try:
            if user_grade[key] != []:
                user_grade[key] = user_grade[key][0:2]
            else:
                user_grade[key] = []
        except:
            continue
    # removes hwsbot from the dictionary
    if 'hwsbot' in user_grade:
        del user_grade['hwsbot']
    # determines the buyer / seller in a trade.
    for user in relationships.keys():
        try:
            for trade in relationships[user]:
                if any(word in trade[1] for word in buying_verbs):
                    trade[1] = 'bought'
                elif any(word in trade[1] for word in selling_vergs):
                    trade[1] = 'sold'
                elif any(word in trade[1] for word in traded):
                    trade[1] = 'traded'
                else:
                    trade[1] = 'ambigious'
        except:
            continue

    return relationships, relationship_text, user_grade

# scrapes all of the data from the confirmed trade threads
def all_data(url_list):
    for url in url_list:
        relationships, relationship_text, user_grade = grab_transactions_final(url)
        print(time.strftime('%H:%M:%S'))
    return relationships, relationship_text, user_grade

# example all_data() call below
# relationships, relationship_text, user_grade = all_data()


