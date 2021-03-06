# -*- coding: utf-8 -*-
#Amanda Foun and Ella Chao 
#views_lineChart.py creates a line chart to show the peaks in video views

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components # generates individual component
from bokeh.models import HoverTool, axes
from bruteforce import getPeaksForOneVideo
import json
import numpy
import pylab
import numpy as np
from bokeh.charts import BoxPlot, output_file, show
from bokeh.charts import Bar, output_file, show



videoInfo = json.loads(open("FinishedCourseData/pausePlayBinsSmooth.json").read()) # smoothed
videoInfo2 = json.loads(open("FinishedCourseData/pausePlayBins.json").read()) # original
wordfreq = json.loads(open("videoTranscripts/transcriptsWordFrequency.json").read())
titles = json.loads(open("videoTranscripts/videos.json").read())
lengthInfo = json.loads(open("FinishedCourseData/pausePlay.json").read()) # distribution of lengths
vidEngage = json.loads(open("averageVideoEngagement.json").read()) # distribution of lengths
vidEngageUsers = json.loads(open("aggregatedVideoEngagement.json").read()) # distribution of lengths

def sortDicts():
    '''Returns a list of sorted IDs, greatest break count to smallest break count'''
    toSort = [(max(videoInfo[d].values()),d) for d in videoInfo]
    toSort.sort(reverse=True)
    sortedIDs = [el[1] for el in toSort] # list of sorted IDs, from the videos with the most counts to the least
    return sortedIDs

def makeScripts():
    '''Creates a text file that contains all the scripts for the videos'''
    scripts = open('Bokeh/towersOfHanoi.txt', 'w')
    #sortedIDs = sortDicts()
    #for vid in sortedIDs:
    #    try: # only get the scripts of the graphs with transcripts
    script, div = withPeaks("SVQuLOiHJeE")
    scripts.write(script + '\n')
    scripts.write(div + '\n')
        #except KeyError:
        #    pass
    scripts.close()
    

def withPeaks(videoID):
    '''Plots a Bokeh graph of video views with the peaks''' 
    
    fiveWords=[wordfreq[videoID][i][0] for i in range(len(wordfreq[videoID])) if i <5]
    stringFiveWords=', '.join(fiveWords)
    viewsDict = videoInfo[videoID]
    viewsDict2 = videoInfo2[videoID]
      
    # x and y contain the points to plot on the graph
    x = []
    y = []
    toInt = map(float, viewsDict.keys())
    toInt.sort()
    for k in toInt: # populate x and y
        x.append(int(k))
        y.append(viewsDict[str(k)]) # append the corresponding video views 
    
    # i and j contain the points to plot on the graph
    i = []
    j = []
    toInt2 = map(float, viewsDict2.keys())
    toInt2.sort()
    for m in toInt2: # populate i and j
        i.append(int(m))
        j.append(viewsDict2[str(m)]) # append the corresponding video views 
    
    # a and b contain the peaks to plot on the graph
    a = []
    b = []
    peaksList = getPeaksForOneVideo(videoID) # list of tuples
    for tup in peaksList:
        a.append(float(tup[0]))
        b.append(tup[1])  

    output_file("towersOfHanoi.html")

    hover = HoverTool(
        tooltips = [
            ("(x,y)", "($x, $y)"),
        ])
    
    TOOLS = ['resize, save, pan, box_zoom, wheel_zoom',hover]
    
    p = figure(plot_width=800, plot_height=800,tools=TOOLS, name=stringFiveWords, title_text_font_size='12pt',title=titles[videoID]['title'][21:], x_axis_label='time (s)', y_axis_label='counts')
    p.xaxis.axis_label_text_font_size='12pt'
    # add original unsmoothed line
    p.line(i[1:-1], j[1:-1], line_color='silver', line_width=2)
    p.line(x[1:-1], y[1:-1], legend=videoID, line_color='royalblue', line_width=2) #legend=videoID
   #p.legend.orientation = "bottom_left"
    p.circle(a, b, fill_color="darkorange", size=8)
    
    #show(p)
    script, div = components(p)
    return script, div  
            
