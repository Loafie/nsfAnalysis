# NSF Award Abstract Lexical and Semantic Analysis Script

This software was built ad-hoc as research questions developed and is in no way structurally or algorithmically optimized. It is offered as-is.

## Usage Instructions:

- Download __stop_words_english.txt__ from [https://countwordsfree.com/stopwords](https://countwordsfree.com/stopwords) and place it in the root repo directory.

- Download all NSF award archives from 1990-2021 from [https://nsf.gov/awardsearch/download.jsp](https://nsf.gov/awardsearch/download.jsp) and extract them all to a subfolder called __awards__.

- Download __crawl-300d-2M.vec.zip__ from [https://fasttext.cc/docs/en/english-vectors.html](https://fasttext.cc/docs/en/english-vectors.html) and extact the file to a subfolder called __embeddings__.

- Run __nsfProcessAndPackage.py__ - _(This will take a while, but only needs to be done once initially.)_

- Run __nsfAnalyze.py__ - _(This will also take a while.)_

- Run __nsfCountPlotter.py__ - _(This will yield all of the graphs used in the publication.)_


