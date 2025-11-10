import tweepy
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv('API_KEY') or os.getenv('CONSUMER_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET') or os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

def authenticate_twitter():
    """Authenticate with Twitter API v1.1"""
    try:
        # OAuth 1.0a authentication
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        
        # Create API object (v1.1)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        
        # Verify credentials
        me = api.verify_credentials()
        print(f"✓ Authenticated as @{me.screen_name}")
        return api
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return None

def search_and_reply(api, hashtag, reply_message, max_tweets=10):
    """
    Search for tweets with hashtag and reply to them
    Using API v1.1 which works with Free tier
    """

    # Add # if not present
  
        
    
    print(f"\nSearching for tweets with {hashtag}...")
    
    # Search tweets (v1.1 endpoint - works with Free tier)
    tweets = api.search_tweets(
        q=hashtag,
        count=max_tweets,
        result_type="recent"
    )
    
    if not tweets:
        print("✗ No tweets found")
        return 0
    
    print(f"✓ Found {len(tweets)} tweets\n")
    
    replied_count = 0
    for tweet in tweets:
        print(f"Tweet by @{tweet.user.screen_name}:")
        print(f"  {tweet.text[:80]}...")
        
        try:
            # Reply to tweet
            api.update_status(
                status=f"@{tweet.user.screen_name} {reply_message}",
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True
            )
            print(f"  ✓ Replied successfully\n")
            replied_count += 1
            time.sleep(2)  # Rate limiting
            
        except tweepy.TweepyException as e:
            if "duplicate" in str(e).lower():
                print(f"  ⚠ Already replied to this tweet\n")
            else:
                print(f"  ✗ Error: {e}\n")
    
    return replied_count
        
  

def main():
    print("=" * 60)
    print("Twitter Bot - Hashtag Reply")
    print("=" * 60)
    
    # Config
    HASHTAG = "something"
    REPLY_MESSAGE = "Thanks for using this hashtag! 🤖"
    MAX_TWEETS = 10
    
    print(f"\nConfig:")
    print(f"  Hashtag: {HASHTAG}")
    print(f"  Reply: {REPLY_MESSAGE}")
    print(f"  Max tweets: {MAX_TWEETS}\n")
    
    # Authenticate
    api = authenticate_twitter()
    if not api:
        print("⚠ Authentication failed")
        return
    
    # Search and reply
    replied = search_and_reply(api, HASHTAG, REPLY_MESSAGE, MAX_TWEETS)
    
    print("=" * 60)
    print(f"Summary: Replied to {replied} tweets")
    print("=" * 60)

if __name__ == "__main__":
    main()

