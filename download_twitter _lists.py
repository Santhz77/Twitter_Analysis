import sys
import config
import tweepy
from tweepy import OAuthHandler


def write_to_file(username):
    with open("tech-company-founders-list.txt", 'a') as f:
        f.write(username + "\n")


# Twitter API Authentication
auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

count = 0




for user in tweepy.Cursor(api.list_members, owner_screen_name="Scobleizer", slug="tech-company-founders").items():
    print(user.screen_name)
    write_to_file(user.screen_name)
    count = count + 1



print(count)