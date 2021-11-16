from bot import Twbot
import time

tw = Twbot()
# tw.auth_test() # to check if the credentials is valid

def start():
    while True:
        # read the dm
        messages = tw.read_dm()
        try:
            dm = messages[0]['message']
            dm_id = messages[0]['message_id']
        except:
            print('Currently, there\'s no dm')
            time.sleep(60)
            continue

        # post the dm
        if 'hello' in dm.lower():
            tw.post_tweet(dm)
            time.sleep(5)

        # delete the posted dm
        tw.delete_dm(dm_id)
        time.sleep(30)
        
if __name__ == '__main__':
    start()