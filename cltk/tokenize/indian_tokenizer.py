"""Tokenizer for Indian languages/scripts."""

import re
import string

__author__ = ['Anoop Kunchukuttan']
__copyright = 'GPL'

modified_punctuations = string.punctuation.replace("|","") # The replace , deletes the ' | ' from the punctuation string provided by the library

indian_punctuation_pattern = re.compile('(['+modified_punctuations+'\u0964\u0965'+']|\|+)')


def indian_punctuation_tokenize_regex(input_str):
    """A trivial tokenizer which just tokenizes on the punctuation boundaries.
    This also includes punctuation, namely the the purna virama ("|") and
    deergha virama ("॥"), for Indian language scripts.

    >>> indian_str = "प्रेमचन्द का जन्म ३१ जुलाई सन् १८८० को बनारस शहर।"
    >>> indian_punctuation_tokenize_regex(indian_str)
    ['प्रेमचन्द', 'का', 'जन्म', '३१', 'जुलाई', 'सन्', '१८८०', 'को', 'बनारस', 'शहर', '।']

    :param input_str: A string to be
    :type input_str: string
    :return List of word tokens.
    :rtype: list
    """
    tok_str = indian_punctuation_pattern.sub(r' \1 ',input_str.replace('\t',' '))
    return re.sub(r'[ ]+',u' ',tok_str).strip(' ').split(' ')


if __name__ == '__main__':
    example = indian_punctuation_tokenize_regex("हिन्दी भारत की सबसे अधिक बोली और समझी जाने वाली भाषा है।")
    print(example)
