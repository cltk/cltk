"""
This list was compiled from the 100 most frequently occurring words in the french_text corpus, with
content words removed. It also includes forms of auxiliary verbs taken from Anglade (1931) and retrieved
from https://fr.wikisource.org/wiki/Grammaire_élémentaire_de_l’ancien_français (available under a
Attribution-ShareAlike 3.0 Creative Commons license.

Code used to determine most frequent words in the corpus:

import nltk
import re
from nltk.probability import FreqDist
from cltk.tokenize.word import WordTokenizer
determines 100 most common words and number of occurrences in the French corpus
ignores punctuation and upper-case
file_content = open("~/cltk/cltk/stop/french/frenchtexts.txt").read()
from cltk.tokenize.word import WordTokenizer

word_tokenizer = WordTokenizer('french')
words = word_tokenizer.tokenize(file_content)
fdist = FreqDist(words)
prints 100 most common words
common_words=fdist.most_common(125)
cw_list = [x[0] for x in common_words]
outputs 100 most common words to .txt file
with open('french_prov_stops.txt', 'a') as f:
    for item in cw_list:
        print(item, file=f)
"""



STOPS_LIST = ["et",
              "a",
              "de",
              "li",
              "la",
              "ne",
              "que",
              "en",
              "le",
              "e",
              "il",
              "si",
              "qui",
              "est",
              "par",
              "se",
              "les",
              "bien",
              "vos",
              "grant",
              "je",
              "me",
              "sa",
              "l'",
              "quant",
              "tant",
              "i",
              "un",
              "plus",
              "por",
              "ce",
              "mes",
              "qu’il",
              "son",
              "fu",
              "cil",
              "or",
              "mult",
              "sun",
              "vous",
              "au",
              "fait",
              "an",
              "molt",
              "mais",
              "lui",
              "ki",
              "une",
              "dist",
              "qu'",
              "ja",
              "car",
              "ou",
              "ses",
              "d'",
              "n'",
              "ad",
              "des",
              "puis",
              "pas",
              "ot",
              "dit",
              "el",
              "vus",
              "s'",
              "tu",
              "ele",
              "del",
              "fet",
              "sire",
              "lor",
              "mon",
              "sont",
              "pour",
              "s’en",
              "tot",
              "tel",
              "te",
              "dame",
              "n’i",
              "vostre",
              "ma",
              "estoit",
              "estre",
              "as",
              "ie",
              "u",
              "du",
              "faire",
              "nos",
              "m'",
              "mal",
              "sunt",
              "al",
              "moi",
              "devant",
              "avoit",
              "ert",
              "tout",
              "fors",
              "lur",
              "rien",
              "sur",
              "vers",
              "dieu",
              "fut",
              "n’",
              "en",
              "soit",
              "nus",
              "vint",
              "cele",
              "fist",
              "trop",
              "sui",
              "es",
              "ies",
              "est",
              "somes",
              "estes",
              "sont",
              "ere",
              "iere",
              "eres",
              "ieres",
              "eret",
              "ieret",
              "eriens",
              "eriez",
              "erent",
              "irent",
              "fui",
              "fus",
              "fut",
              "fumes",
              "fustes",
              "furent",
              "ier",
              "iers",
              "iert",
              "ert",
              "ermes",
              "ertes",
              "ierent",
              "sereie",
              "seroie",
              "sereies",
              "sereiet",
              "sereit",
              "seriiens",
              "seriiez",
              "sereient",
              "seie",
              "seies",
              "seiet",
              "seit",
              "seiens",
              "seiez",
              "seient",
              "estant",
              "esté",
              "oi",
              "oüs",
              "eüs",
              "óut",
              "ot",
              "oümes",
              "eümes",
              "oüstes",
              "eüstes",
              "óurent",
              "orent",
              "ai",
              "as",
              "a",
              "at",
              "avons",
              "avez",
              "ont",
              "d'",]
              
