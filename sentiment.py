import nltk

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

n_instances = 100
subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
len(subj_docs), len(obj_docs)
(100, 100)
Each document is represented by a tuple (sentence, label). The sentence is tokenized, so it is represented by a list of strings:

>>> subj_docs[0]
(['smart', 'and', 'alert', ',', 'thirteen', 'conversations', 'about', 'one',
'thing', 'is', 'a', 'small', 'gem', '.'], 'subj')
We separately split subjective and objective instances to keep a balanced uniform class distribution in both train and test sets.

>>> train_subj_docs = subj_docs[:80]
>>> test_subj_docs = subj_docs[80:100]
>>> train_obj_docs = obj_docs[:80]
>>> test_obj_docs = obj_docs[80:100]
>>> training_docs = train_subj_docs+train_obj_docs
>>> testing_docs = test_subj_docs+test_obj_docs
>>> sentim_analyzer = SentimentAnalyzer()
>>> all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])
We use simple unigram word features, handling negation:

>>> unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
>>> len(unigram_feats)
83
>>> sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
We apply features to obtain a feature-value representation of our datasets:

>>> training_set = sentim_analyzer.apply_features(training_docs)
>>> test_set = sentim_analyzer.apply_features(testing_docs)
We can now train our classifier on the training set, and subsequently output the evaluation results:

>>> trainer = NaiveBayesClassifier.train
>>> classifier = sentim_analyzer.train(trainer, training_set)
Training classifier
>>> for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
...     print('{0}: {1}'.format(key, value))
Evaluating NaiveBayesClassifier results...
Accuracy: 0.8
F-measure [obj]: 0.8
F-measure [subj]: 0.8
Precision [obj]: 0.8
Precision [subj]: 0.8
Recall [obj]: 0.8
Recall [subj]: 0.8
Vader

