import tweepy
import hidden
import time

class Twbot:
    def __init__(self):
        self.init = tweepy.OAuthHandler(hidden.CONSUMER_KEY, hidden.CONSUMER_SECRET)
        self.init.set_access_token(hidden.TOKEY_KEY, hidden.TOKEY_SECRET)
        self.api = tweepy.API(self.init)
    
    def auth_test(self):
        try:
            self.api.verify_credentials()
            print('Auth OK')
        except Exception as err:
            print(err, 'occured. Re-check the credentials')

    def read_dm(self):
        """ Returns 
        -----------
        `[{sender, message, message_id}]'
        """

        dm = self.api.get_direct_messages()
        dms = list()
        for i in range(len(dm)):
            sender = dm[i].message_create['sender_id']
            message = dm[i].message_create['message_data']['text']
            message_id = dm[i].id
            temp = dict(sender=sender, message=message, message_id=message_id)
            dms.append(temp)
        dms.reverse() # reading from the first person to dm
        return dms
        """ conditional with media """

    def post_tweet(self, tweet):
        self.api.update_status(tweet)
        print('Tweeting...')
        time.sleep(3)
        print('Tweeted!\n')

    def post_tweet_with_media(self, tweet, media):
        self.api.update_status_with_media(tweet, media)
        """ CONTINUE """

    def delete_dm(self, id):
        self.api.delete_direct_message(id)
        print('Deleting DM...')
        time.sleep(3)
        print('DM deleted!\n')

# post tweet > API.update_status()
# post tweet with media > API.update_status_with_media()