def noPeaks(videoID):
    '''Plots a Bokeh graph of video views'''
    
    fiveWords=[wordfreq[videoID][i][0] for i in range(len(wordfreq[videoID])) if i <5]
    stringFiveWords=', '.join(fiveWords)
    viewsDict = videoInfo[videoID]
      
    # x and y contain the points to plot on the graph
    x = []
    y = []
    
    toInt = map(float, viewsDict.keys())
    toInt.sort()
    for k in toInt: # populate x and y
        x.append(k)
        y.append(viewsDict[str(k)]) # append the corresponding video views
        
    TOOLS = 'resize,hover, save, pan, box_zoom, wheel_zoom'

    p = figure(plot_width=400, plot_height=400,tools=TOOLS, title_text_font_size='12pt',title=titles[videoID]['title'][21:], x_axis_label='time (s)', y_axis_label='counts')

    # add a line and set line thickness
    p.line(x[1:], y[1:], legend=videoID, line_width=2)
    
    # display chart 
    #output_file("views.html", title="Peaks in Video Views")
    #show(p)
    script, div = components(p)
    return script, div

def lengthDistribution(videoID, breakPt):
    '''Creates a histogram of the distribution of lengths of breaks. 
       Only plots the breaks with length less than breakPt (seconds)'''
    fiveWords=[wordfreq[videoID][i][0] for i in range(len(wordfreq[videoID])) if i <5]
    stringFiveWords=', '.join(fiveWords)
    lengths = [elt[1] for elt in lengthInfo[videoID]]
    filteredLen = [i for i in lengths if i<=breakPt]
    keep = float(len(filteredLen))/len(lengths)
    percent = float("%.2f" % keep)*100 # get percentage of points that we kept after filtering out the big values
    
    hover = HoverTool(
        tooltips = [
            ("(x,y)", "($x, $y)"),
        ])
    
    TOOLS = ['resize, save, pan, box_zoom, wheel_zoom',hover]

    p = figure(plot_width=800, plot_height=800,tools=TOOLS, name=stringFiveWords, 
    title_text_font_size='12pt',title=titles[videoID]['title'][21:], 
    x_axis_label='Break Lengths (s)', y_axis_label='Count')
    
    p.xaxis.axis_label_text_font_size='12pt'
    p.yaxis.axis_label_text_font_size='12pt'    

    hist, edges = np.histogram(filteredLen, bins=100)
    
    p.quad(top=hist, bottom=0, legend=str(percent)+'% below '+str(breakPt), left=edges[:-1], right=edges[1:],
       line_color="#033649",\
    )

    output_file('histogram.html')
    show(p)
    #script, div = components(p)
    #return script, div

   
        

def allLengths():
   allLens = sorted([i[1] for vid in lengthInfo for i in lengthInfo[vid]])
   with open('allBreakLens.json', 'w') as outfile:
            json.dump(allLens, outfile)   

def allLengthDistribution(startPt,breakPt):
    '''Creates a histogram of the distribution of lengths of breaks. 
       Only plots the breaks with length less than breakPt (seconds)'''
    lengths = json.loads(open('allBreakLens.json').read())
    filteredLen = [i for i in lengths if i<=breakPt and i>startPt]
    keep = float(len(filteredLen))/len(lengths)
    percent = float("%.2f" % keep)*100 # get percentage of points that we kept after filtering out the big values
    
    hover = HoverTool(
        tooltips = [
            ("(x,y)", "($x, $y)"),
        ])
    
    TOOLS = ['resize, save, pan, box_zoom, wheel_zoom',hover]

    p = figure(plot_width=500, plot_height=500,tools=TOOLS, 
    title_text_font_size='12pt',title='All Break Lengths Between ' + str(startPt) + ' and ' + str(breakPt), 
    x_axis_label='Break Lengths (s)', y_axis_label='Count')
    
    p.xaxis.axis_label_text_font_size='12pt'
    p.yaxis.axis_label_text_font_size='12pt'    

    hist, edges = np.histogram(filteredLen, bins=50)

    #output_file('histogram.html')
    #show(p)
    script, div = components(p)
    return script, div

    
            
