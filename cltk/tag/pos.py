"""Tag part of speech (POS) using CLTK taggers."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'


from cltk.utils.file_operations import open_pickle
from nltk.tokenize import wordpunct_tokenize
import os


TAGGERS = {'greek':
               {'unigram': 'unigram.pickle',
                'bigram': 'bigram.pickle',
                'trigram': 'trigram.pickle',
                'ngram_123_backoff': '123grambackoff.pickle',
                'tnt': 'tnt.pickle',
               },
           'latin':
               {'unigram': 'unigram.pickle',
                'bigram': 'bigram.pickle',
                'trigram': 'trigram.pickle',
                'ngram_123_backoff': '123grambackoff.pickle',
                'tnt': 'tnt.pickle',
               }}


class POSTag():
    """Tag words' parts-of-speech."""

    def __init__(self, language: str):
        """Setup variables."""
        self.language = language
        self.available_taggers = self._setup_language_variables(self.language)

    def _setup_language_variables(self, lang: str):
        """Check for language availability and presence of tagger files.
        :param lang: The language argument given to the class.
        :type lang: str
        :rtype : dict
        """
        assert lang in TAGGERS.keys(), \
            'POS tagger not available for {0} language.'.format(lang)
        rel_path = os.path.join('~/cltk_data',
                                lang,
                                'model/' + lang + '_models_cltk/taggers/pos')  # pylint: disable=C0301
        path = os.path.expanduser(rel_path)
        tagger_paths = {}
        for tagger_key, tagger_val in TAGGERS[lang].items():
            tagger_path = os.path.join(path, tagger_val)
            assert os.path.isfile(tagger_path), \
                'CLTK linguistics models not available for {0}.'.format(tagger_val)
            tagger_paths[tagger_key] = tagger_path
        return tagger_paths

    def tag_unigram(self, untagged_string: str):
        """Tag POS with unigram tagger.
        :type untagged_string: str
        :param : An untagged, untokenized string of text.
        :rtype tagged_text: str
        """
        untagged_tokens = wordpunct_tokenize(untagged_string)
        pickle_path = self.available_taggers['unigram']
        tagger = open_pickle(pickle_path)
        tagged_text = tagger.tag(untagged_tokens)
        return tagged_text

    def tag_bigram(self, untagged_string: str):
        """Tag POS with bigram tagger.
        :type untagged_string: str
        :param : An untagged, untokenized string of text.
        :rtype tagged_text: str
        """
        untagged_tokens = wordpunct_tokenize(untagged_string)
        pickle_path = self.available_taggers['bigram']
        tagger = open_pickle(pickle_path)
        tagged_text = tagger.tag(untagged_tokens)
        return tagged_text

    def tag_trigram(self, untagged_string: str):
        """Tag POS with trigram tagger.
        :type untagged_string: str
        :param : An untagged, untokenized string of text.
        :rtype tagged_text: str
        """
        untagged_tokens = wordpunct_tokenize(untagged_string)
        pickle_path = self.available_taggers['trigram']
        tagger = open_pickle(pickle_path)
        tagged_text = tagger.tag(untagged_tokens)
        return tagged_text

    def tag_ngram_123_backoff(self, untagged_string: str):
        """Tag POS with 1-, 2-, 3-gram tagger.
        :type untagged_string: str
        :param : An untagged, untokenized string of text.
        :rtype tagged_text: str
        """
        untagged_tokens = wordpunct_tokenize(untagged_string)
        pickle_path = self.available_taggers['ngram_123_backoff']
        tagger = open_pickle(pickle_path)
        tagged_text = tagger.tag(untagged_tokens)
        return tagged_text

    def tag_tnt(self, untagged_string: str):
        """Tag POS with TnT tagger.
        :type untagged_string: str
        :param : An untagged, untokenized string of text.
        :rtype tagged_text: str
        """
        untagged_tokens = wordpunct_tokenize(untagged_string)
        pickle_path = self.available_taggers['tnt']
        tagger = open_pickle(pickle_path)
        tagged_text = tagger.tag(untagged_tokens)
        return tagged_text
