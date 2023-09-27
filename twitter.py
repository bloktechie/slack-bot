from  twitter_scraper import get_tweets

def get_tweets_from_user(username: str):
  for tweet in get_tweets(username, pages = 1):
    print(tweet['text'])

get_tweets_from_user('twiitter')