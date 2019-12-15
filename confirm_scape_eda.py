import praw


reddit = praw.Reddit(client_id = "",
                    client_secret = "",
                    user_agent="",
                    username = "",
                    password = "")

#72 months
def confirm_urls():
    url_list = []
    # sets subreddit to hardwareswap to specifically search r/hardwareswap
    subreddit = reddit.subreddit('hardwareswap')
        # appends the url for each search result to url_list by using the argument .url
    for i in subreddit.search("confirmed trade thread", limit=72):
        url_list.append(i.url)
    # reverse the list so the URL's are from oldest to newest
    url_list = url_list[::-1]
    return url_list


#example call
url_list = confirm_urls()
