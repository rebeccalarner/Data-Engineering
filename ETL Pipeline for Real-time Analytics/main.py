from dotenv import load_dotenv
import os
import tweepy

load_dotenv()

bearer_token = os.getenv("BEARER_TOKEN")

streaming_client = tweepy.StreamingClient(bearer_token)

sample = streaming_client.sample()


print(sample)