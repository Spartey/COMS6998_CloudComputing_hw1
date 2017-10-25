import tweepy
from tweepy import OAuthHandler
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import geocoder
import random
import re
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyBoSqXtWfy90BM7Mr0AMAoZcOOw5ZPrglM')

emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+", flags=re.UNICODE)

# Authentication for Twitter API
consumer_key = '6FTxbOcOaIwX1yzDCo4kJdxvt'
consumer_secret = 'UHdnHVRSRwCbhXrGWExy1poVNP9buNo5KpeRiOsAK8C8OmcRkc'
access_token = '2439402091-TWGdQR1eOqPELxEigMs7de4RPXiT0aWg7ovuWfm'
access_secret = 'iGsKk33zlpOjZ3oIInf7gvM0mIc8rZeG5sUCfnY3MyhR5'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# Authentication for AWS ES
AWS_ACCESS_KEY = 'AKIAJ64AHWCSS5HG6BDQ'
AWS_SECRET_KEY = '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'
region = 'us-east-1'
service = 'es'

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)
host = 'search-twitterdata-lz2xqedrliqfw7l423g5uo7a34.us-east-1.es.amazonaws.com'

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

# All 10 possible keywords
wordList = ['serendipity','AlphaGo Zero','HKUST','Columbia University','Cloud Computing','Drunken Noodles','Facebook','Eason Chan','X-man','Gotham']
max_twitts = 450

search_result = [status._json for status in tweepy.Cursor(api.search,q='Beethoven',since='2017-10-14',until='2017-10-21').items(max_twitts)]
# print(len(search_result))

for i in range(0,len(search_result)):
    # change location 
    location = search_result[i]['user']['location']
    # remove emojis,...
    location = emoji_pattern.sub(r'', location)

    # print(location)

    if location:
        result = gmaps.geocode(location)
        if result:
            search_result[i]['user']['location'] = result[0]['geometry']['location']
        else:
            search_result[i]['user']['location'] = {'lat':random.uniform(-90,90), 'lng':random.uniform(-180,180)}
    else:
        search_result[i]['user']['location'] = {'lat':random.uniform(-90,90), 'lng':random.uniform(-180,180)}
    es.index(index="twitters", doc_type="serendipity", id=str(i), body=search_result[i])



#print(es.get(index="twitters", doc_type="serendipity", id="5"))



# f = open('data.json','w')
# search_result = [status._json for status in tweepy.Cursor(api.search,q='serendipity',since='2017-10-14',until='2017-10-21').items(max_twitts)]
# for i in range(0,len(search_result)):
#     json.dump({"index" : { "_index": "twitterdata", "_type" : "serendipity", "_id" : str(i+1) }},f)
#     f.write('\n')
#     json.dump(search_result[i], f)
#     f.write('\n')
# f.close()



# f = open('data.json','w')
# for word in wordList:
#     search_result = [status._json for status in tweepy.Cursor(api.search,q=word,since='2017-10-14',until='2017-10-21').items(max_twitts)]
#     for i in search_result:
#         json.dump(i, f)
#         f.write('\n')
# f.close()

#search_result = [status._json for status in tweepy.Cursor(api.search,q='Gotham',since='2017-10-14',until='2017-10-21').items(max_twitts)]

#print(len(search_result))

