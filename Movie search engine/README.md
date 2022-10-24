# Build a search engine over a list of movies that have a dedicated page on Wikipedia.

collector.ipynb: a notebook that contains the code needed to collect the data from the html page and Wikipedia.

parser.ipynb: a notebook that contains the code needed to parse the entire collection of html pages and save those in tsv files.

index.py: a python file that once executed generate two documents. The first one is the Vocabulary.txt that pairs each word to an integer. The other one is the InvertedIndex.txt that generates a document with the indices of the Search Engine.

main.py: a python file that execute one of the 3 search engines. It will ask for the kind of Search Engine we want to use and the query (words separated by a space). This file needs the documents Vocabulary.txt and InvertedIndex.txt to work.
It returns the list of the movies that best mecht the query. 
