# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:58:33 2018
4503 articles
@author: azqueta
"""
## Libraries to download
from nltk.tokenize import RegexpTokenizer
#from nltk.corpus import stopwords
#from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

#from gensim.parsing.preprocessing import STOPWORDS

## Tokenizing
tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
#en_stop = stopwords.words('english')
#stop_words = set(stopwords.words('english'))

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

## Reading the data

import json
import nltk
import re
import pandas

appended_data = []

for i in range(1,2):
    df0 = pandas.DataFrame([json.loads(l) for l in open('ChinaFinancialRisk_%d.json' % i)])
    appended_data.append(df0)
    

appended_data = pandas.concat(appended_data)
# doc_set = df1.body

doc_set = appended_data.body

print(len(doc_set))

## English Stopwords
English_Stopwords = open("English_Stopwords.txt").read() # also contain uni-characters
English_Stopwords1=English_Stopwords.split('\n')


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
    stopped_tokens = [i for i in words if not i in English_Stopwords1]
    
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)


# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]
#The function doc2bow() simply counts the number of occurrences of each distinct word, 
#converts the word to its integer word id and returns the result as a sparse vector



# generate LDA model, need to set minimum probability to zero otherwise topics will be surpresed in the next steps
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=20, id2word = dictionary, passes=50, minimum_probability=0)
ldamodel.save("model.ldaFinanceRisk20") 
#class gensim.models.ldamodel.LdaModel(corpus=None, num_topics=100, id2word=None, distributed=False, 
#chunksize=2000, passes=1, update_every=1, alpha='symmetric', eta=None, decay=0.5, offset=1.0, eval_every=10, 
#iterations=50, gamma_threshold=0.001, minimum_probability=0.01)
#passes: optional. The number of laps the model will take through corpus. 
#The greater the number of passes, the more accurate the model will be. A lot of passes can be slow on a very large corpus.

print(ldamodel.print_topics(num_topics=20, num_words=30))


## visualization of the topics
import pyLDAvis
import pyLDAvis.gensim
pyLDAvis.enable_notebook()
pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)

vis_data = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
pyLDAvis.save_html(vis_data, 'Chinse_Financial_Risk_Topics_20.html')


## -----------------------------------------------------------------------------------------------------------##
# ------------------------------------- OBTAINING ARTICLES-TOPICS DISTRIBUTIONS -------------------------------#
## -----------------------------------------------------------------------------------------------------------##

# https://web.stanford.edu/class/stats202/content/lab18.htm very complete link with LDA information

## Here we save the topics in a readable csv file

numTopics = 20
topics = {"topic":[],"word":[],"weight":[]}
for topic in range(numTopics):
    x = ldamodel.show_topic(topic,20)
    for weight, word in x:
        topics["topic"].append(topic)
        topics["word"].append(word)
        topics["weight"].append(weight)
topics = pandas.DataFrame(topics)

topics.to_csv("topics20.csv")

# Here, we store the distribution of topics in every article

topicDists = [ ldamodel[corpus[i]] for i in range(len(corpus)) ]

# convert it into a dataframe
topic_article_Dists = pandas.DataFrame(topicDists)

# select only the probabilities for each column
topic_article_Dists = pandas.concat([topic_article_Dists[x].str[1] for x in topic_article_Dists.columns], axis=1)

# save the output as a csv file
topic_article_Dists.to_csv("Article-Topic-Distri20.csv")        
           
## Save the date in a csv file         
Date = pandas.DataFrame(appended_data.date)   
Date.to_csv("Date_20.csv")     





















