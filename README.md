# MachineTranslation

sentiment.py - naive sentiment analyzer, outputs sentiment for each of the test tweets <br />
sample.csv - random 10,000 tweets obtained from training dataset <br />
MAGA_tweets.csv - tweets with #MAGA, used as testing dataset <br />

twitter-sentiment-classifier:
getsample.py - create sample of dataset
getsentiwordnet.py - get pos/neg words from sentiwordnet
preprocess.py - text preprocessing
sentiment.py - sentiment analyzer, outputs accuracy

bot.py: finds_trends() finds trends by location, and tweet() updates the bot status
scrape_google.py: scrape_for_links() returns Google News links for a search term, get_keywords_from_link() returns the keywords from the url of a link
gettweet.py: gets tweets by username and by hashtag
