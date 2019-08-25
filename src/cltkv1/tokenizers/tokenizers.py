"""Module for tokenizers."""

import re
from typing import List

from cltkv1.utils.cltk_dataclasses import Word


def _dummy_get_token(indices_tokens: List[List[int]], text: str) -> List[Word]:
    """Take indices and populate Word object.

    >>> from cltkv1 import NLP
    >>> cltk_nlp = NLP(language='greek')
    >>> john_damascus_corinth = "Τοῦτο εἰπὼν, ᾐνίξατο αἰτίους ὄντας τοῦ τὰ ἐλάσσονα λαμβάνειν, καὶ κυρίους, εἰ βούλοιντο, τοῦ τὰ μείζονα. Ἔστι δὲ πολὺ μείζων ἡ ἀγάπη πάντων τῶν χαρισμάτων."
    >>> indices_words = _dummy_get_token_indices(text=john_damascus_corinth)
    >>> tokens = _dummy_get_token(indices_words, john_damascus_corinth)
    >>> tokens[0]
    Word(index_char_start=0, index_char_stop=5, index_token=0, index_sentence=None, string='Τοῦτο', pos=None, scansion=None)
    """
    tokens = list()
    for count, indices in enumerate(indices_tokens):
        start, end = indices[0], indices[1]
        token_str = text[start:end]
        word = Word(
            index_char_start=start,
            index_char_stop=end,
            index_token=count,
            string=token_str,
        )
        tokens.append(word)
    return tokens


def _dummy_get_token_indices(text: str) -> List[List[int]]:
    """Get the start/stop char indices of word boundaries.

    >>> from cltkv1 import NLP
    >>> cltk_nlp = NLP(language='greek')
    >>> john_damascus_corinth = "Τοῦτο εἰπὼν, ᾐνίξατο αἰτίους ὄντας τοῦ τὰ ἐλάσσονα λαμβάνειν, καὶ κυρίους, εἰ βούλοιντο, τοῦ τὰ μείζονα. Ἔστι δὲ πολὺ μείζων ἡ ἀγάπη πάντων τῶν χαρισμάτων."
    >>> indices_words = _dummy_get_token_indices(text=john_damascus_corinth)
    >>> indices_words[0:3]
    [[0, 5], [6, 11], [13, 20]]
    """
    indices_words = list()
    pattern_word = re.compile(r"\w+")
    for word_match in pattern_word.finditer(string=text):
        idx_word_start, idx_word_stop = word_match.span()
        indices_words.append([idx_word_start, idx_word_stop])
    return indices_words


def _dummy_get_sentence_indices(text: str) -> List[List[int]]:
    """Get the stops/start char indices of where sentences begin and end.

    >>> from cltkv1 import NLP
    >>> cltk_nlp = NLP(language='greek')
    >>> john_damascus_corinth = "Τοῦτο εἰπὼν, ᾐνίξατο αἰτίους ὄντας τοῦ τὰ ἐλάσσονα λαμβάνειν, καὶ κυρίους, εἰ βούλοιντο, τοῦ τὰ μείζονα. Ἔστι δὲ πολὺ μείζων ἡ ἀγάπη πάντων τῶν χαρισμάτων."
    >>> indices_sentences = _dummy_get_sentence_indices(text=john_damascus_corinth)
    >>> indices_sentences
    [[103, 104], [154, 155]]
    """
    indices_sentences = list()
    pattern_sentence = re.compile(r"\.")
    for sentence_match in pattern_sentence.finditer(string=text):
        idx_sentence_start, idx_sentence_stop = sentence_match.span()
        indices_sentences.append([idx_sentence_start, idx_sentence_stop])
    return indices_sentences
