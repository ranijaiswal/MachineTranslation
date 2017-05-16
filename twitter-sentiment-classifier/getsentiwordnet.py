#use senti-wordnet
def featuredict():
	f=open("sentiwordnet.txt","r")
	sentiwordlist={}
	for line in f:
		a = line.split()
		if len(a)>5:
			if float(a[2])-float(a[3])>0.5:
				word = a[4]
				word = word[:-2]
				sentiwordlist[word]="positive"
			elif float(a[2])-float(a[3])<-0.5:
				word = a[4]
				word = word[:-2]
				sentiwordlist[word]="negative"
	return sentiwordlist

def make_tweet_dict(txt):
	sentiwordlist = featuredict()
	txtLow = ' ' + txt.lower() + ' '
	fvec = {}

    # search for each feature
	for word in sentiwordlist:
		fvec[word] = False;
		fvec[word] = fvec[word] or (txtLow.find(word) != -1)
	return fvec