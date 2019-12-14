
import pandas as pd
import praw
import re
import time


reddit = praw.Reddit(client_id = "",
                    client_secret = "",
                    user_agent="",
                    username = "",
                    password = "")

def estimate_prices():
    prices = []
    price = ''
    price_final = []
    average_price = 0
    for comment in reddit.subreddit('hardwareswap').hot(limit=1000):
        #     print(comment.link_flair_css_class)

        if str(comment.link_flair_css_class) == 'closed':
            #             print(comment.url)
            body = str(comment.selftext)
            price = re.search(r'[\$\£\€](\d+(?:\.\d{1,2})?)', body) or re.search(r'[0-9]+', body)
            if price != None:
                prices.append([price.group(), time.strftime('%m/%d/%Y', time.gmtime(comment.created)), comment.url])

    for i in prices:
        if i[0][0] == '$':
            price = float(i[0][1:])
            price_final.append([price, i[1], i[2]])

    df = pd.DataFrame(price_final, columns=['price', 'date', 'url'])
    average_price = round(df['price'].mean(), 2)
    old = df['date'].min()
    new = df['date'].max()
    print(f'The estimated average price is {average_price} for posts closed between {old} and {new}')
    return df


df = estimate_prices()
print(df.head())
