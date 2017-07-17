#encoding : utf-8
import re
from cltk.tokenize.word import WordTokenizer
from cltk.stem.french.exceptions import exceptions

text = "sains jorge ne vost plus atendre " \
       "ains comença son cors estendre" \
       "ses mains joinst sur sa peitréine " \
       "vers les sergens son chief encline " \
       "que tantost le chief li trencherent " \
       "conques de rien ne l’sparaignerent " \
       "li angle deu l’arme saisirent " \
       "a grant joie quant il la virent " \
       "lié furent docement chanterent " \
       "véant tos au ciel la porterent " \
       "grant joie en est et fu jadis " \
       "de saint jorge en paradis"

def stem(text):
#normalise apostrophes
    text = re.sub(r"’", "'", text)
# make string lower-case
    text = text.lower()
    """Stem each word of the French text."""

    stemmed_text = ''

    word_tokenizer = WordTokenizer('french')
    tokenized_text = word_tokenizer.tokenize(text)
    #tokenize text rather than split on ' '
    for word in tokenized_text:
            # remove the simple endings from the target word
        word, was_stemmed = matchremove_simple_endings(word)
        # if word didn't match the s
            # imple endings, try verb endings
        if not was_stemmed:
            word = matchremove_verb_endings(word)
        # add the stemmed word to the text
        stemmed_text += word + ' '
    return stemmed_text

def matchremove_simple_endings(word):
    """Remove the noun, adverb word endings"""

    was_stemmed = False

    # common and proper noun and adjective word endings sorted by charlen, then alph
    simple_endings = ['arons', 'ains', 'aron', 'ment', 'ain', 'age', 'on', 'es', 'ie', 's']

    for ending in simple_endings:
        #ignore exceptions
        if word in exceptions:
            word = word
            was_stemmed = True
            break
        #removes simple endings
        if word.endswith(ending):
            word = re.sub(r'{0}$'.format(ending), '', word)
            was_stemmed = True
            break

    return word, was_stemmed

def matchremove_verb_endings(word):
    """Remove the verb endings"""
    #sorted by len then alphabetic order
    verb_endings = ['issiiens', 'isseient', 'issiiez', 'issons', 'issent', 'issant', 'isseie', 'isseit', 'issons',
                    'isseiz', 'assent', 'issons', 'isseiz', 'issent', 'iiens', 'eient', 'issez', 'er,es', 'oient',
                    'istes', 'ïstes', 'istes', 'astes', 'erent', 'istes', 'irent', 'ustes', 'urent', 'âmes', 'âtes',
                    'èrent', 'asses', 'isses', 'issez', 'ssons', 'sseiz', 'ssent', 'erent', 'eies', 'iiez', 'oies',
                    'iens', 'ions', 'oint', 'eret', 'imes', 'rent', 'ümes', 'ütes', 'ïmes', 'imes', 'asse', 'isse',
                    'usse', 'ames', 'imes', 'umes', 'asse', 'isse', 'sses', 'ssez', 'ons', 'ent', 'ant', 'eie', 'eit',
                    'ist', 'eiz', 'oie', 'oit', 'iez', 'ois', 'oit', 'iez', 'res', 'ert', 'ast', 'ist', 'sse', 'mes',
                    'et', 'er', 'ez', 'is', 're', 'oi', 'ïs', 'üs', 'ai', 'ai', 'as', 'at', 'is', 'it', 'ui', 'us', 'ut',
                    'st', 's', 't', 'e', 'é', 'z', 'i', 'u', 'a', 'i', 'i', 'u']

    # otherwise, remove verb endings
    for ending in verb_endings:
        if word.endswith(ending):
            word = re.sub(r'{0}$'.format(ending), '', word)
            break

    return word

print(stem(text))


