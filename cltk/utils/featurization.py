"""`featurization.py` - a collection of methods for featurizing."""

import logging
from typing import List

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


def word_to_features(word: str, max_word_length: int = 20) -> List[int]:
    """

    :param word: a single word
    :param max_word_length: the maximum word length for the feature array
    :return: A list of ordinal integers mapped to each character and padded to the max word length.

    >>> word_to_features('far', 20)
    [114, 97, 102, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32]
    """
    if len(word) > max_word_length:
        LOG.warning('Excessive word length {} for {}, truncating to {}'.format(len(word), word,
                                                                               max_word_length))
        word = word[:max_word_length]
    wordlist = list(word)
    wordlist.reverse()
    return [ord(c) for c in "".join(wordlist).ljust(max_word_length, ' ')]
