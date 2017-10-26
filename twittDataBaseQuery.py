import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import tweepy
from tweepy import OAuthHandler
import random
import re
import googlemaps


gmaps = googlemaps.Client(key='AIzaSyBoSqXtWfy90BM7Mr0AMAoZcOOw5ZPrglM')

emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+", re.UNICODE)


# Authentication for AWS ES
AWS_ACCESS_KEY = 'AKIAJ64AHWCSS5HG6BDQ'
AWS_SECRET_KEY = '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'
region = 'us-east-1'
service = 'es'
wordList = ['serendipity','AlphaGo Zero','HKUST','Columbia University','Cloud Computing','Drunken Noodles','Facebook','Eason Chan','X-man','Gotham']
awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)
host = 'search-twitterdata-lz2xqedrliqfw7l423g5uo7a34.us-east-1.es.amazonaws.com'

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

# Authentication for Twitter API
consumer_key = '6FTxbOcOaIwX1yzDCo4kJdxvt'
consumer_secret = 'UHdnHVRSRwCbhXrGWExy1poVNP9buNo5KpeRiOsAK8C8OmcRkc'
access_token = '2439402091-TWGdQR1eOqPELxEigMs7de4RPXiT0aWg7ovuWfm'
access_secret = 'iGsKk33zlpOjZ3oIInf7gvM0mIc8rZeG5sUCfnY3MyhR5'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# keep track of current number of twitts of a type
doc_count = 0
doc_type = ''

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        stream_result = status._json
        location = str(stream_result['user']['location'])
        location = emoji_pattern.sub(r'', location)

        if location:
            result = gmaps.geocode(location)
            if result:
                stream_result['user']['location'] = result[0]['geometry']['location']
            else:
                stream_result['user']['location'] = {'lat':random.uniform(-90,90), 'lng':random.uniform(-180,180)}
        else:
            stream_result['user']['location'] = {'lat':random.uniform(-90,90), 'lng':random.uniform(-180,180)}
        global doc_count
        global doc_type
        doc_count += 1
        es.create(index="twitterstream", doc_type=doc_type, id=str(doc_count), body=stream_result)
        

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)


def getTwitts(wordNumber):
	
	# Database querying
	search_result = es.search(index="twitters", doc_type= wordList[wordNumber], size=200)
	# a list of json obj
	list_twitts = search_result['hits']['hits']

	# stream database querying
	search_streamed = es.search(index="twitterstream", doc_type= wordList[wordNumber], size=200)
	list_streamed = search_streamed['hits']['hits']

	merged_list = list_twitts + list_streamed

	# add new live streamed twitts
	global doc_count
	doc_count = len(list_streamed)
	global doc_type
	doc_type = wordList[wordNumber]
	myStream.filter(track=[wordList[wordNumber]])
	
	# contain basic info of twitter obj
	twitter_info = []
	for i in merged_list:
		text = i['_source']['text'].replace('\n',' ')
		twitter_info.append({'username':i['_source']['user']['name'], 'text':text, 'location':i['_source']['user']['location']})


	 #print list_twitts[0]['_source']['user']['location']
	 #a list of twitters
	return twitter_info

