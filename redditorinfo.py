import praw
import numpy as np
import time
from datetime import datetime

reddit = praw.Reddit(client_id = "",
                    client_secret = "",
                    user_agent="",
                    username = "",
                    password = "")


# takes in username gather from the URL scrapes.  Can take one of the dictionaries.keys() to get all user names
# This function returns if the reddit user email is varified, gold account, moderator, karma and age of account

# takes list of usernames
def redditor_attributes(reddit_usernames):
    redditor_data = {}
    count = 0

    for name in reddit_usernames:

        try:
            redditor = reddit.redditor(name=name)
            varified_email = redditor.has_verified_email
            gold = redditor.is_gold
            mod = redditor.is_mod
            karma = int(redditor.link_karma) + int(redditor.comment_karma)
            # Calculating Date Time Difference
            a = time.strftime('%m/%d/%Y', time.gmtime(redditor.created_utc))
            b = time.strftime('%m/%d/%Y')
            dates = [a, b]
            dates = [datetime.strptime(x, '%m/%d/%Y') for x in dates]
            diff = dates[0] - dates[1]
            days = abs(diff.days)

            if name not in redditor_data:
                redditor_data.setdefault(name, [])
                redditor_data[name].append([varified_email, gold, mod, karma, days])

            # if count % 50 == 0:
            #     print(count)
            #
            # count += 1
        except:
            continue

    return redditor_data


# Additional function to gather info for EDA on what subreddits users are visiting as well as comments
def redditor_subreddit(redditor_list):
    subreddit_freq_dictionary = {}
    redditor_subreddit_list = []
    subreddit_list = []
    redditor_comments = []
    count = 0
    for name in redditor_list:
        redditor = reddit.redditor(name=name)
        try:
            for comment in redditor.comments.new(limit=50):
                subreddit_list.append(str(comment.subreddit))
                sub_unique = list(np.unique(subreddit_list))
                redditor_comments.append(comment.body)

            for i in sub_unique:
                if i not in subreddit_freq_dictionary:
                    subreddit_freq_dictionary[i] = 1
                else:
                    subreddit_freq_dictionary[i] += 1

            sub_unique.insert(0, name)

        except:
            continue

        subreddit_list = []
        redditor_subreddit_list.append(sub_unique)

    if count % 50 == 0:
        print(count)

    count += 1

    return redditor_subreddit_list, subreddit_freq_dictionary, redditor_comments

