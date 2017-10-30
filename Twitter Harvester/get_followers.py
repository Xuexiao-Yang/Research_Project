import tweepy
from tweepy import OAuthHandler
import time
import json

from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key = 'q8fS8K*****'
consumer_secret = 'Ca8C****'
access_token = '8574905***'
access_secret = 'mn9k1rDMV***'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

## avoid rate limit
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


sleeptime = 4

with open('test.json', 'a') as f:
	
	# Fill in the screen name of the user to start the process
	pages = tweepy.Cursor(api.followers, screen_name="****").pages()

	while True:
	    try:
	        page = next(pages)
	        time.sleep(sleeptime)
	    except tweepy.TweepError: #taking extra care of the "rate limit exceeded"
	        time.sleep(60*15) 
	        page = next(pages)
	    except StopIteration:
	        break

	    for user in page:
			screenName =  user.screen_name
			print screenName
			try:
				timelines = api.user_timeline(screen_name = screenName, count = 200, include_rts = True)
				for tweets in timelines:
					f.write(json.dumps(tweets._json) + "\n")
			except Exception, e:
				pass
	

f.close()

