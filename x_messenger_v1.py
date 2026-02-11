
import os
import requests
from requests_oauthlib import OAuth1

# Credentials (from environment or replace with actual keys for one-time run)
consumer_key = os.environ.get("X_CONSUMER_KEY")
consumer_secret = os.environ.get("X_CONSUMER_SECRET")
access_token = os.environ.get("X_ACCESS_TOKEN")
access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

def post_tweet(text):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    payload = {"text": text}
    response = requests.post(url, auth=auth, json=payload)
    if response.status_code == 201:
        print(f"Success! Tweet ID: {response.json()['data']['id']}")
        return response.json()['data']['id']
    else:
        print(f"Failed: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        post_tweet(sys.argv[1])
