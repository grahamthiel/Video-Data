# -*- coding: utf-8 -*-
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import json
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

"""
wordFreq = open('../Video-Data/videoTranscripts/transcriptsWordFrequency.json').read()
wordFreqDict = json.loads(wordFreq)
wordFreqList = wordFreqDict.values()
vocabList=[]
for i in wordFreqList:
    vocabList.append(i[0][0])
    
vocabList = set(vocabList)
"""
class LemmaTokenizer(object):
     def __init__(self):
         self.wnl = WordNetLemmatizer()
     def __call__(self, doc):
         return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]
wordFreqDict = json.load(open('../Video-Data/videoTranscripts/transcriptNewWordFreq.json'))
vocabs = []
for key in wordFreqDict:
    vocabs.extend(wordFreqDict[key].keys())
    
vocabList = list(set(vocabs))

textFilesList = os.listdir(os.getcwd())
textFilesList.pop(0)
commonWords = open('../Video-Data/videoTranscripts/commonWords.txt','r').readlines()
commonWordsList = []
for i in commonWords:
    commonWordsList.append(i.replace('\n',''))

d = Counter()
for key in wordFreqDict:
    vD = wordFreqDict[key]
    d.update(vD)

filenames = textFilesList
##
vectorizer = CountVectorizer(input='filename',lowercase=True,vocabulary=vocabList,stop_words=commonWordsList,tokenizer=LemmaTokenizer() )
dtm = vectorizer.fit_transform(filenames)
#vocab = vectorizer.get_feature_names()
dtm = dtm.toarray() 
#vocab = np.array(vocab)
#
#import lda
#dtm.shape

#vocab = lda.datasets.load_reuters_vocab()
#titles = lda.datasets.load_reuters_titles()
#X.shape
#
#model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
#model.fit(X)
#topic_word = model.topic_word_  # model.components_ also works
#n_top_words = 8
#for i, topic_dist in enumerate(topic_word):
#     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
#     print('Topic {}: {}'.format(i, ' '.join(topic_words)))
