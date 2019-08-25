"""Primary module for CLTK pipeline."""

import re
from typing import List

from cltkv1.tokenizers.tokenizers import (
    _dummy_get_sentence_indices,
    _dummy_get_token,
    _dummy_get_token_indices,
)
from cltkv1.utils.cltk_dataclasses import Text
from cltkv1.utils.pipelines import GenericPipeline, LatinPipeline

# from cltkv1.wrappers import StanfordNLPWrapper


class NLP:
    """Primary class for NLP pipeline.

    >>> cltk_nlp = NLP(language='greek')
    >>> cltk_nlp.language
    'greek'
    >>> john_damascus_corinth = "Τοῦτο εἰπὼν, ᾐνίξατο αἰτίους ὄντας τοῦ τὰ ἐλάσσονα λαμβάνειν, καὶ κυρίους, εἰ βούλοιντο, τοῦ τὰ μείζονα. Ἔστι δὲ πολὺ μείζων ἡ ἀγάπη πάντων τῶν χαρισμάτων."
    >>> john_text_analyzed = cltk_nlp.analyze(john_damascus_corinth)
    >>> john_text_analyzed.language
    'greek'
    >>> john_text_analyzed.indices_sentences
    [[103, 104], [154, 155]]
    >>> john_text_analyzed.indices_tokens[0:3]
    [[0, 5], [6, 11], [13, 20]]
    """

    def __init__(self, language: str, custom_pipeline: List[str] = None) -> None:
        """Constructor for CLTK class.

        >>> cltk_nlp = NLP(language='greek')
        >>> isinstance(cltk_nlp, NLP)
        True
        """
        self.language = language
        self.custom_pipeline = custom_pipeline
        self.pipeline = self._get_pipeline(self.custom_pipeline)

    def _get_pipeline(self, custom_pipeline=None):
        """Select appropriate pipeline for given language. If custom
        processing is requested, ensure that user-selected choices
        are valid, both in themselves and in unison.
        """
        if not custom_pipeline:
            # look up default pipeline for given language
            if self.language == "latin":
                self.pipeline = LatinPipeline
            self.pipeline = GenericPipeline
        else:
            # confirm that user-defined pipeline is possible
            raise NotImplementedError("Custom pipelines not implemented yet.")

    def analyze(self, text: str) -> Text:
        """The primary method for the NLP object, to which raw text strings are passed.

        >>> cltk_nlp = NLP(language='latin')
        >>> isinstance(cltk_nlp, NLP)
        True
        >>> galileo_sidereus = "Preclarum sane atque humanitatis plenum eorum fuit institutum, qui excellentium virtute virorum res preclare gestas ab invidia tutari, eorumque immortalitate digna nomina ab oblivione atque interitu vindicare, conati sunt. Hinc ad memoriam posteritatis prodite imagines, vel marmore insculpte, vel ex ere ficte; hinc posite statue, tam pedestres, quam equestres; hinc columnarum atque pyramidum, ut inquit ille, sumptus ad sidera ducti; hinc denique urbes edificate, eorumque insignite nominibus, quos grata posteritas eternitati commendandos existimavit. Eiusmodi est enim humane mentis conditio, ut nisi assiduis rerum simulacris in eam extrinsecus irrumpentibus pulsetur, omnis ex illa recordatio facile effluat."
        >>> analyzed_text = cltk_nlp.analyze(galileo_sidereus)
        >>> analyzed_text.language
        'latin'
        >>> analyzed_text.indices_sentences
        [[221, 222], [554, 555], [714, 715]]
        >>> analyzed_text.indices_tokens[0:3]
        [[0, 9], [10, 14], [15, 20]]
        >>> analyzed_text.tokens[0]
        Word(index_char_start=0, index_char_stop=9, index_token=0, index_sentence=None, string='Preclarum', pos=None, scansion=None)
        """

        indices_sentences = _dummy_get_sentence_indices(text=text)
        indices_words = _dummy_get_token_indices(text=text)
        tokens = _dummy_get_token(indices_words, text)
        text = Text(
            indices_sentences=indices_sentences,
            indices_tokens=indices_words,
            language=self.language,
            raw=text,
            tokens=tokens,
        )
        return text
