import nltk

from nltk import *
# from nltk.probability import FreqDist, DictionaryProbDist, ELEProbDist

# http://thinknook.com/twitter-sentiment-analysis-training-corpus-dataset-2012-09-22/
# DATASET IS FROM ABOVE LINK ^
import csv

alltweets = {}
pos_tweets = []
neg_tweets = []
with open('Sentiment Analysis Dataset 2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        alltweets[row[0]] = row[2]
        if row[1] == '1':
            pos_tweets.append((row[2],'positive'))
        elif row[1] == '0':
            neg_tweets.append((row[2],'negative'))
pos_tweets = pos_tweets[:10000]
neg_tweets = neg_tweets[:10000]

# get training tweets
# pos_tweets = [('I love this car', 'positive'),
#               ('This view is amazing', 'positive'),
#               ('I feel great this morning', 'positive'),
#               ('I am so excited about the concert', 'positive'),
# 	          ('He is my best friend', 'positive')]

# neg_tweets = [('I do not like this car', 'negative'),
#               ('This view is horrible', 'negative'),
#               ('I feel tired this morning', 'negative'),
#               ('I am not looking forward to the concert', 'negative'),
#               ('He is my enemy', 'negative')]

tweets = []

for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

# get test tweets

# test_tweets = [
#     (['feel', 'happy', 'this', 'morning'], 'positive'),
#     (['larry', 'friend'], 'positive'),
#     (['not', 'like', 'that', 'man'], 'negative'),
#     (['house', 'not', 'great'], 'negative'),
#     (['your', 'song', 'annoying'], 'negative')]

# classifier

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

word_features = get_word_features(get_words_in_tweets(tweets))

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

# contains the labeled feature sets. list of tuples which each tuple containing the feature dictionary and the sentiment/label for each tweet.
training_set = nltk.classify.apply_features(extract_features, tweets)
# print(training_set)

classifier = nltk.NaiveBayesClassifier.train(training_set)

def train(labeled_featuresets, estimator=ELEProbDist):
    ...
    # Create the P(label) distribution
    label_probdist = estimator(label_freqdist)
    ...
    # Create the P(fval|label, fname) distribution
    feature_probdist = {}
    ...
    return (label_probdist, NaiveBayesClassifier(label_probdist, feature_probdist))

# print(classifier.show_most_informative_features(32))
print("Trained")

tweet = 'way to go'
print(classifier.classify(extract_features(tweet.split())))
