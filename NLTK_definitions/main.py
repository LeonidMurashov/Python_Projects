from nltk.corpus import wordnet as wn
from nltk.tokenize import WordPunctTokenizer
import json

tokenizer = WordPunctTokenizer()
positions = {}
stop_words = ['-', 'and', 'of','the', 'for', ')', '(', '\'', '\'-']
with open("defs.txt",'w') as output:
	for row in open("imagenet_comp_graph_label_strings.txt"):
		row = row.strip()
		words = tokenizer.tokenize(row)
		arr_words = {}
		for word in [i for i in words if i not in stop_words]:
			try:
				syns = wn.synsets(word)
				assert len(syns) != 0
				syns = syns[:min(len(syns),3)]
				defs = [i.definition() for i in syns]
				arr_words[word] = defs
			except:
				print("Error in", word)

		positions[row] = arr_words
	output.write(json.dumps(positions))
			#print(wn.synset('dog.n.01')).

