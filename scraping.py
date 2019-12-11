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

# Gets the last 72 confirmed trade threads from hardwareswaps
subreddit = reddit.subreddit('hardwareswap')
url_list = []
for i in subreddit.search("confirmed trade thread", limit=72):
    url_list.append(i.url)

