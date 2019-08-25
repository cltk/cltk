"""Sentence splitting."""

import re
from typing import List


class Splitter:
    """High-level class for sentence splitting, to be inherited by language-specific splitters."""

    def __init__(self):
        """Constructor for ``DefaultSplitter()``.

        >>> splitter = Splitter()
        >>> type(splitter)
        <class 'cltkv1.tokenizers.sentence.Splitter'>
        """
        pass

    @staticmethod
    def dummy_get_indices(text: str) -> List[List[int]]:
        """Returns the indices of detected sentences.

        >>> splitter = Splitter()
        >>> john_damascus_corinth = "Τοῦτο εἰπὼν, ᾐνίξατο αἰτίους ὄντας τοῦ τὰ ἐλάσσονα λαμβάνειν, καὶ κυρίους, εἰ βούλοιντο, τοῦ τὰ μείζονα. Ἔστι δὲ πολὺ μείζων ἡ ἀγάπη πάντων τῶν χαρισμάτων."
        >>> indices_sentences = splitter.dummy_get_indices(text=john_damascus_corinth)
        >>> indices_sentences
        [[103, 104], [154, 155]]
        """
        indices_sentences = list()
        pattern_sentence = re.compile(r"\.")
        for sentence_match in pattern_sentence.finditer(string=text):
            idx_sentence_start, idx_sentence_stop = sentence_match.span()
            indices_sentences.append([idx_sentence_start, idx_sentence_stop])
        return indices_sentences


class DefaultSplitter(Splitter):
    """Sentence splitter for languages for which there is not a specific splitter.

    >>> splitter = Splitter()
    >>> john_damascus_corinth = "Τοῦτο εἰπὼν, ᾐνίξατο αἰτίους ὄντας τοῦ τὰ ἐλάσσονα λαμβάνειν, καὶ κυρίους, εἰ βούλοιντο, τοῦ τὰ μείζονα. Ἔστι δὲ πολὺ μείζων ἡ ἀγάπη πάντων τῶν χαρισμάτων."
    >>> indices_sentences = splitter.dummy_get_indices(text=john_damascus_corinth)
    >>> indices_sentences
    [[103, 104], [154, 155]]
    """

    def __init__(self):
        """Constructor for ``DefaultSplitter()``.

        >>> def_splitter = Splitter()
        >>> type(def_splitter)
        <class 'cltkv1.tokenizers.sentence.Splitter'>
        """
        super().__init__()


class LatinSplitter(Splitter):
    """Sentence splitter(s) for the Latin language."""

    def __init__(self):
        """Constructor for the ``LatinSplitter()`` class."""
        super().__init__()


if __name__ == "__main__":
    pass
