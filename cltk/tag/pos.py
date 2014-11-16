"""Tags part of speech (POS)."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from nltk.tokenize import wordpunct_tokenize
import os
import pickle


def tag_unigram(untagged_string, language):
    """Reads language .pickle for right language"""
    if language == 'greek':
        path_rel = '~/cltk_data/greek/trained_model/cltk_linguistic_data/taggers/pos/unigram.pickle'  # pylint: disable=C0301
    elif language == 'latin':
        path_rel = '~/cltk_data/latin/trained_model/cltk_linguistic_data/taggers/pos/unigram.pickle'  # pylint: disable=C0301
    else:
        print('No unigram tagger for this language available.')
    pickle_path = os.path.expanduser(path_rel)
    with open(pickle_path, 'rb') as open_pickle:
        tagger = pickle.load(open_pickle)
    untagged_tokens = wordpunct_tokenize(untagged_string)
    tagged_text = tagger.tag(untagged_tokens)
    return tagged_text


def tag_bigram(untagged_string, language):
    """Reads language .pickle for right language"""
    if language == 'greek':
        path_rel = '~/cltk_data/greek/trained_model/cltk_linguistic_data/taggers/pos/bigram.pickle'  # pylint: disable=C0301
    elif language == 'latin':
        path_rel = '~/cltk_data/latin/trained_model/cltk_linguistic_data/taggers/pos/bigram.pickle'  # pylint: disable=C0301
    else:
        print('No bigram tagger for this language available.')
    pickle_path = os.path.expanduser(path_rel)
    with open(pickle_path, 'rb') as open_pickle:
        tagger = pickle.load(open_pickle)
    untagged_tokens = wordpunct_tokenize(untagged_string)
    tagged_text = tagger.tag(untagged_tokens)
    return tagged_text


def tag_ngram_123_backoff(untagged_string, language):
    """Reads language .pickle for right language"""
    if language == 'greek':
        path_rel = '~/cltk_data/greek/trained_model/cltk_linguistic_data/taggers/pos/123grambackoff.pickle'  # pylint: disable=C0301
    elif language == 'latin':
        path_rel = '~/cltk_data/latin/trained_model/cltk_linguistic_data/taggers/pos/123grambackoff.pickle'  # pylint: disable=C0301
    else:
        print('No n–gram backoff tagger for this language available.')
    pickle_path = os.path.expanduser(path_rel)
    with open(pickle_path, 'rb') as open_pickle:
        tagger = pickle.load(open_pickle)
    untagged_tokens = wordpunct_tokenize(untagged_string)
    tagged_text = tagger.tag(untagged_tokens)
    return tagged_text


def tag_trigram(untagged_string, language):
    """Reads language .pickle for right language"""
    if language == 'greek':
        path_rel = '~/cltk_data/greek/trained_model/cltk_linguistic_data/taggers/pos/trigram.pickle'  # pylint: disable=C0301
    elif language == 'latin':
        path_rel = '~/cltk_data/latin/trained_model/cltk_linguistic_data/taggers/pos/trigram.pickle'  # pylint: disable=C0301
    else:
        print('No trigram tagger for this language available.')
    pickle_path = os.path.expanduser(path_rel)
    with open(pickle_path, 'rb') as open_pickle:
        tagger = pickle.load(open_pickle)
    untagged_tokens = wordpunct_tokenize(untagged_string)
    tagged_text = tagger.tag(untagged_tokens)
    return tagged_text


def tag_tnt(untagged_string, language):
    """Reads language .pickle for right language"""
    if language == 'greek':
        path_rel = '~/cltk_data/greek/trained_model/cltk_linguistic_data/taggers/pos/tnt.pickle'  # pylint: disable=C0301
    elif language == 'latin':
        path_rel = '~/cltk_data/latin/trained_model/cltk_linguistic_data/taggers/pos/tnt.pickle'  # pylint: disable=C0301
    else:
        print('No n–gram backoff tagger for this language available.')
    pickle_path = os.path.expanduser(path_rel)
    with open(pickle_path, 'rb') as open_pickle:
        tagger = pickle.load(open_pickle)
    untagged_tokens = wordpunct_tokenize(untagged_string)
    tagged_text = tagger.tag(untagged_tokens)
    return tagged_text
