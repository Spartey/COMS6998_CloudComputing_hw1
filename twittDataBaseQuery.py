import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# Authentication for AWS ES
AWS_ACCESS_KEY = 'AKIAIFBL2BHBX2WG6OZA'
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

# Database querying
search_result = es.search(index="twitters", doc_type="serendipity", size=500)
# a list of json obj
list_twitts = search_result['hits']['hits']

# a list of coordinates