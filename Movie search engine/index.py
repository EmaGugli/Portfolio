import string
from collections import defaultdict
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

d = 20000  # number of documents to analyze
invdict = defaultdict(list)
voc = {}
count = 0
for j in range(d):
    # handle error if file is not present
    try:
        tsvfile = open(r"C:\Users\39335\Desktop\GitHub\HW3\tsv\article_" + str(j) + ".tsv", "r")
    except:
        continue

    reader = tsvfile.readlines()
    text = []

    # transform the paragraph in a list with all the words
    for row in reader:
        text += row.split()

    sw = set(stopwords.words('english'))
    ps = PorterStemmer()
    # Preprocess the words

    for k in range(len(text)):
        # remove stop words
        text[k] = text[k].lower()
        if text[k] in sw:
            text[k] = ""

        # remove punctuation
        table = str.maketrans(dict.fromkeys(string.punctuation))
        text[k] = text[k].translate(table)

        # stemming
        text[k] = ps.stem(text[k])

    # We create a vocabulary that pairs each word to an ID.
    # We make a inverted index where the key is the ID of the word and the value is a list of the ID
    # of the documents that word is present

    # Remove empty elements
    text[:] = [x for x in text if x != ""]

    for word in text:

        # create vocabulary
        if not word in voc:
            voc[word] = count
            count += 1

        # create inverted dictionary
        if j in invdict[voc[word]]:
            continue
        invdict[voc[word]].append(j)

    tsvfile.close()

# I now save the results in txt files so I can use them to search for the query later.
with open("Vocabulary.txt", "w") as f:
    f.write(json.dumps(voc))
with open("InvertedDict.txt", "w") as f:
    f.write(json.dumps(invdict))