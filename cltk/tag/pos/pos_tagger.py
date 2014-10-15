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
            pickle_path = os.path.abspath('cltk/tag/pos/greek/greek.pickle')
        elif language == 'latin':
            pickle_path = os.path.abspath('cltk/tag/pos/latin/latin.pickle')
        else:
            print('No unigram tagger for this language available.')
        with open(pickle_path, 'rb') as open_pickle:
            tagger = pickle.load(open_pickle)
        untagged_tokens = wordpunct_tokenize(untagged_string)
        tagged_text = tagger.tag(untagged_tokens)
        return tagged_text
