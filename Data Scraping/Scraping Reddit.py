'''
Scrape Reddit WallStreetBets from March 2022 to March 2023
'''
import praw
from datetime import datetime as dt
import pandas as pd


# Reddit API credentials (id and password are intentionally deleted!)
reddit= praw.Reddit(client_id = '',
                              client_secret = '',
                              user_agent = 'yuting17')


# Specify the subreddit
subreddit = reddit.subreddit('wallstreetbets')
keywords = ['inflation', 'interest rate', 'unemployment rate', 'forecast', 'recession']

# List to store posts
list_post = []

for keyword in keywords:
    for submission in subreddit.search(keyword,  limit=None):
        if not submission.stickied:
            list_post.append((submission, keyword))

# Create a DataFrame
df_data = []

for submission, keyword in list_post:
    df_data.append({
        'id_str': submission.id,
        'user.id_str': submission.author_fullname,
        'subreddit': submission.subreddit.display_name,
        'title': submission.title,
        'selftext': submission.selftext,
        'text': submission.title + submission.selftext,
        'created_at': dt.utcfromtimestamp(submission.created_utc),
        'upvote_ratio': submission.upvote_ratio,
        'ups': submission.ups,
        'downs': submission.downs,
        'score': submission.score,
        'permalink': 'https://www.reddit.com' + submission.permalink,
        'num_comments': submission.num_comments,
        'keyword': keyword,
        'source': 'reddit'
    })

df = pd.DataFrame(df_data)
df.to_excel("scraped_reddit_data.xlsx", index=False)
