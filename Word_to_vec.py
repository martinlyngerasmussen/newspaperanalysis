# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 12:23:24 2019

@author: azqueta
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:17:33 2019

@author: azqueta
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:58:33 2018
6669 Articles
@author: azqueta
"""
## Libraries to download
from nltk.tokenize import RegexpTokenizer
#from nltk.corpus import stopwords
#from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from gensim import corpora, models
import gensim
import csv

#from gensim.parsing.preprocessing import STOPWORDS

## Tokenizing
tokenizer = RegexpTokenizer(r'\w+')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()


## Reading the data

import json
#import nltk
#import re
import pandas

appended_data = []

for i in range(1,35):
    df1 = pandas.DataFrame([json.loads(l) for l in open('NYT_%d.json' % i)])
    appended_data.append(df1)
    

appended_data = pandas.concat(appended_data)
# doc_set = df1.body

doc_set = appended_data.body

print(len(doc_set))

## French Stopwords
German_Stopwords = open("German_Stopwords.txt").read()
German_Stopwords1=German_Stopwords.split('\n')


# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)
    
    # remove all tokens that are not alphabetic
    words = [word for word in tokens if word.isalpha()]

    # remove stop words from tokens
    #stopped_tokens = [i for i in tokens if not i in en_stop]
    #stopped_tokens = [i for i in words if not i in German_Stopwords1]
    
    # stem tokens
    #stemmed_tokens = [sbGerman.stem(i) for i in stopped_tokens]
    
    # add tokens to list
    texts.append(words)


model = gensim.models.Word2Vec(
    texts,
    size=150,
    window=10,
    min_count=2,
    workers=10)

model.train(texts, total_examples=len(texts), epochs=10)


# Once the model is trained, I could obtain the relationship of words per each month
#w1 = "growth"
#model.wv.most_similar(positive=w1)

#model.wv.similarity(w1="bad", w2="futur")

#w1 = "inflation"
#result = model.wv.most_similar(positive=w1)
#print(result)

# Similarity between Inflation and tomorrow

model.wv.similarity(w1="inflation", w2="zukunft")


#result = model.most_similar(positive=['econom', 'futur'], negative=['negativ'], topn=1)
#print(result)



