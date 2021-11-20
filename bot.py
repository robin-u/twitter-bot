import tweepy
import hidden
import time
import requests
from requests_oauthlib import OAuth1
import os
import re

class Twbot:
    def __init__(self):
        self.init = tweepy.OAuthHandler(hidden.CONSUMER_KEY, hidden.CONSUMER_SECRET)
        self.init.set_access_token(hidden.TOKEN_KEY, hidden.TOKEN_SECRET)
        self.api = tweepy.API(self.init)
    
    # Testing if the key is valid or not
    def auth_test(self):
        try:
            a = self.api.verify_credentials()
            return True
        except tweepy.errors.TweepyException as err:
            print(err, "occured. Re-check the credentials")

    # Reading through DM
    def read_dm(self):
        """ Returns https://ton.twitter.com/1.1/ton/data/dm/1461612025017110532/1461611503707045889/Hg6Ziu5X.jpg
        -----------
        `[{sender, message, message_id, media_id, media_url, short_url, media_type}]`
        """
        dm = self.api.get_direct_messages()
        dms = list()
        for i in range(len(dm)):
            sender = dm[i].message_create['sender_id']
            message_data = dm[i].message_create['message_data']
            message = message_data['text']
            message_id = dm[i].id
            if 'attachment' not in message_data:
                temp = dict(sender=sender, message=message, message_id=message_id, media_id=None, media_url=None, short_url=None, media_type=None)
                dms.append(temp)

            else:
                attachment_type = dm[i].message_create['message_data']['attachment']['media']['type']
                attachment_id = dm[i].message_create['message_data']['attachment']['media']['id']
                attachment_url = dm[i].message_create['message_data']['attachment']['media']['media_url']
                attachment_short_url = dm[i].message_create['message_data']['attachment']['media']['url']
                
                if attachment_type != 'photo':
                    temp = dict(sender=sender, message=message, message_id=message_id, media_id=None, media_url=None, short_url=None, media_type=attachment_type)
                    dms.append(temp)
                else:
                    media_type = attachment_url.split('.')[-1]
                    temp = dict(sender=sender, message=message, message_id=message_id, media_id=attachment_id, media_url=attachment_url, short_url=attachment_short_url, media_type=attachment_type)
                    dms.append(temp)
        dms.reverse() # Reading from the oldest dm
        return dms
    
    # Checking if there's an url_attachment
    # Tweeting tweet (text-only)
    def post_tweet(self, tweet):
        # Checks if there's the regex pattern in dm (for QRT purposes)
        try:
            if re.search(r'https://twitter.com/.+/\d+', tweet).group() in tweet:
                url = re.search(r'https://twitter.com/.+/\d+', tweet).group()
            self.api.update_status(tweet, attachment_url=url)
        except:
            self.api.update_status(tweet)

        print("Tweeting...")
        time.sleep(3)
        print("Tweeted!")

    # Uploading image to tweet
    def upload_image(self, media_url):
        try:
            # Authorization for accessing DM's media url
            oauth = OAuth1(client_key=hidden.CONSUMER_KEY, 
                            client_secret=hidden.CONSUMER_SECRET, 
                            resource_owner_key=hidden.TOKEN_KEY, 
                            resource_owner_secret=hidden.TOKEN_SECRET)

            # Requesting access
            r = requests.get(media_url, auth=oauth)
            
            # Getting the attachment file
            filename = media_url.split('/')[-1]
            with open(filename, 'wb') as f:
                f.write(r.content)
            
            # uploading the file
            media_ids = self.api.media_upload(filename).media_id
            os.remove(filename)
            return media_ids
        except tweepy.errors.TweepyException as err:
            print(err)
            pass

    # Tweeting tweet with media
    def post_tweet_with_media(self, tweet, media_id, media_short_url):
        tweet = tweet.replace(media_short_url, '')
        try:
            if re.search(r'https://twitter.com/.+/\d+', tweet).group() in tweet:
                url = re.search(r'https://twitter.com/.+/\d+', tweet).group()
            self.api.update_status(tweet, media_ids=media_id, attachment_url=url)
        except:
            self.api.update_status(tweet, media_ids=media_id)
        print("Tweeting with attachment(s)...")
        time.sleep(3)
        print("Tweeted with attachment(s)!")

    # Deleting tweet
    def delete_dm(self, id):
        self.api.delete_direct_message(id)
        print("Deleting DM...")
        time.sleep(3)
        print("""DM deleted!
Restarting the script...
{}
""".format('-'*50))
        time.sleep(60)