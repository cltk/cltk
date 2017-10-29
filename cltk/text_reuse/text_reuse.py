"""
Offer text reuse tools optimized for classical languages
"""

import re, string
import unicodedata
from cltk.tokenize.sentence import TokenizeSentence
from cltk.utils.cltk_logger import logger
from cltk.text_reuse.levenshtein import Levenshtein
from cltk.text_reuse.comparison import Comparison
from cltk.stem.latin.stem import Stemmer


__author__ = ['Luke Hollis <lukehollis@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


class TextReuse:
    """
    A class for doing string similarity comparisons.

    This class currently only relies on the Levenshtein distance calucation for
    string comparison.  When we have the need to support multiple types of string
    comparison, update the class to do so.

    """


    def __init__(self, text_ref_a=None, text_ref_b=None, stem_words=False, sanitize_input=False):
        """
        Indicate if text reuse class should stem words and/or sanitize_input before comparison
        :param text_a: dict
        :param text_b: dict
        :param stem_words: bool
        :param sanitize_input: bool
        """

        self.text_ref_a = text_ref_a
        self.text_ref_b = text_ref_b
        self.stem_words = stem_words
        self.sanitize_input = sanitize_input

        return

    def compare_sentences(self, str_a, str_b, language):
        """Tokenize two input strings on sentence boundary and return a
        matrix of Levenshtein distance ratios.
        :param language: str (language name)
        :param string_a: str
        :param string_b: str
        :return: list [[Comparison]]
        """

        sents_a = []
        sents_b = []
        ratios = []

        # Make the latin tokenizer
        if language == "latin":
            sent_tokenizer = TokenizeSentence('latin')

        # Make the greek tokenizer
        elif language == "greek":
            sent_tokenizer = TokenizeSentence('greek')

        # Otherwise, if language, is unsupported, throw error stating accepted Language
        # values that may be used to tokenize sentences
        else:
            print("Language for sentence tokenization not recognized. "
                  "Accepted values are 'latin' and 'greek'.")
            return

        # If class instance is set to stem words, do so
        if self.stem_words:
            stemmer = Stemmer()
            str_a = stemmer.stem(str_a)
            str_b = stemmer.stem(str_b)

        # Tokenize input strings
        sents_a = sent_tokenizer.tokenize_sentences(str_a)
        sents_b = sent_tokenizer.tokenize_sentences(str_b)

        # Process sentences for comparison (taking into account sanitization settings)
        sents_a = self._process_sentences(sents_a)
        sents_b = self._process_sentences(sents_b)

        # Build matrix of edit distance ratios
        comparisons = self._calculate_ratios(sents_a, sents_b)

        return comparisons

    def compare_sliding_window(self, str_a, str_b, window_length=50, curse_forward=20):
        """
        Compare two strings with a sliding window method based on window_length and curse_forward values
        :param string_a: str
        :param string_b: str
        :param window_length: int
        :param curse_forward: int
        :return: list [[Comparison]]
        """

        if self.stem_words:
            stemmer = Stemmer()
            str_a = stemmer.stem(str_a)
            str_b = stemmer.stem(str_b)

        substrs_a = self._str_to_windows(str_a, window_length, curse_forward)
        substrs_b = self._str_to_windows(str_b, window_length, curse_forward)

        # Build
        comparisons = self._calculate_ratios(substrs_a, substrs_b)

        return comparisons

    def _calculate_ratios(self, list_a, list_b):
        """
        Calulate a matrix of string comparisons given two input lists
        :param list_a: list [object]
        :param list_b: list [object]
        :return: list [[Comparison]]
        """

        comparisons = []
        l = Levenshtein()

        # For all strings in list a
        for i, str_a in enumerate(list_a):

            # Add a new list to our list of lists of comparisons
            comparisons.append([])

            # Compare str_a to every string in list_b
            for str_b in list_b:

                # If the sanitize, input flag is set, make the ratio with the sanitized values
                if self.sanitize_input:
                    new_comparison = Comparison(
                                            str_a['text'],
                                            str_b['text'],
                                            l.ratio(str_a['sanitized'], str_b['sanitized'])
                                        )

                # Otherwise, make the ratio with the original, unsanitize text strings
                else:
                    new_comparison = Comparison(
                                            str_a['text'],
                                            str_b['text'],
                                            l.ratio(str_a['text'], str_b['text'])
                                        )

                # If text metadata is set on this class for text a or b, save that data with the
                # comparison
                if self.text_ref_a:
                    new_comparison.set_ref_a(self.text_ref_a)
                if self.text_ref_b:
                    new_comparison.set_ref_b(self.text_ref_b)

                # Finally, append the new comparison to the list of comparisons
                comparisons[i].append(new_comparison)

        return comparisons

    def _process_sentences(self, sents_list):
        """
        Divide an input string to a list of substrings based on window_length and curse_forward values
        :param sents_list: list [str]
        :return: list [object]
        """
        processed_sents = []

        for sent in sents_list:
            processed_sent = {
                                'text' : sent
                            }
            # If the class is set to santize input before comparison, do so
            if self.sanitize_input:
                processed_sent['sanitized'] = self._sanitize(sent),

            processed_sents.append(processed_sent)

        return processed_sents

    def _str_to_windows(self, input_str, window_length, curse_forward):
        """
        Divide an input string to a list of substrings based on window_length and curse_forward values
        :param input_str: str
        :param window_length: int
        :param curse_forward: int
        :return: list [str]
        """
        windows = []

        i = 0
        len_input = len(input_str)
        while i < len_input:
            window_text = input_str[i:i+window_length]

            if self.sanitize_input:
                windows.append({
                                    'sanitized' : self._sanitize(window_text),
                                    'text' : window_text
                                })
            else:
                windows.append({
                                    'text' : window_text
                                })

            i = i + curse_forward


        return windows

    def _sanitize(self, unsanitized):
        """
        Sanitize input string to optimize string comparison match
        :param unsanitized: str
        :return: str
        """

        sanitized = ""

        # strip punctuation and diacritics
        replace_punct = str.maketrans( string.punctuation + "᾽᾿῾", ' '*(len(string.punctuation) + 3)  )
        sanitized = unsanitized.translate( replace_punct )
        sanitized = "".join(c for c in unicodedata.normalize("NFD", sanitized) if unicodedata.category(c) != "Mn")

        #finally, lose all whitespace
        sanitized = re.sub(r'\s+','', sanitized)

        return sanitized
