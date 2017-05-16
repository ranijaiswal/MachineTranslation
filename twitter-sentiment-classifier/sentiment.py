import sys
import csv, random
import nltk
# import tweet_features, tweet_pca
import getsentiwordnet
import preprocess

reload(sys)
sys.setdefaultencoding('utf8')

# read all tweets and labels
fp = open( 'sample.csv', 'rb' )
reader = csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )
tweets = []
for row in reader:
    tweets.append( [row[0], row[1]] );

# delete non-utf8 characters
for t in tweets:
	t[0]=t[0].decode('utf-8','ignore').encode("utf-8")

for t in tweets:
	if t[1] == '0':
		t[1] = 'negative'
	else:
		t[1] = 'positive'

# text preprocessing
for t in tweets:
	t[0] = preprocess.sen_preprocess(t[0])

# split into training and test sets
random.shuffle( tweets );

print tweets[100]
print tweets[200]


fvecs = [(getsentiwordnet.make_tweet_dict(t),s) for (t,s) in tweets]
v_train = fvecs[:9000]
v_test  = fvecs[9000:]


# apply PCA reduction
#(v_train, v_test) = \
#        tweet_pca.tweet_pca_reduce( v_train, v_test, output_dim=1.0 )


# train classifier
classifier = nltk.NaiveBayesClassifier.train(v_train);


# classify and get accuracy
print '\nAccuracy %f\n' % nltk.classify.accuracy(classifier, v_test)