>>> from nltk.sentiment.vader import SentimentIntensityAnalyzer
>>> sentences = ["VADER is smart, handsome, and funny.", # positive sentence example
...    "VADER is smart, handsome, and funny!", # punctuation emphasis handled correctly (sentiment intensity adjusted)
...    "VADER is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
...    "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
...    "VADER is VERY SMART, handsome, and FUNNY!!!",# combination of signals - VADER appropriately adjusts intensity
...    "VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!!",# booster words & punctuation make this close to ceiling for score
...    "The book was good.",         # positive sentence
...    "The book was kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
...    "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
...    "A really bad, horrible book.",       # negative sentence with booster words
...    "At least it isn't a horrible book.", # negated negative sentence with contraction
...    ":) and :D",     # emoticons handled
...    "",              # an empty string is correctly handled
...    "Today sux",     #  negative slang handled
...    "Today sux!",    #  negative slang with punctuation emphasis handled
...    "Today SUX!",    #  negative slang with capitalization emphasis
...    "Today kinda sux! But I'll get by, lol" # mixed sentiment example with slang and constrastive conjunction "but"
... ]
>>> paragraph = "It was one of the worst movies I've seen, despite good reviews. \
... Unbelievably bad acting!! Poor direction. VERY poor production. \
... The movie was bad. Very bad movie. VERY bad movie. VERY BAD movie. VERY BAD movie!"
>>> from nltk import tokenize
>>> lines_list = tokenize.sent_tokenize(paragraph)
>>> sentences.extend(lines_list)
>>> tricky_sentences = [
...    "Most automated sentiment analysis tools are shit.",
...    "VADER sentiment analysis is the shit.",
...    "Sentiment analysis has never been good.",
...    "Sentiment analysis with VADER has never been this good.",
...    "Warren Beatty has never been so entertaining.",
...    "I won't say that the movie is astounding and I wouldn't claim that \
...    the movie is too banal either.",
...    "I like to hate Michael Bay films, but I couldn't fault this one",
...    "It's one thing to watch an Uwe Boll film, but another thing entirely \
...    to pay for it",
...    "The movie was too good",
...    "This movie was actually neither that funny, nor super witty.",
...    "This movie doesn't care about cleverness, wit or any other kind of \
...    intelligent humor.",
...    "Those who find ugly meanings in beautiful things are corrupt without \
...    being charming.",
...    "There are slow and repetitive parts, BUT it has just enough spice to \
...    keep it interesting.",
...    "The script is not fantastic, but the acting is decent and the cinematography \
...    is EXCELLENT!",
...    "Roger Dodger is one of the most compelling variations on this theme.",
...    "Roger Dodger is one of the least compelling variations on this theme.",
...    "Roger Dodger is at least compelling as a variation on the theme.",
...    "they fall in love with the product",
...    "but then it breaks",
...    "usually around the time the 90 day warranty expires",
...    "the twin towers collapsed today",
...    "However, Mr. Carter solemnly argues, his client carried out the kidnapping \
...    under orders and in the ''least offensive way possible.''"
... ]
>>> sentences.extend(tricky_sentences)
>>> sid = SentimentIntensityAnalyzer()
>>> for sentence in sentences:
...     print(sentence)
...     ss = sid.polarity_scores(sentence)
...     for k in sorted(ss):
...         print('{0}: {1}, '.format(k, ss[k]), end='')
...     print()
VADER is smart, handsome, and funny.
compound: 0.8316, neg: 0.0, neu: 0.254, pos: 0.746,
VADER is smart, handsome, and funny!
compound: 0.8439, neg: 0.0, neu: 0.248, pos: 0.752,
VADER is very smart, handsome, and funny.
compound: 0.8545, neg: 0.0, neu: 0.299, pos: 0.701,
VADER is VERY SMART, handsome, and FUNNY.
compound: 0.9227, neg: 0.0, neu: 0.246, pos: 0.754,
VADER is VERY SMART, handsome, and FUNNY!!!
compound: 0.9342, neg: 0.0, neu: 0.233, pos: 0.767,
VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!!
compound: 0.9469, neg: 0.0, neu: 0.294, pos: 0.706,
The book was good.
compound: 0.4404, neg: 0.0, neu: 0.508, pos: 0.492,
The book was kind of good.
compound: 0.3832, neg: 0.0, neu: 0.657, pos: 0.343,
The plot was good, but the characters are uncompelling and the dialog is not great.
compound: -0.7042, neg: 0.327, neu: 0.579, pos: 0.094,
A really bad, horrible book.
compound: -0.8211, neg: 0.791, neu: 0.209, pos: 0.0,
At least it isn't a horrible book.
compound: 0.431, neg: 0.0, neu: 0.637, pos: 0.363,
:) and :D
compound: 0.7925, neg: 0.0, neu: 0.124, pos: 0.876,
<BLANKLINE>
compound: 0.0, neg: 0.0, neu: 0.0, pos: 0.0,
Today sux
compound: -0.3612, neg: 0.714, neu: 0.286, pos: 0.0,
Today sux!
compound: -0.4199, neg: 0.736, neu: 0.264, pos: 0.0,
Today SUX!
compound: -0.5461, neg: 0.779, neu: 0.221, pos: 0.0,
Today kinda sux! But I'll get by, lol
compound: 0.2228, neg: 0.195, neu: 0.531, pos: 0.274,
It was one of the worst movies I've seen, despite good reviews.
compound: -0.7584, neg: 0.394, neu: 0.606, pos: 0.0,
Unbelievably bad acting!!
compound: -0.6572, neg: 0.686, neu: 0.314, pos: 0.0,
Poor direction.
compound: -0.4767, neg: 0.756, neu: 0.244, pos: 0.0,
VERY poor production.
compound: -0.6281, neg: 0.674, neu: 0.326, pos: 0.0,
The movie was bad.
compound: -0.5423, neg: 0.538, neu: 0.462, pos: 0.0,
Very bad movie.
compound: -0.5849, neg: 0.655, neu: 0.345, pos: 0.0,
VERY bad movie.
compound: -0.6732, neg: 0.694, neu: 0.306, pos: 0.0,
VERY BAD movie.
compound: -0.7398, neg: 0.724, neu: 0.276, pos: 0.0,
VERY BAD movie!
compound: -0.7616, neg: 0.735, neu: 0.265, pos: 0.0,
Most automated sentiment analysis tools are shit.
compound: -0.5574, neg: 0.375, neu: 0.625, pos: 0.0,
VADER sentiment analysis is the shit.
compound: 0.6124, neg: 0.0, neu: 0.556, pos: 0.444,
Sentiment analysis has never been good.
compound: -0.3412, neg: 0.325, neu: 0.675, pos: 0.0,
Sentiment analysis with VADER has never been this good.
compound: 0.5228, neg: 0.0, neu: 0.703, pos: 0.297,
Warren Beatty has never been so entertaining.
compound: 0.5777, neg: 0.0, neu: 0.616, pos: 0.384,
I won't say that the movie is astounding and I wouldn't claim that the movie is too banal either.
compound: 0.4215, neg: 0.0, neu: 0.851, pos: 0.149,
I like to hate Michael Bay films, but I couldn't fault this one
compound: 0.3153, neg: 0.157, neu: 0.534, pos: 0.309,
It's one thing to watch an Uwe Boll film, but another thing entirely to pay for it
compound: -0.2541, neg: 0.112, neu: 0.888, pos: 0.0,
The movie was too good
compound: 0.4404, neg: 0.0, neu: 0.58, pos: 0.42,
This movie was actually neither that funny, nor super witty.
compound: -0.6759, neg: 0.41, neu: 0.59, pos: 0.0,
This movie doesn't care about cleverness, wit or any other kind of intelligent humor.
compound: -0.1338, neg: 0.265, neu: 0.497, pos: 0.239,
Those who find ugly meanings in beautiful things are corrupt without being charming.
compound: -0.3553, neg: 0.314, neu: 0.493, pos: 0.192,
There are slow and repetitive parts, BUT it has just enough spice to keep it interesting.
compound: 0.4678, neg: 0.079, neu: 0.735, pos: 0.186,
The script is not fantastic, but the acting is decent and the cinematography is EXCELLENT!
compound: 0.7565, neg: 0.092, neu: 0.607, pos: 0.301,
Roger Dodger is one of the most compelling variations on this theme.
compound: 0.2944, neg: 0.0, neu: 0.834, pos: 0.166,
Roger Dodger is one of the least compelling variations on this theme.
compound: -0.1695, neg: 0.132, neu: 0.868, pos: 0.0,
Roger Dodger is at least compelling as a variation on the theme.
compound: 0.2263, neg: 0.0, neu: 0.84, pos: 0.16,
they fall in love with the product
compound: 0.6369, neg: 0.0, neu: 0.588, pos: 0.412,
but then it breaks
compound: 0.0, neg: 0.0, neu: 1.0, pos: 0.0,
usually around the time the 90 day warranty expires
compound: 0.0, neg: 0.0, neu: 1.0, pos: 0.0,
the twin towers collapsed today
compound: -0.2732, neg: 0.344, neu: 0.656, pos: 0.0,
However, Mr. Carter solemnly argues, his client carried out the kidnapping under orders and in the ''least offensive way possible.''
compound: -0.5859, neg: 0.23, neu: 0.697, pos: 0.074,
