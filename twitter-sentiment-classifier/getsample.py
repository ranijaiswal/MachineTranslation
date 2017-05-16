import csv
import random
fp =open( 'sentiment-large.csv', 'rb' )
reader = csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )
all_tweets = []
for row in reader:
    all_tweets.append( [row[3], row[1]] );
tweets = random.sample(all_tweets, 10000)

with open('sample.csv','w') as f:
	writer = csv.writer(f)
	writer.writerow(["text","sentiment"])
	writer.writerows(tweets)