from pymongo import MongoClient
#import requests, json, unirest
import csv


client = MongoClient("mongodb://eecs395:395pw@ds027155.mongolab.com:27155/yakscrape")
db = client['yakscrape']
yaks = db.yaks

# def getSentiment(text):
# 	# These code snippets use an open-source library. http://unirest.io/python
# 	response = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",
# 	  headers={
# 	    "X-Mashape-Key": "hE2i6lyLhYmshEmKFgrgVXmhskiDp1qClXjjsnIade4Ufa36gl",
# 	    "Content-Type": "application/x-www-form-urlencoded",
# 	    "Accept": "application/json"
# 	  },
# 	  params={
# 	    "language": "english",
# 	    "text": text
# 	  }
# 	)
# 	return(response.body)

#[i.message_id, i.poster_id, location, coordlocation, str(i.message), i.latitude, i.longitude, i.time, i.likes, i.comments]
def createDict(messageID, posterID, region, regionCoord, message, latitude, longitude, time, likes, comments):
	#apiResponse = getSentiment(message)

	newDoc = {};
	newDoc['message_id'] = messageID
	newDoc['poster_id'] = posterID
	newDoc['region'] = region
	newDoc['regionCoord'] = regionCoord
	newDoc['message'] = message
	newDoc['latitude'] = latitude
	newDoc['longitude'] = longitude
	newDoc['time'] = time
	newDoc['likes'] = likes
	newDoc['comments'] = comments
	# newDoc['sentiment'] = apiResponse['label']
	# newDoc['probability'] = apiResponse['probability']

	return(newDoc)


# #Function for clearly printing a dictionary's values
def dictPrint(dictIn):
	for attribute, value in dictIn.items():
		try:
			print('{} : {}'.format(attribute, value))
		except Exception as e:
			continue
	print('\n')

def putInDB(docDict):
	exists = yaks.find({"message_id": docDict['message_id']}).limit(1)
	if(exists.count() == 0):
		result = yaks.insert_one(docDict)


with open('all_yaks-12-5-10PM-MoreNY.csv', newline='') as f:
  reader = csv.reader(f)
  for row in reader:
  	document = createDict(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
  	putInDB(document)
    

