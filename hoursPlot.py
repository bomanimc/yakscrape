import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from dateutil import parser
from pymongo import MongoClient
import json
from copy import deepcopy

client = MongoClient("mongodb://eecs395:395pw@ds027155.mongolab.com:27155/yakscrape")
db = client['yakscrape']
yaks = db.yakfinal

NU = ['Northwestern University, Evanston, IL', 'Wilmette, IL', 'Skokie, IL', 'Rogers Park, IL']
UChicago = ['University of Chicago', 'Hyde Park, IL', 'Southshore Park, IL']
#Took out Kenwood from UChi
NY = ['Manhattan, NY', 'Bronx, NY', 'Queens, NY', 'Brooklyn, NY']
Stanford = ['Stanford University', 'Los Altos, CA', 'Palo Alto, CA', 'Menlo Park, CA']
JHU = ['John Hopkins University', 'Hampden, MD', 'Remington, MD', 'Waverly, MD'];
Vanderbilt = ['Vanderbilt University', 'Green Hills, TN', 'East Nashville, TN', 'Berry Hill, TN']
Madison = ['University of Wisconsin - Madison', 'Madison, WI', 'Monona, WI', 'Fitchburg, WI']
CollegePark = ['University of Maryland - College Park', 'Adelphi, MD', 'Hyattsville, MD', 'Beywrn Heights, MD']
UCLA = ['University of Californa - Los Angeles', 'Bel Air, CA', 'Holmby Hills, CA', 'Century City, CA', 'Brentwood, CA']
WashU = ['Washington University St. Louis', 'Ferguson, MO', 'Central West End, MO', 'Downtown St. Louis']
Rice = ['Rice University','Downtown Houston', 'Montrose, TX', 'Woodland Heights. TX']


topicsList = ['Advice', 'Art', 'Entertainment', 'Food', 'Funny', 'Gaming', 'Internet', 'News', 'Politics', 'School', 'Science', 'Sex', 'Sports', 'Travel', 'Other']
tonesList = ['Angry', 'Creepy', 'Happy', 'Helpful', 'Insult', 'Joking', 'Positive', 'Negative', 'Sad', 'Violent']

#Function for clearly printing a dictionary's values
def dictPrint(dictIn):
	for attribute, value in dictIn.items():
		print('{} : {}'.format(attribute, value))
	print('\n')

# A function for binning the times of each posts
def timeBinning(cursor):
	amount = cursor.count()
	#timeBins = dict.fromkeys(range(0, 24), 0)
	timeBins = dict.fromkeys(range(0, 3), 0)
	for row in cursor:
		rowHour = parser.parse(row['time']).hour
		if(rowHour > 1 and rowHour <= 8):  #Morning Bucket
			timeBins[0] += 1
		elif(rowHour > 8 and rowHour <= 16): 
			timeBins[1] += 1
		else:
			timeBins[2] += 1
	return(timeBins)
	
def normalize(dictIn, count):
	normalBins = dict.fromkeys(range(0, 3), 0)
	for attribute, value in dictIn.items():
		normalBins[attribute] = 100*(dictIn[attribute]/float(count))
	dictPrint(normalBins)

	checkList = []
	for attribute, value in normalBins.items():
		checkList.append(normalBins[attribute])
	print('Sum is {}. Count is {}.'.format(sum(checkList), count))

	return(normalBins)

def getVals(dictIn):
	vals = []
	for attribute, value in dictIn.items():
		vals.append(value)
	print(sum(vals))
	return vals

def createTraces(locations):
	allHours = range(0, 23)
	data = []
	for place in locations:
		print(place)
		dbCursor = yaks.find({"region":place})
		timeBins = normalize(timeBinning(dbCursor), dbCursor.count())
		print(timeBins)

		trace = go.Bar(
			x = ['2AM-8AM', '9AM-4PM', '5PM-1AM'],
			y = getVals(timeBins), 
			name=place,
		    opacity=0.75
		)
		
		data.append(trace)
	return(data)


def makeLayout(title):
	layout = go.Layout(
	title=title,
    xaxis=dict(
    	title='Time Range',
    ),
    yaxis=dict(
        title='Percent of Yaks'
    ),
    barmode='group',
)


def getAllFromCursor(cursor):
	data = []

	for datum in cursor:
		# print datum
		data.append(datum)

	return data

def makeTimeBin(yaks):
	timeBins = dict.fromkeys(range(0, 3), [])

	for time in range(0, 3):
		timeBins[time] = []

	for yak in yaks:
		rowHour = parser.parse(yak['time']).hour

		if(rowHour > 1 and rowHour <= 8):  #Morning Bucket
			timeBins[0].append(yak)
		elif(rowHour > 8 and rowHour <= 16): 
			timeBins[1].append(yak)
		else:
			timeBins[2].append(yak)

	return timeBins

def makeTopicBins(yaks):
	ret = dict.fromkeys(topicsList, None)

	for topic in topicsList:
		ret[topic] = []

	# print ret
	for yak in yaks:
		# print "new yak*******************"
		for topic in  topicsList:
			try:
				# print topic + ": " + str(yak['topics'][topic])
				if yak['topics'][topic]:
					ret[topic].append(yak)
					# print "Added. New length: {0}".format(len(ret[topic])) 

			except KeyError:
				print "Skipping"

	return ret 

def collapseTopicsBin(topicBin):
	ret = []

	for topic in topicsList:
		total = len(topicBin[topic])
		print "Total for {0} is {1}".format(topic, total)
		ret.append(total)

	return ret


def makeTopicTimePlot(region):
	cursor = yaks.find({'region' : region});
	yakdata = getAllFromCursor(cursor)

	yak_t = makeTimeBin(deepcopy(yakdata))
	print "Morning yaks length"
	print len(yak_t[0])
	print len(yak_t[1])
	print len(yak_t[2])

	yak_tt = dict.fromkeys(range(0, 3), None)
	yak_ttc = dict.fromkeys(range(0, 3), None)


	for key in yak_t:
		print "Time bin key"
		yak_tt[key] = makeTopicBins(yak_t[key])
		yak_ttc[key] = collapseTopicsBin(yak_tt[key])


	times = ['2AM-8AM', '9AM-4PM', '5PM-1AM']

	data = []

	for key in dict.fromkeys(range(0, 3), None):
		trace = go.Bar(
			x = topicsList,
			y = yak_ttc[key], 
		    opacity=0.75,
		    name=times[key]
		)

		data.append(trace);


	layout = go.Layout(
		title='Topics Over Time for ' + region,
	    xaxis=dict(
	    	title='Topics',
	    ),
	    yaxis=dict(
	        title='Number of Yaks'
	    ),
	    barmode='group',
	)

	fig = go.Figure(data=data, layout=layout)
	fname = region + "_topics_over_time"
	fname = fname.replace(" ", "")
	fname = fname.replace(",", "")
	plot_url = py.plot(fig, filename=fname)


makeTopicTimePlot(NY[3]);

# area = Rice;
# fig = go.Figure(data=createTraces(area), layout=layout)
# plot_url = py.plot(fig, filename='time-bar')