def makeScriptsHist():
    '''Creates a text file that contains all the scripts for the videos'''
    scripts = open('Bokeh/test.txt', 'w')
    #for vid in lengthInfo:
       # try: # only get the scripts of the graphs with transcripts
    script, div = vidEngageDistributionOneUser("icmehhllem.json")
            #script2, div2 = lengthDistribution(vid, 200)
            #script3, div3 = lengthDistribution(vid, 400)
    scripts.write(script + '\n')
    scripts.write(div + '\n')
            #scripts.write(script2 + '\n')
            #scripts.write(div2 + '\n')
            #scripts.write(script3 + '\n')
            #scripts.write(div3 + '\n')
     #   except KeyError:
      #      pass
    scripts.close()

def averageBreakLen():
    allNum=0
    lengthOfLength=0
    lengthOfFilter=0
    for vid in lengthInfo:
        length=[i[1] for i in lengthInfo[vid]]
        filteredLen=[i for i in length if i<=100]
        lengthOfLength+=len(length)
        lengthOfFilter+=len(filteredLen)
        allNum+=sum(filteredLen)/float(len(filteredLen))
    average=allNum/len(lengthInfo.keys())
    return average, float(lengthOfFilter)/lengthOfLength
    
def vidEngageDistribution():
    '''Creates a histogram of the distribution of video engagement'''
    lengths =sorted(vidEngage.values(), reverse=True)[:10]
    t=sorted(vidEngage, key=vidEngage.get,reverse=True)[:10]
    print t
    actualTitles=[titles[i]['title'][21:].replace('_',' ') for i in t]
        
    hover = HoverTool(
        tooltips = [
            ("(x,y)", "($x, $y)"),
        ])
    
    TOOLS = ['resize, save, pan, box_zoom, wheel_zoom',hover]
    output_file("h.html")
    bar = Bar(lengths, actualTitles, title="Overall Distribution of Video Engagement",width=800,height=800,ylabel='Video Engagement Factor')
    show(bar)
 

def vidEngageDistributionOneUser(userID):
    lengths =sorted(vidEngageUsers[userID].values(), reverse=True)[:30]
    t=sorted(vidEngageUsers[userID], key=vidEngageUsers[userID].get,reverse=True)[:30]
    actualTitles=[titles[i]['title'][21:].replace('_',' ') for i in t][:30]
    
        
    hover = HoverTool(
        tooltips = [
            ("(x,y)", "($x, $y)"),
        ])
    
    TOOLS = ['resize, save, pan, box_zoom, wheel_zoom',hover]
    output_file("h.html")
    bar = Bar(lengths, actualTitles, title="Distribution of Video Engagement",width=1000,height=1000, ylabel='Video Engagement Factor')
    show(bar)    

def vidEngageDistributionOneVideo(videoID):
    factor=sorted([vidEngageUsers[user][i] for user in vidEngageUsers for i in vidEngageUsers[user] if i==videoID][:30], reverse=True)
    print factor
    userNames=[i[0] for i in sorted([(u.replace('.json',''),vidEngageUsers[u][j]) for u in vidEngageUsers for j in vidEngageUsers[u] if j==videoID][:30],key=lambda x: x[1],reverse=True)]
    hover = HoverTool(
        tooltips = [
            ("(x,y)", "($x, $y)"),
        ])
    
    TOOLS = ['resize, save, pan, box_zoom, wheel_zoom',hover]
    output_file("h.html")
    bar = Bar(factor, userNames, title="Distribution of Video Engagement for ",width=1000,height=1000, ylabel='Video Engagement Factor')
    show(bar)    
            
    #script, div = components(bar)
    #return script, div 
#############
## TESTING ## 
#############
 
#makeScripts()
#withPeaks("SVQuLOiHJeE")
#noPeaks("IRxsjPGh1oQ")
#lengthDistribution("IRxsjPGh1oQ",600)
#makeScriptsHist()

#vidEngageDistributionOneUser("icmehhllem.json")
vidEngageDistributionOneVideo('CsQrTLde-dM')

