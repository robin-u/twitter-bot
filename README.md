# TWITTER BOT

## Description
The whole point of this script is to use Twitter API, and then forward each DMs that were sent to the account with the keys and tokens that's being used in the script.

## API Endpoints
Essentialy, the purpose of the script is to tweet a dm with the *trigger word*. The Twitter API endpoints that this script uses are:
```
1. GET account/verify_credentials
2. GET direct_messages/events/list
3. POST status/update
4. POST media/upload
5. DELETE direct_messages/events/destroy
```

## Features
The main features of this script are listed below:
1. **Read DM**, and then **tweet DM** that contains a trigger word— limited to 1 tweet/minute to prevent spam and reaching the rate limit.
2. **Quote tweet** can be performed by adding a tweet url in the last part of the dm. Below is the example:
```
This is just a dummy text to tweet <https://twitter.com/<USERNAME>/status/<TWEET ID>>
```
3. The script will automatically **delete DM** that either contains > 280 characters and/or doesn't have the trigger word.

Because the script is still rather simple (and written by a beginner), I would strongly advise for people to write it their own and learn from it. 

And that's why there's no reason for me to explain further how to clone this repo or how to automate it by deploying on a cloud platform.

## Disclaimer
The purpose of this script is just to familiarize myself with Python (OOP in particular and the other things), reading documentations (in this case, Tweepy library and Twitter API) and how to interact with an API. Thus, the script **_is not_** fully tested on edge cases.

## Retrospective
If I were to do this again, I would definitely create a list of features and a *rough* program flow with any API endpoints that I'm gonna be interacting with— the idea is to be more structured, focused and efficient in the programming phase.