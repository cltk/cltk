#encoding : utf-8
import re
from cltk.stop.french.stops import STOPS_LIST

#fist mer nule -z pl vos certes vendroie vos mais -is end. onques combastist oceistes font? nos sire talent omnipot pense jadis
text = "par deu qui l’air fist et la mer " \
       "ne me mandez nule foiz mais " \
       "je vos di bien tristran a fais " \
       "certes je n’i vendroie mie " \
       "li rois pense que par folie " \
       "sire tristran vos aie amé " \
       "mais dé plevis ma loiauté " \
       "qui sor mon cors mete flaele " \
       "s’onques fors cil qui m’ot pucele " \
       "out m’amistié encor nul jor " \
       "se li felon de cest’enor " \
       "por qui jadis vos conbatistes " \
       "o le morhout quant l’oceïstes " \
       "li font acroire (ce me senble) " \
       "que nos amors jostent ensenble " \
       "sire vos n’en avez talent " \
       "ne je par deu omnipotent " \
       "n’ai corage de druërie "

text = text.lower()

exceptions = ["mer", "certes", "mais", "vos", "onques", "nos", "sire", "talent", "omnipotent", "jadis"]

#reduced forms

text = re.sub(r"n'", "ne ", text)
text = re.sub(r"s'", "si ", text)
text = re.sub(r"t'", "te ", text)
text = re.sub(r"qu'", "que ", text)
# l' can stand for la or lui or le
text = re.sub(r"l'", "lui ", text)
text = re.sub(r"m'", "me ", text)

#VERBS : regular grammatical forms
#être
#indic
text = re.sub(r"\bsui\b|\bies\b|\bes\b|\best\b|\bsons\b|\bsomes\b|\bestes\b|\bsont\b", "sui", text)
#subj
text = re.sub(r"eie\b|oie\b|eies\b|oies\b|eiet\b|eit\b|oit\b|eiens\b|oions\b|eiez\b|"
              r"oiez\b|eient\b|oient\b", "", text)
#infinitive
text = re.sub(r"er\b", "", text)
text = re.sub(r"re\b", "", text)
# indicative - 2s, 3s, 1pl, 2pl, 3pl
text = re.sub(r"\Bes\b", "", text) # problematic - text = re.sub(r"e\b", "", text)
text = re.sub(r"ons\b", "", text)
text = re.sub(r"ez\b", "", text)
text = re.sub(r"eiz\b", "", text)
text = re.sub(r"ent\b", "", text)


#NOUNS : regular grammatical forms

# e.g. "mur" (Brunot & Bruneau, 1949 :192)
text = re.sub(r"\Bs\b", "", text) #here is the issue with s
# e.g. "none" (Einhorn, 1975: 15)
text = re.sub(r"ain\b", "", text)
text = re.sub(r"ains\b", "", text)
# e.g. "baron" (Einhorn, 1975: 15)
text = re.sub(r"aron\b", r"er", text)
text = re.sub(r"arons\b", r"er", text)


class Stemmer(object):

    def __init__(self, stops=STOPS_LIST):
        """Initializer for stemmer, imports stops"""
        self.stops = stops

        return

    def stem(self, text):
        """Stem each word of the French text."""

        # reduced forms

        text = re.sub(r"n'", "ne ", text)
        text = re.sub(r"s'", "si ", text)
        text = re.sub(r"t'", "te ", text)
        text = re.sub(r"qu'", "que ", text)
        # l' can stand for la or lui or le
        text = re.sub(r"l'", "lui ", text)
        text = re.sub(r"m'", "me ", text)

        stemmed_text = ''

        for word in text.split(' '): #french tokenizer pls
            if word not in self.stops:
                # remove the simple endings from the target word
                word, was_stemmed = self._matchremove_simple_endings(word)
            # if word didn't match the simple endings, try verb endings
                if not was_stemmed:
                        word = self._matchremove_verb_endings(word)
        # add the stemmed word to the text
        stemmed_text += word + ' '
        return stemmed_text

    def _matchremove_simple_endings(self, word):
        """Remove the noun, adjective, adverb word endings"""

        was_stemmed = False

        # noun, adjective, and adverb word endings sorted by charlen, then alph
        simple_endings = ['s',
                          'ain',
                          'ains',
                          'aron',
                          'arons']

        for ending in simple_endings:
            if word.endswith(ending):
                word = re.sub(r'{0}$'.format(ending), '', word)
                was_stemmed = True
                break

        return word, was_stemmed

    def _matchremove_verb_endings(self, word):
        """Remove the verb endings"""

      #  i_verb_endings = ['iuntur',
       #                     'erunt',
       #                     'untur',
       #                     'iunt',
       #                     'unt']

     #   bi_verb_endings = ['beris',
     #                       'bor',
     #                       'bo']

     #   eri_verb_endings = ['ero']

        verb_endings = ['es',
                        'et',
                        'ons',
                        'ez',
                        'ent',
                        's',
                        't',
                        'e',
                        'ant',
                        'eie',
                        'eies',
                        'eit',
                        'iiens',
                        'iiez',
                        'eient',
                        'is',
                        'ist',
                        'issons',
                        'issez',
                        'issent',
                        'issant',
                        'isseie',
                        'isseit',
                        'issiiens',
                        'issiiez',
                        'isseient'
                        ]

        # replace i verb endings with i
    #    for ending in i_verb_endings:
     #       if word.endswith(ending):
      #          word = re.sub(r'{0}$'.format(ending), 'i', word)
       #         return word

        # replace bi verb endings with bi
#        for ending in bi_verb_endings:
 #           if word.endswith(ending):
  #              word = re.sub(r'{0}$'.format(ending), 'bi', word)
   #             return word

        # replace eri verb endings with eri
    #    for ending in eri_verb_endings:
     #       if word.endswith(ending):
      #          word = re.sub(r'{0}$'.format(ending), 'eri', word)
       #         return word

        # otherwise, remove general verb endings
        for ending in verb_endings:
            if word.endswith(ending):
                word = re.sub(r'{0}$'.format(ending), '', word)
                break

        return word


print(text)