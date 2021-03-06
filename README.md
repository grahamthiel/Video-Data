# Video-Data
Analyzing data from an online course.

CONTENTS:

+ <b>bigram.py:</b> Finds the frequency of bigrams in video transcript. Helps with creating video descriptions.

+ <b>bigrams.json:</b> Dictionary of dictionaries where keys are video IDs and values are frequency of bigrams.

+ <b>bokeh.css:</b> CSS for generating Bokeh graphs on a webpage.

+ <b>bokeh.html:</b> Generates Bokeh graphs of video views. Contains scripts which create each individual Bokeh graph.

+ <b>bokeh.js:</b> JS for generating Bokeh graphs on a webpage. boxes() adds checkboxes, print() prints the videos that have been checked, ids() displays the video ID below each video.

+ <b>bokehPeaks.html:</b>  Generates Bokeh graphs of video views with the peaks highlighted as red points.

+ <b>bruteforce.py:</b>  Uses brute force algorithm to search for peaks.

+ <b>code.json:</b> List of all the video IDs

+ <b>commonWords.txt:</b>  Text file of common words.
 
+ <b>create_intervals.py:</b> Creates a json file with the number of views at each second of every video.
 
+ <b>data.json:</b> Dictionary of dictionaries of all the video IDs and their view segments.

+ <b>data.py:</b> Creates a json file with a dictionary of dictionaries of all the video IDs, view segments, view count, and length of video.

+ <b>finalData.json:</b> Dictionary of dictionaries of all the video IDs, view segments, view count, and length of each video.

+ <b>finalData.py:</b> Functions that clean up the raw student data, calculates rewatch counts, and calculates unique counts.

+ <b>graph analysis.py:</b> 

+ <b>graphAnalysis.py:</b> 

+ <b>graphScripts.txt:</b>  

FinishedCourseData Folder:

+ <b>allPauses.json:</b> dictionary where keys are video IDs and values are lists of times during the video when students  pressed pause.

+ <b>allPlays.json:</b> dictionary where keys are video IDs and values are lists of times during the video when students  pressed play.

+ <b>pausePlay.json:</b> dictionary where keys are video IDs and values are lists of tuples: (when the student pressed pause, how long they paused for). 

+ <b>pauseBins.json:</b> sorts allPauses.json into bins.

+ <b>playBins.json:</b> sorts allPlays.json into bins.

+ <b>pausePlayBins.json:</b> sorts pausePlay.json into bins.

videoTranscripts Folder:

+ <b>commonWords.txt:</b> Text file of common English words.
 
+ <b>csvToDict.py:</b> CSV into Dictionary (work in progress)

+ <b>transcripts.py:</b> Gets the video transcript at a given second.

+ <b>transcriptsOrderedWords.json:</b> JSON file of video word frequencies with words ordered alphabetically.

+ <b>transcriptsParagraph.json:</b> JSON file of video transcripts in paragraph form.

+ <b>transcriptsSentences.json:</b> JSON file of video transcripts as a list of sentences.

+ <b>transcriptsTime.json:</b> JSON file file of video transcripts with start, duration and corresponding transcript sentences.

+ <b>transcriptsWordFrequency.json:</b> JSON file of video word frequencies ordered by most frequent.

+ <b>transcriptsXML.json:</b> JSON file of video transcipts in XML form.

+ <b>videoTranscripts.py:</b> Gets video transcripts, cleans them, and creates video transcript json files.

+ <b>views.py:</b> Creates a list of dictionaries for one video which contain info about the number of views at each second

+ <b>views_lineChart.py:</b> Creates a line chart with Bokeh to show the peaks in video views

+ <b>views_peaks.py:</b> Creates a line chart with matplotliv where all the peaks are marked on the graph

***********************************************
***** Created by the DAV-Lab, Summer 2015 *****
***********************************************
