import tweepy
from tweepy import OAuthHandler
import json
from tweepy import Stream
from tweepy.streaming import StreamListener


######################################################################
## API access key and tokens, please replace with yours
consumer_key = 'U8anfB2BuVJD********'
consumer_secret = 'sn1SXhuLU********'
access_token = '840800636337********'
access_secret = '0L7P6b6vh3HA*******'
######################################################################


# Authenticate and connect with Twitter
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


# Store Tweets into CouchDB 
class TweetStore(object):
    def __init__(self, dbname, url='http://admin:admin@localhost:5984/'):
        try:
            self.server = couchdb.Server(url=url)
            self.db = self.server.create(dbname)
            #self._create_views()
        except couchdb.http.PreconditionFailed:
            self.db = self.server[dbname]
                  
    def save_tweet(self, tw):
        tw['_id'] = tw['id_str']
        if tw['_id'] in self.db:
            pass
        else:
            self.db.save(tw)


# Streaming process, collect tweets from twitter
class MyListener(StreamListener):
    def on_data(self, data):
        try:
            #store in a .json file to check result
            # with open('diabetesmel.json', 'a') as f:
            #     f.write(data)
            #     convert unicode to json format
            #     data = json.loads(data)
            #     screenName = data['user']['screen_name']
            #     print screenName
            
            tweets_data = json.loads(data)
            TweetStore.save_tweet(tweets_data)   
        
        except BaseException as e:
            print 'Exception: ', str(e)
        return True
    
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())

#Collect tweets within Melbourne 
twitter_stream.filter(locations=[144.5937,-38.4338,145.5126,-37.5112])

