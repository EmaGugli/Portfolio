from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer
import json
import pandas as pd
import numpy as np
import math
import sys
import io

ps = PorterStemmer()
d = 20000   # Number of documents
# Now we find all the documents that have all the words in the query.
# The search engine will be a function that takes as input the query. If we need the ID of the document (for example in ex 2.2.2) the second argument should be ID=True.
def SearchEngine1(q, ID=False):
    query = []

    # We need to stem the word of the query
    for word in q:
        query.append(ps.stem(word))

    querydict = {}
    for word in query:
        if word in vocab:
            querydict[word] = vocab[word]
        else:
            print("The word %s was not found" % word)
    l = []
    for i in inverted:
        for ele in query:
            if i == str(querydict[ele]):
                l.append(inverted[i])

    # I want to find the intersection between the lists of documents ID that contain the query
    # (the documents that contains all the words we want)
    inter = set(l[0])
    for i in range(1, len(l)):
        inter = inter.intersection(set(l[i]))
    if len(inter) == 0:
        print("No documents satisfy all the elements in the query.")
        sys.exit()

    # Inter is a set with the ID of the documents we need, now we open the html for each and extract the info we need.
    # I want to make 3 lists with title, intro and url for each movie that satisfies the query and then make a dataframe.
    title = []
    introduction = []
    url = []

    for doc in inter:
        file = open(r'C:\Users\39335\Desktop\GitHub\HW3\Pages\Dataarticle_' + str(doc) + '.html', 'r', encoding="utf-8")
        s1 = file.read()
        soup = BeautifulSoup(s1, 'html')
        try:
            t = soup.title.text.strip('- Wikipedia')
        except:
            t = "NA"
        title.append(t)

        intro = ""
        try:
            start1 = soup.find('table')
            for elem in start1.next_siblings:
                if elem.name == 'h2':
                    break
                if elem.name != 'p':
                    continue
                intro1 = elem.text
                intro = intro + intro1
                intro = intro.strip('\n')
        except:
            intro = "NA"
        introduction.append(intro)
        u = "https://en.wikipedia.org/wiki/" + t
        u = u.replace(" ", "_")
        url.append(u)

    # Make the data frame
    if ID == True:
        result = np.transpose(pd.DataFrame(np.array([title, introduction, url, list(inter)])))
        result.columns = ["Title", "Intro", "Wikipedia Url", "Document ID"]
    else:
        result = np.transpose(pd.DataFrame(np.array([title, introduction, url])))
        result.columns = ["Title", "Intro", "Wikipedia Url"]

    return (result)
def SearchEngine2(q):
    for word in q:  # stem the query
        word = ps.stem(word)
    df = SearchEngine1(q, ID=True)
    sim = []

    for ele in df["Document ID"]:
        qtfIdf = queryTFIDF(q)
        doctfIdf = tfIdf(q, ele)
        cosim = (np.dot(qtfIdf, doctfIdf) / (np.linalg.norm(qtfIdf) * np.linalg.norm(doctfIdf)))
        sim.append(cosim)

    df.insert(3, "Similarity", sim, True)
    df = df.round({"Similarity": 3})
    df.drop(columns="Document ID", inplace=True)
    k = 3  # how many documents we want to see
    df = df.sort_values(by='Similarity', kind='heapsort',
                        ascending=False)  # Use heap data structure as a sorting algorithm
    return (df.head(k))
def SearchEngine3(q):
    for word in q:           #stem the query
        word = ps.stem(word)
    df = SearchEngine1(q, ID = True)
    BoxOffice = []

    for ele in df["Document ID"]:
        filename=r'C:\Users\39335\Desktop\GitHub\HW3\Pages\Dataarticle_'+str(ele)+'.html'
        with io.open(filename,'r', encoding="utf-8") as f:
            s1=f.read()
            soup = BeautifulSoup(s1, 'html')
        tab=soup.find('table',class_='infobox vevent')
        box = ""
        boxdic = {}

        for r in tab.find_all('tr'):
            td1 = r.find("td")
            if td1 != None:
                s1 = td1
                p1 = r.find("th")
                if p1!=None:
                    boxdic[p1.text.strip("\n")] = s1.text.strip("\n")
        try:
            box = boxdic['Budget']
        except:
            boxdic['Budget'] = "NA"

        BoxOffice.append(box)
    df.insert(3, "Budget", BoxOffice, True)
    df.drop(columns="Document ID", inplace=True)
    k = 3  #how many documents we want to see
    df = df.sort_values(by='Budget', kind='heapsort', ascending=False)
    return (df.head(k))


# Calculate the tfIdf s for all the terms in a document
def tfIdf(terms, documentID):
    tfidf = []
    # Evaluate Term Frequency
    tsvfile = open(r"C:\Users\39335\Desktop\GitHub\HW3\tsv\article_" + str(documentID) + ".tsv", "r")
    reader = tsvfile.readlines()
    text = []

    # transform the paragraph in a list with all the words
    for row in reader:
        text += row.split()

    sw = set(stopwords.words('english'))
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

    # Remove empty elements
    text[:] = [x for x in text if x != ""]

    for term in terms:
        tf = (text.count(term) / float(len(text)))

        # Evaluate Inverse Document Frequency
        numDocumentsWithTerm = len(SearchEngine1([term]))
        if numDocumentsWithTerm > 0:
            idf = 1.0 + math.log(d / numDocumentsWithTerm)
        else:
            idf = 1.0

        tfidf.append(tf * idf)
    return tfidf
# Returns a list with the tfIdf for each work in the query calculated in the query itself
def queryTFIDF(q):
    tfidf = []
    for i in range(len(q)):
        tfidf.append((1 / len(q) * (1 + math.log(len(q)))))
    return tfidf


# We need to pen the file with the vocabulary and the inverted dictionary
with open('Vocabulary.txt', 'r') as v:
    vocab = json.load(v)
with open('InvertedDict.txt', 'r') as i:
    inverted = json.load(i)

print("What search engine do you want to use? (1-Standard, 2-Sorted bu cosine similarity, 3-Sorted by budget")
search_engine = int(input())
print("Insert the query to search. (Insert the words separated by a space)")
q = input().split()

if search_engine == 1:
    SearchEngine1(q)
if search_engine == 2:
    SearchEngine2(q)
if search_engine == 3:
    SearchEngine3(q)
