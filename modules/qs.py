import os
from dotenv import load_dotenv
import tweepy
import time

# Load environment variables
load_dotenv()

BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_KEY = os.getenv('API_KEY') or os.getenv('CONSUMER_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET') or os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# tweepy client for both searching and replying
tweepy_client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def create_post(client, text):
    """Create a new tweet"""
    response = client.create_tweet(text=text)
    return response

def submit_comment(client, text, tweet_id):
    """Reply to a tweet"""
    response = client.create_tweet(
        text=text,
        in_reply_to_tweet_id=tweet_id
    )
    return response

def search_tweets(client, query, max_results=10):
    """Search for recent tweets"""
    response = client.search_recent_tweets(query=query, max_results=max_results)
    return response

# Try to search - if rate limited, will catch and show message

# response = search_tweets(tweepy_client, "api", max_results=5)
# print(response)

# reply = submit_comment(tweepy_client, "This is a test comment! 🤖", "1988232973817442450")
# print(reply)
# try:
#     print("Searching for tweets with 'api' keyword...")
    
    
#     if response.data:
#         print(f"Found {len(response.data)} tweets\n")
#         for post in response.data:
#             print(f"Tweet: {post.text[:60]}...")
#             print(f"ID: {post.id}")
            
#             # Reply to the tweet
#             reply = submit_comment(tweepy_client, "This is a test comment! 🤖", post.id)
#             print(f"✓ Replied with ID: {reply.data['id']}\n")
#             time.sleep(2)  # Rate limit protection
#     else:
#         print("No tweets found.")
        
# except tweepy.errors.TooManyRequests:
#     print("\n⚠️ Rate limit hit! Wait 15 minutes before searching again.")
#     print("Functions are ready to use:\n")
#     print("  - create_post(client, text)")
#     print("  - submit_comment(client, text, tweet_id)")
#     print("  - search_tweets(client, query, max_results=10)")

