# Introduction
I made this code in function of my bachelor thesis. In my bachelor thesis I researched creating a search engine with an inverted index.

# files
### formatter_SQLite.py
This Python script converts data from XML files I got from `http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm` to an SQLite database.

### invertedIndex7.py
This Python script is the last iteration of my code to create an inverted index table from the dataset.

### nlp.py
This file contains a class NLP which handles all the Natural Language Processing for both creating my inverted index and processing my search terms

### idf-calc7.py
This Python script adds the TF-IDF score to the indexed table. THis is done after the indexation.

### searching.py
This running this script you can enter search terms and they will be searched.

### search_inverted_index.py
This script contains all SQL queries needed for the search