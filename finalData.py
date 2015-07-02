import json
import datetime
import ast
import requests
import xmltodict
import bisect
import os
import isodate
import numpy
from math import floor, ceil
from collections import Counter
import math


APIKEY='API'

def getLengths(codeFile):
    '''Returns a dictionary where keys=video IDs and values=length of video in seconds'''
    code=json.load(open(codeFile))
    v={}
    for i in code.keys():
        information=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+i+'&key='+APIKEY).content)
        if len(information['items'])!=0:
            length=information['items'][0]['contentDetails']['duration']
    	    parsedT=isodate.parse_duration(length)
            secs=parsedT.total_seconds()
            counts=information['items'][0]['statistics']['viewCount']
            v[i]={'length':secs,'counts':counts}
    with open('lengthsAndViews.json', 'w') as outfile:
            json.dump(v, outfile)

#getLengths('videos.json')

def generateVideoDict(fileName):
    '''generates a dictionary where keys are video ids and values are lists of 3-tuples
    (event type, timestamp, current video time). If the events is not play or pause video,
    a 2-tuple is create instead'''
    filename=json.load(open(fileName))
    video={}
    code=''
    found=False
    current=0
    for i in range(len(filename)):
        if filename[i]['event_type']=='pause_video' or filename[i]['event_type']=='play_video':
            d = json.loads(ast.literal_eval(filename[i]['event']))
            videoDict=dict((k,v) for (k,v) in d.items())
            if code!='' and code!=videoDict['code']:
                video[code].append(('watched another video',datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0)))            
            code=videoDict['code']
            found=True
            try:
                current=float(videoDict['currentTime'])
            #when currentTime is not there
            except (KeyError, TypeError):
                if filename[i]['event_type']=='pause_video' and filename[i-1]['event_type']=='play_video':
                    diff=datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0)-datetime.datetime.utcfromtimestamp(filename[i-1]['timestamp']/1000.0)
                    current+=diff.total_seconds()
                elif filename[i]['event_type']=='play_video' and filename[i-1]['event_type']=='pause_video':
                    current=current
                elif filename[i]['event_type']=='play_video' and filename[i-1]['event_type']=='play_video':
                    diff=datetime.datetime.utcfromtimestamp(filename[i+1]['timestamp']/1000.0)-datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0)
                    current=diff.total_seconds()
                else:
                    continue
            if code not in video:
                video[code]=[(filename[i]['event_type'],datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0),current)]
            else:
                video[code].append((filename[i]['event_type'],datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0),current))
        else:
            if found:
                video[code].append((filename[i]['event_type'],datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0)))
                found=False
                code=''
    return video

def parseTimes(listTuples):
    '''Takes a list of 3-tuples and returns a list of intervals. If the current video time is NaN, then
    that event is ignored.'''
    intervals=[]
    type1='play_video'
    type2='pause_video'
    length=len(listTuples)
    i=0
    while i<length-1:
        if listTuples[i][0]==type1:
            start=listTuples[i][2]
            if listTuples[i+1][0]==type2:
                end=listTuples[i+1][2]
            else:
                diff=listTuples[i+1][1]-listTuples[i][1]
                end=start+diff.total_seconds()
            if math.isnan(start)==False and math.isnan(end)==False:
                intervals.append([start,end])
            i+=1
        else:
            i+=1
    return intervals
    
#length=json.load(open('Video-Data/length.json'))

def parseAllVid(videoDict):
    '''Takes a dictionary generated by generateVideoDict() and returns a dictionary where the keys are
    video IDs and values are time intervals'''
    all={}
    for key in videoDict:
        try:
            vidLength=length[key]
            intervals=parseTimes(videoDict[key])
            for i in intervals:
                if i[1]>vidLength:
                    i[1]=vidLength
            all[key]=intervals
        except KeyError:
            all[key]=parseTimes(videoDict[key])
    return all

#listOfFileNames=os.listdir('examtakers')

def allUsers(listOfFiles):
    '''Takes in a list of files for each student and writes a json file with
    a dictionary of intervals for each student'''
    for i in listOfFiles:
        d=generateVideoDict('examtakers/'+i)
        combinedD=parseAllVid(d)
        with open('newData/'+i, 'w') as outfile:
            json.dump(combinedD, outfile)
            

def totalTime(dirname):
    '''Takes in a folder with files about each student. Creates a json file with a dictionary
    where keys are student IDs and values are total time they spent watching videos in minutes'''
    timeDict={}
    listFiles=os.listdir(dirname)
    for i in listFiles:
        oneFile=json.load(open(dirname+'/'+i))
        for key in oneFile:
            #in minutes
            total=(numpy.sum(numpy.diff(oneFile[key])))/60
            if i in timeDict:
                timeDict[i]+=total
            else:
                timeDict[i]=total
    with open('totalTime.json', 'w') as outfile:
        json.dump(timeDict, outfile)

def countViews(filename):
    '''Takes in a dictionary of intervals and returns a dictionary where the keys are
    current time in video (in seconds) and values are number of rewatches at that time'''
    data = json.load(open(filename))            
    peaksDct = {}
    for key in data.keys():
        values = data[key]
        counterSeg = Counter()
        for seg in values:
            seg = [int(floor(seg[0])), int(ceil(seg[1]))] # rounds the intervals
            end = seg[1]
            for el in range(seg[0], end+1):
                counterSeg[el] += 1
        newC=Counter({ k: v for k, v in counterSeg.iteritems() if v not in (0, 1)}) # ignore seconds with 0 or 1 views
        if len(newC) != 0:
            peaksDct[key] = newC
    return peaksDct   

       
def filterRewatches(dirname):
    '''Takes in a folder with student files and creates a json file of dictionaries where the keys are
    current time in video (in seconds) and values are number of rewatches at that time'''
    listFiles=os.listdir(dirname)
    for i in listFiles:
        rewatches=countViews(dirname+'/'+i)
        with open('rewatches/'+i, 'w') as outfile:
            json.dump(rewatches, outfile)
            
def addRewatches(dirname):
    '''Creates a json file of a dictionary where the keys are user IDs and the values
    are dictionaries with the amount of time rewatched in seconds for each video'''
    rewatches={}
    listFiles=os.listdir(dirname)
    for i in listFiles:
        oneFile=json.load(open(dirname+'/'+i))
        secs={}
        for key in oneFile:
            total=sum(oneFile[key].values())-len(oneFile[key].values()) # subtract first time from rewatches
            secs[key]=total
        rewatches[i]=secs
    with open('totalRewatchTime.json', 'w') as outfile:
        json.dump(rewatches, outfile)

def rewatchPeaks(dirname):
    '''Takes in a folder with view counts for every student and creates a json file 
    of a dictionary where the keys are video IDs and values are total
    rewatch views at each second.'''
    rewatches={}
    listFiles=os.listdir(dirname)
    for i in listFiles:
        oneFile=json.load(open(dirname+'/'+i))
        for videoID in oneFile:
            new=Counter({k:v-1 for k,v in oneFile[videoID].items()}) # subtract 1 to exclude the 1st time
            if videoID not in rewatches:
                rewatches[videoID]=new
            else:
                rewatches[videoID]+=new
    with open('rewatchPeaks.json', 'w') as outfile:
            json.dump(rewatches, outfile)
                