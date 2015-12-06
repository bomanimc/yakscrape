import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from dateutil import parser
from pymongo import MongoClient
import json

client = MongoClient("mongodb://eecs395:395pw@ds027155.mongolab.com:27155/yakscrape")
db = client['yakscrape']
yaks = db.yaks

# NU = ['Northwestern University, Evanston, IL', 'Wilmette, IL', 'Skokie, IL', 'Rogers Park, IL']
# UChicago = ['University of Chicago', 'Hyde Park, IL', 'Kenwood, IL', 'Southshore Park, IL']
# Columbia = ['Columbia University', 'Manhattan, NY', 'Bronx, NY', 'North Bergen, NJ', 'Queens, NY', 'Brooklyn, NY']
# Stanford = ['Stanford University', 'Los Altos, CA', 'Palo Alto, CA', 'Menlo Park, CA']
# JHU = ['John Hopkins University', 'Hampden, MD', 'Remington, MD', 'Waverly, MD'];
# Vanderbilt = ['Vanderbilt University', 'Green Hills, TN', 'East Nashville, TN', 'Berry Hill, TN']
# Madison = ['University of Wisconsin - Madison', 'Madison, WI', 'Monona, WI', 'Fitchburg, WI']
# CollegePark = ['University of Maryland - College Park', 'Adelphi, MD', 'Hyattsville, MD', 'Beywrn Heights, MD']
# UCLA = ['University of Californa - Los Angeles', 'Bel Air, CA', 'Holmby Hills, CA', 'Century City, CA', 'Brentwood, CA']
# WashU = ['Washington University St. Louis', 'Ferguson, MO', 'Central West End, MO', 'Downtown St. Louis']
# Rice = ['Rice University','Downtown Houston', 'Montrose, TX', 'Woodland Heights. TX']

#Function for clearly printing a dictionary's values
def dictPrint(dictIn):
	for attribute, value in dictIn.items():
		print('{} : {}'.format(attribute, value))
	print('\n')

# A function for binning the times of each posts
def timeBinning(cursor):
	amount = cursor.count()
	timeBins = dict.fromkeys(range(0, 24), 0)
	for row in cursor:
		rowHour = parser.parse(row['time']).hour
		timeBins[rowHour] += 1
	return(timeBins)
	
def normalize(dictIn, count):
	normalBins = dict.fromkeys(range(0, 24), 0)
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

		# Create traces
		trace = go.Scatter(
		    x = allHours,
		    y = getVals(timeBins),
		    mode = 'lines+markers',
		    name = place,
			opacity=0.75
		)
		data.append(trace)

	return(data)


layout = go.Layout(
    title='New York Area Yak Activity',
    xaxis=dict(
        title='Time (Hour)'
    ),
    yaxis=dict(
        title='Percent of Yaks'
    )
)

area = ['Manhattan, NY', 'Bronx, NY', 'North Bergen, NJ', 'Queens, NY', 'Brooklyn, NY']
fig = go.Figure(data=createTraces(area), layout=layout)
plot_url = py.plot(fig, filename='time-line')
