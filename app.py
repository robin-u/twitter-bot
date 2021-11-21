from bot import Twbot
import time
import sqlite3 # Comment this line out if you don't want to store sender id and the dm sent

# Creating the twitter/tw object
tw = Twbot()
credential_check = tw.auth_test() # to check if the credentials is valid

# Creating DB
try: 
    con = sqlite3.connect('senders.sqlite')
    cur = con.cursor()

    # Creating table with the attribute of sender_id and sent_dm
    # There's no primary key or unique constraint, as the db is just intended to store sender id and the dm
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Message (
        sender_id INT NOT NULL,
        sent_dm VARCHAR(280)
    );  
    ''')
except:
    pass

def start():
    """ Trigger word is "word!" """
    trigger_word = 'word!'
    while True:
        messages = tw.read_dm()
        try:
            sender_id = messages[0]['sender']
            dm = messages[0]['message']
            dm_id = messages[0]['message_id']
            media_id = messages[0]['media_id']
            media_url = messages[0]['media_url']
            media_short_url = messages[0]['short_url']
            media_type = messages[0]['media_type']
        except:
            print("Currently, there's no dm. Waiting for a new DM")
            print('-'*50 + '\n')
            time.sleep(90)
            continue
        
        # Check if the length is <= 280 and if there's trigger word
        if len(dm) <= 280 and trigger_word in dm:
            # Tweets if there's no media id and media type
            if media_id is None and media_type is None:
                print("There's a DM! The DM doesn't have any media. Will be tweeted soon~")
                try:
                    tw.post_tweet(dm)
                    # Storing the sender id
                    cur.execute(''' INSERT INTO Message VALUES (?, ?)''', (sender_id, dm))
                    con.commit()
                except:
                    print("This a duplicate of the same dm that just got tweeted. This dm will be deleted")
                    pass
                tw.delete_dm(dm_id)
            # Delete the DM because it has invalid attachment (gif or video)
            elif media_id is None and media_type != 'photo':
                print("File is not a photo. File type is %s. Please, attach a photo" % (media_type))
                print("Wrong attachment type. Will delete DM")
                tw.delete_dm(dm_id)
            else:
                print("There's a DM! The DM has a media attached...")
                # Uploading media
                media_ids = list()
                media_ids.append(tw.upload_image(media_url))

                # Tweets
                dm = dm.replace(media_short_url, '')
                try:
                    tw.post_tweet_with_media(dm, media_ids[:], media_short_url)
                    # Storing the sender id
                    cur.execute(''' INSERT INTO Message VALUES (?, ?)''', (sender_id, dm))
                    con.commit()
                except:
                    print("This a duplicate of the same dm that just got tweeted. This dm will be deleted")
                    pass
                tw.delete_dm(dm_id)
        else:
            if len(dm) > 280:
                print("DM will be deleted. It's longer than 280 char. Instead, screenshot the dm and send it again.")
            elif trigger_word not in dm:
                print("DM will be deleted. It don't have the trigger word")
            else:
                print("DM will be deleted. The sent dm doesn't follow the rules")
            tw.delete_dm(dm_id)
        messages = list() # resets the dms in messages var

if credential_check and __name__ == '__main__':
    start()