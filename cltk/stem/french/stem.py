import re
from cltk.tokenize.word import WordTokenizer
from cltk.stem.french.exceptions import exceptions

__author__ = ['Natasha Voake <natashavoake@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

def stem(text):
    """make string lower-case"""
    text = text.lower()
    """Stem each word of the French text."""

    stemmed_text = ''

    word_tokenizer = WordTokenizer('french')
    tokenized_text = word_tokenizer.tokenize(text)
    for word in tokenized_text:
        """remove the simple endings from the target word"""
        word, was_stemmed = matchremove_noun_endings(word)
        """if word didn't match the simple endings, try verb endings"""
        if not was_stemmed:
            word = matchremove_verb_endings(word)
        """add the stemmed word to the text"""
        stemmed_text += word + ' '
    return stemmed_text

def matchremove_noun_endings(word):
    """Remove the noun and adverb word endings"""

    was_stemmed = False

    """common and proper noun and adjective word endings sorted by charlen, then alph"""
    noun_endings = ['arons', 'ains', 'aron', 'ment', 'ain', 'age', 'on', 'es', 'ée', 'ee', 'ie', 's']

    for ending in noun_endings:
        """ignore exceptions"""
        if word in exceptions:
            word = word
            was_stemmed = True
            break
        if word == ending:
            word = word
            was_stemmed = True
            break
        """removes noun endings"""
        if word.endswith(ending):
            word = re.sub(r'{0}$'.format(ending), '', word)
            was_stemmed = True
            break

    return word, was_stemmed

def matchremove_verb_endings(word):
    """Remove the verb endings"""
    """verb endings sorted by charlen then alph"""
    verb_endings =['issiiens', 'isseient', 'issiiez', 'issons', 'issent', 'issant', 'isseie', 'isseit', 'issons',
                   'isseiz', 'assent', 'issons', 'isseiz', 'issent', 'iiens', 'eient', 'issez', 'oient', 'istes',
                   'ïstes', 'istes', 'astes', 'erent', 'istes', 'irent', 'ustes', 'urent', 'âmes', 'âtes', 'èrent',
                   'asses', 'isses', 'issez', 'ssons', 'sseiz', 'ssent', 'erent', 'eies', 'iiez', 'oies', 'iens',
                   'ions', 'oint', 'eret', 'imes', 'rent', 'ümes', 'ütes', 'ïmes', 'imes', 'asse', 'isse', 'usse',
                   'ames', 'imes', 'umes', 'asse', 'isse', 'sses', 'ssez', 'ons', 'ent', 'ant', 'eie', 'eit', 'int',
                   'ist', 'eiz', 'oie', 'oit', 'iez', 'ois', 'oit', 'iez', 'res', 'ert', 'ast', 'ist', 'sse', 'mes', 'er',
                   'es', 'et', 'ez', 'is', 're', 'oi', 'ïs', 'üs', 'ai', 'as', 'at', 'is', 'it', 'ui',
                   'us', 'ut', 'st', 's', 't', 'e', 'é', 'z', 'u', 'a', 'i']

    for ending in verb_endings:
        if word == ending:
            word = word
            break
        if word.endswith(ending):
            word = re.sub(r'{0}$'.format(ending), '', word)
            break

    return word
