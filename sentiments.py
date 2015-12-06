import requests, json, unirest
from pymongo import MongoClient
import csv

client = MongoClient("mongodb://eecs395:395pw@ds027155.mongolab.com:27155/yakscrape")
db = client['yakscrape']
yaks = db.yaks

def getSentiment(text):
	# These code snippets use an open-source library. http://unirest.io/python
	response = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",
	  headers={
	    "X-Mashape-Key": "hE2i6lyLhYmshEmKFgrgVXmhskiDp1qClXjjsnIade4Ufa36gl",
	    "Content-Type": "application/x-www-form-urlencoded",
	    "Accept": "application/json"
	  },
	  params={
	    "language": "english",
	    "text": text
	  }
	)
	return(response.body)


#allYaks = yaks.find({});
allYaks = yaks.find( { 'sentiment' : { '$exists' : False } } );
print(allYaks.count())
for doc in allYaks:
	if('message' in doc.keys()):
		apiResponse = getSentiment(doc['message'])
		sentimmentProbability = apiResponse['probability']
		sentiment = apiResponse['label']

		yaks.update_one(
			{ '_id' : doc['_id']}, 
			{
			  '$set': {'sentiment': sentiment, 'probability': sentimmentProbability}
			}, upsert=False)
	else:
		print('No message');