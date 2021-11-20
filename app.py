from bot import Twbot
import time

tw = Twbot()
credential_check = tw.auth_test() # to check if the credentials is valid

def start():
    """ Trigger word is "ftw!" """
    trigger_word = 'ftw!'
    while True:
        messages = tw.read_dm()
        try:
            dm = messages[0]['message']
            dm_id = messages[0]['message_id']
            media_id = messages[0]['media_id']
            media_url = messages[0]['media_url']
            media_short_url = messages[0]['short_url']
            media_type = messages[0]['media_type']
        except:
            print("Currently, there's no dm")
            time.sleep(120)
            continue
        
        # Check if the length is <= 280 and if there's trigger word
        if len(dm) <= 280 and trigger_word in dm:
            # Tweets if there's no media id and media type
            if media_id is None and media_type is None:
                print("DM doesn't have any media...")
                tw.post_tweet(dm)
                tw.delete_dm(dm_id)
                time.sleep(60)
            # Delete the DM because it has invalid attachment (gif or video)
            elif media_id is None and media_type != 'photo':
                print("File is not a photo. File type is %s. Please, attach a photo" % (media_type))
                print("Wrong attachment type. Will delete DM")
                tw.delete_dm(dm_id)
                time.sleep(60)
            else:
                print("DM has a media attached...")
                # Uploading media
                media_ids = list()
                media_ids.append(tw.upload_image(media_url))

                # Tweets
                dm = dm.replace(media_short_url, '')
                tw.post_tweet_with_media(dm, media_ids[:], media_short_url)
                tw.delete_dm(dm_id)
                print("Restarting the script")
                time.sleep(60)
        else:
            if len(dm) > 280:
                print("DM will be deleted. It's longer than 280 char")
            elif trigger_word not in dm:
                print("DM will be deleted. It don't have the trigger word")
            else:
                print("DM will be deleted. The sent dm doesn't follow the rules")
            tw.delete_dm(dm_id)
            print("Restarting the script")
            time.sleep(60)
        messages = list() # resets the dms in messages var

if credential_check and __name__ == '__main__':
    start()