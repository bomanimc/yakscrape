import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from dateutil import parser
from pymongo import MongoClient
import json


client = MongoClient("mongodb://eecs395:eecs395@apollo.modulusmongo.net:27017/us8upoZa")
yakclient = MongoClient("mongodb://eecs395:395pw@ds027155.mongolab.com:27155/yakscrape")
db = client['us8upoZa']
yakdb = yakclient['yakscrape']
yaktags = db.yaktags
yaks = yakdb.yaks


NY = ['Manhattan, NY', 'Bronx, NY', 'Queens, NY', 'Brooklyn, NY']


topicsList = ['Advice', 'Art', 'Entertainment', 'Food', 'Funny', 'Gaming', 'Internet', 'News', 'Politics', 'School', 'Science', 'Sex', 'Sports', 'Travel', 'Other']
tonesList = ['Angry', 'Creepy', 'Happy', 'Helpful', 'Insult', 'Joking', 'Positive', 'Negative', 'Sad', 'Violent']

#Function for clearly printing a dictionary's values
def dictPrint(dictIn):
	for attribute, value in dictIn.items():
		print('{} : {}'.format(attribute, value))
	print('\n')

def getVals(dictIn):
	vals = []
	for attribute, value in dictIn.items():
		vals.append(value)
	print(sum(vals))
	return(vals)

def normalize(dictIn, count, refList):
	normalBins = dict.fromkeys(refList, 0)
	for attribute, value in dictIn.items():
		normalBins[attribute] = 100*(dictIn[attribute]/float(count))
	dictPrint(normalBins)

	checkList = []
	for attribute, value in normalBins.items():
		checkList.append(normalBins[attribute])
	print('Sum is {}. Count is {}.'.format(sum(checkList), count))

	return(normalBins)


def barForTopics(cursor):
	cursor = cursor.rewind()
	topicBins = dict.fromkeys(topicsList, 0)
	allTopics = []
	
	dictPrint(topicBins)
	for attribute, value in topicBins.items():
		allTopics.append(attribute)

	print(allTopics)

	dictPrint(topicBins)

	for row in cursor:
		#yak = yaks.find({ "message_id" : row['message_id'] }).limit(1)
		for attribute, value in row['topics'].items():
			if(value == True):
				topicBins[attribute] += 1
	dictPrint(topicBins)
	#normalBins = normalize(topicBins, cursor.count(), topicsList)

	trace = go.Bar(
		x = allTopics,
		y = getVals(topicBins), 
	    opacity=0.75,
	    marker=dict(
	    	color='rgb(231, 76, 60)'
	    )
	)

	data = [trace]

	layout = go.Layout(
		title='Yak Topics',
	    xaxis=dict(
	    	title='Topics',
	    ),
	    yaxis=dict(
	        title='Percent of Yaks'
	    ),
	    barmode='group',
	)

	fig = go.Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename='topic-bar')


def barForTones(cursor):
	cursor = cursor.rewind()
	tonesBins = dict.fromkeys(tonesList, 0)
	allTones = []
	
	dictPrint(tonesBins)
	for attribute, value in tonesBins.items():
		allTones.append(attribute)

	print(allTones)

	dictPrint(tonesBins)
	for row in cursor:
		#yak = yaks.find({ "message_id" : row['message_id'] }).limit(1)
		for attribute, value in row['tones'].items():
			if(value == True):
				tonesBins[attribute] += 1
	dictPrint(tonesBins)

	trace = go.Bar(
		x = allTones,
		y = getVals(tonesBins), 
	    opacity=0.75,
	    marker=dict(
	    	color='rgb(231, 76, 60)'
	    )
	)

	data = [trace]

	layout = go.Layout(
		title='Yak Tones',
	    xaxis=dict(
	    	title='Tones',
	    ),
	    yaxis=dict(
	        title='Percent of Yaks'
	    ),
	    barmode='group',
	)

	fig = go.Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename='tones-bar')


def createTopicTraces(locations):
	allHours = range(0, 23)
	data = []
	for place in locations:
		topicBins = dict.fromkeys(topicsList, 0)
		allTopics = []
		
		dictPrint(topicBins)
		for attribute, value in topicBins.items():
			allTopics.append(attribute)

		print(place)
		regionYaks = yaks.find({"region":place})
		print('DB Cursor is {}'.format(regionYaks.count()))
		for row in regionYaks:
			topicForRow = yaktags.find({"message_id":row['message_id']}).limit(1);
			for attribute, value in topicForRow['topics'].items():
				if(value == True):
					topicBins[attribute] += 1
		dictPrint(topicBins)

		trace = go.Bar(
			x = NY,
			y = getVals(topicBins), 
			name=place,
		    opacity=0.75
		)
		
		data.append(trace)
	
	layout = go.Layout(
		title='Yak Topics Across New York',
	    xaxis=dict(
	    	title='Topics',
	    ),
	    yaxis=dict(
	        title='Number of Yaks'
	    ),
	    barmode='group',
	)

	# fig = go.Figure(data=data, layout=layout)
	# plot_url = py.plot(fig, filename='tones-bar-allNY')



#dbCursor = yaktags.find({})
#barForTopics(dbCursor)
#barForTones(dbCursor)
createTopicTraces(NY)

