import praw
import pandas as pd
import time
import config

#SQL
import mysql.connector
from sqlalchemy import create_engine


def reddit_object():

    reddit = praw.Reddit(client_id="WKfANfqtJZEuhg",
                         client_secret="ruYIIrAlQYS816YCZQVQ8t7MExQ",
                         user_agent="WKfANfqtJZEuhg",
                         username="Python_integrated",
                         password="Python123")

    return reddit

def scrape_submissions_1000(reddit):
    sub_list = []
    subreddit = reddit.subreddit('appleswap')
    for submission in subreddit.new(limit=100):
        author = str(submission.author)
        dates = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(submission.created_utc))
        permalink = submission.permalink
        text = submission.selftext
        title = submission.title
        pk = submission.id
        direction = submission.link_flair_text

        sub_list.append([pk, dates, title, text, direction, author, permalink])
    df = pd.DataFrame(sub_list, columns=['id', 'date', 'title', 'text', 'direction', 'author', 'link'])

    return df


def new_submissions(df):
    cnx = mysql.connector.connect(
        host = config.host,
        user = config.user,
        password = config.passwd,
        database = config.db_name
    )
    cur = cnx.cursor()
    cur.execute("""SELECT * FROM Submissions.appleswap;""")
    df_sql = pd.DataFrame(cur.fetchall())
    df_sql.columns = [x[0] for x in cur.description]
    df_sql.to_csv('/home/ubuntu/Reddit-Transaction-Analysis/apple_sql_backup.csv')
    new_submission = df[~df['id'].isin(df_sql['id'])]
    new_sub_list = new_submission.values.tolist()
    cur.close()
    cnx.close()
    return new_sub_list, new_submission, df_sql


def sql_submit(new_submission):
    engine = create_engine("mysql+mysqlconnector://{user}:{pw}@{host}/{db}"
                           .format(user=config.user,
                                   pw=config.passwd,
                                   host=config.host,
                                   db=config.db_name))

    # Insert whole DataFrame into MySQL
    new_submission.to_sql('appleswap', con = engine, if_exists = 'append')



reddit = reddit_object()
df = scrape_submissions_1000(reddit)
new_sub_list, new_submission, df_sql = new_submissions(df)
print(new_submission.shape)
sql_submit(new_submission)



