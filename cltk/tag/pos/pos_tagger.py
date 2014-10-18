"""Tags part of speech (POS)."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from nltk.tokenize import wordpunct_tokenize
import os
import pickle


class POSTag(object):
    """Picks up taggers made with UnigramTagger"""

    def __init__(self):
        """Initializer. Should it do anything?"""
        pass

    def unigram_tagger(self, untagged_string, language):
        """Reads language .pickle for right language"""
        if language == 'greek':
            pickle_path = os.path.expanduser('~/cltk_data/greek/cltk_linguistic_data/taggers/pos/unigram.pickle')
        elif language == 'latin':
            pickle_path = os.path.expanduser('~/cltk_data/latin/cltk_linguistic_data/taggers/pos/unigram.pickle')
        else:
            print('No unigram tagger for this language available.')
        with open(pickle_path, 'rb') as open_pickle:
            tagger = pickle.load(open_pickle)
        untagged_tokens = wordpunct_tokenize(untagged_string)
        tagged_text = tagger.tag(untagged_tokens)
        return tagged_text


    def bigram_tagger(self, untagged_string, language):
        """Reads language .pickle for right language"""
        if language == 'greek':
            pickle_path = os.path.expanduser('~/cltk_data/greek/cltk_linguistic_data/taggers/pos/bigram.pickle')
        elif language == 'latin':
            pickle_path = os.path.expanduser('~/cltk_data/latin/cltk_linguistic_data/taggers/pos/bigram.pickle')
        else:
            print('No bigram tagger for this language available.')
        with open(pickle_path, 'rb') as open_pickle:
            tagger = pickle.load(open_pickle)
        untagged_tokens = wordpunct_tokenize(untagged_string)
        tagged_text = tagger.tag(untagged_tokens)
        return tagged_text


    def trigram_tagger(self, untagged_string, language):
        """Reads language .pickle for right language"""
        if language == 'greek':
            pickle_path = os.path.expanduser('~/cltk_data/greek/cltk_linguistic_data/taggers/pos/trigram.pickle')
        elif language == 'latin':
            pickle_path = os.path.expanduser('~/cltk_data/latin/cltk_linguistic_data/taggers/pos/trigram.pickle')
        else:
            print('No trigram tagger for this language available.')
        with open(pickle_path, 'rb') as open_pickle:
            tagger = pickle.load(open_pickle)
        untagged_tokens = wordpunct_tokenize(untagged_string)
        tagged_text = tagger.tag(untagged_tokens)
        return tagged_text
