def sen_preprocess(sentence):
	sentence = sentence[2:-1]
	words = sentence.split()

	for i in range(0,len(words)-1):
		word = words[i]
		#Remove link
		if not word.find("https:") == -1:
			del words[i]
			words.insert(i,'')
		#Remove hashtag
		if not word.find("#") == -1:
			del words[i]
			words.insert(i,'')
		#Remove 'RT'
		if not word.find("RT") == -1:
			del words[i]
			words.insert(i,'')
		#Remove '@'
		if not word.find("@") == -1:
			del words[i]
			words.insert(i,'')
		#Stop word removal
		if word =='a' or word =='and'or word == 'is' or word=='on' or word=='in' or\
			word=='of' or word=='or' or word=='at' or word=='the' or word=='was' or\
			word=='with':
			del words[i]
			words.insert(i,'')


	newsentence = ''
	for i in range(0, len(words)-1):
		if not words[i] == '':
			newsentence+=' '
			newsentence+=words[i]
	return newsentence