#encoding: utf8

import nltk
import re

from nltk.probability import FreqDist
from cltk.tokenize.word import WordTokenizer

##determines 100 most common words and number of occurrences in the French corpus
##ignores punctuation and upper-case
file_content = open("~/cltk/stop/french/frenchtexts.txt").read()
from cltk.tokenize.word import WordTokenizer

word_tokenizer = WordTokenizer('french')
words = word_tokenizer.tokenize(file_content)
fdist = FreqDist(words)
##prints 100 most common words
common_words=fdist.most_common(125)
cw_list = [x[0] for x in common_words]
##outputs 100 most common words to .txt file
with open('french_prov_stops.txt', 'a') as f:
    for item in cw_list:
        print(item, file=f)

