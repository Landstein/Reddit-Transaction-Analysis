import praw
import numpy as np

reddit = praw.Reddit(client_id = "",
                    client_secret = "",
                    user_agent="",
                    username = "",
                    password = "")

# HWS ban list
url = 'https://www.reddit.com/r/hardwareswap/wiki/banlist?utm_source=reddit&utm_medium=usertext&utm_name=hardwareswap&utm_content=t5_2skrs'


# Pulls content of HWS ban page
wikipage = reddit.subreddit('hardwareswap').wiki['banlist']
print(wikipage.content_html)

# Gets the usernames of scammers on the wikipage
def api_scammers():
    scammer_list = []
    scammer = ''

    wikipage = reddit.subreddit('hardwareswap').wiki['banlist']
    ban_list = wikipage.content_md.split('*')

    for scammer_text in ban_list[1:]:
        if re.search(r"u\/[A-Za-z0-9_-]+", str(scammer_text)):
            scammer = re.search(r"u\/[A-Za-z0-9_-]+", str(scammer_text))

        scammer_list.append(scammer.group()[2:])

    return scammer_list


# Will check the wiki page for new scammers by comparing to the old list from the above function
def new_scammers_test(scammers_old):
    scammer_list = []
    scammer = ''

    wikipage = reddit.subreddit('hardwareswap').wiki['banlist']
    ban_list = wikipage.content_md.split('*')

    for scammer_text in ban_list[1:]:
        if re.search(r"u\/[A-Za-z0-9_-]+", str(scammer_text)):
            scammer = re.search(r"u\/[A-Za-z0-9_-]+", str(scammer_text))

        scammer_list.append(scammer.group()[2:])

    if set(scammers_old) != set(scammer_list):
        diff = set(scammers_old) - set(scammer_list)
        return diff
    else:
        return False


# Grabs Scammer Attributes
def scammer_attributes(reddit_usernames):
    redditor_data = {}
    count = 0
    temp_list = []
    subreddit_freq_dictionary = {}

    for name in reddit_usernames:

        try:
            redditor = reddit.redditor(name=name)
            trophy = redditor.trophies()
            varified_email = redditor.has_verified_email
            mod = redditor.is_mod
            gold = redditor.is_gold
            karma = int(redditor.link_karma) + int(redditor.comment_karma)
            reddit_employee = redditor.is_employee
            # Calculating Date Time Difference
            for comment in redditor.comments.new(limit=1):
                a = time.strftime('%m/%d/%Y', time.gmtime(comment.created))
                b = time.strftime('%m/%d/%Y', time.gmtime(redditor.created_utc))
                dates = [a, b]
                dates = [datetime.strptime(x, '%m/%d/%Y') for x in dates]
                diff = dates[0] - dates[1]
                days = abs(diff.days)

            for comment in redditor.comments.new(limit=100):
                temp_list.append(comment.body)

            list_len = len(temp_list)
            temp_list = []

            if name not in redditor_data:
                redditor_data.setdefault(name, [])
                redditor_data[name].append([varified_email, gold, mod, karma, days, list_len])

            if count % 50 == 0:
                print(count)

            count += 1
        except:
            continue

    return redditor_data


# From 50 comments get a unique list of subreddits the scammer was participating in
# scammer_subreddits can be used to gather comments for NLP as well as subreddits visited for EDA or potentially
# more features in the logistic regression model
def scammer_subreddit(scammer_list):
    subreddit_freq_dictionary = {}
    scammer_subreddit_list = []
    subreddit_list = []
    scammer_comments = []
    count = 0
    for name in scammer_list:
        redditor = reddit.redditor(name=name)
        try:
            for comment in redditor.comments.new(limit=50):
                subreddit_list.append(str(comment.subreddit))
                sub_unique = list(np.unique(subreddit_list))
                scammer_comments.append(comment.body)

            for i in sub_unique:
                if i not in subreddit_freq_dictionary:
                    subreddit_freq_dictionary[i] = 1
                else:
                    subreddit_freq_dictionary[i] += 1

            sub_unique.insert(0, name)

        except:
            continue

        subreddit_list = []
        scammer_subreddit_list.append(sub_unique)

    if count % 50 == 0:
        print(count)

        count += 1

    return scammer_subreddit_list, subreddit_freq_dictionary, scammer_comments
