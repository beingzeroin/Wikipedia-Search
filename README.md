# Wikipedia Search

A simple search engine on the Wikipedia dump based on inverted index and postings list. Secondary index allows this to be scaled for large corpora.

## Usage:

* python index. py
    * Creates the index in index/. This creates a primary and secondary index to speed up search. The indices are made for separate fields: title,      body, infobox, references, external links and categories. This is done to enable faster multi-field queries.
* python search.py
    * Search query terms. Multi-field queries are given as: <field1>:<search term>, <field2>:<search_term>,..


