import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

def getTwitts(wordNumber):
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

	# Database querying
	search_result = es.search(index="twitters", doc_type= wordList[wordNumber], size=500)
	# a list of json obj
	list_twitts = search_result['hits']['hits']

	# contain basic info of twitter obj
	twitter_info = []
	for i in list_twitts:
		twitter_info.append({'username':i['_source']['user']['name'], 'text':i['_source']['text'], 'location':i['_source']['user']['location']})

	# print list_twitts[0]['_source']['user']['location']
	# a list of twitters
	return twitter_info
