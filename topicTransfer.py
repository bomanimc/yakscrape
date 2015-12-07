import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from dateutil import parser
from pymongo import MongoClient
import json


yakclient = MongoClient("mongodb://eecs395:395pw@ds027155.mongolab.com:27155/yakscrape")
tagclient = MongoClient("mongodb://eecs395:eecs395@apollo.modulusmongo.net:27017/us8upoZa")
yakdb = yakclient['yakscrape']
tagdb = tagclient['us8upoZa']
yaktags = tagdb.yaktags
yaks = yakdb.yaks



tagCursor = yaktags.find({});
# yakcursor = yaks.find({'message_id' : "R/566366478680ff994029f3f9acba7"});


# for yak in yakcursor:
# 	print yak


for tag in tagCursor:
	# print tag
	m_id = tag['message_id']
	tones = tag['tones']
	topics = tag['topics']

	oneC = yaks.find({ 'message_id' : m_id}).limit(1);
	# # print oneC
	yak_id = None

	for row in oneC:
		yak_id = row['_id']

	result = yaks.update_one(
		{ '_id' : yak_id}, 
		{
		  '$set': {'topics': topics, 'tones': tones}
		}
	)

	print result.modified_count

