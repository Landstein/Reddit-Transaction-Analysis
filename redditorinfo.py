import praw

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
            gold = redditor.is_mod
            mod = redditor.is_gold
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
