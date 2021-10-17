"""``Process`` classes for accessing the Stanza project."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import stanza
from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, MorphosyntacticFeature, Process, Word
from cltk.dependency.stanza import StanzaWrapper
from cltk.dependency.tree import DependencyTree
from cltk.morphology.morphosyntax import (
    MorphosyntacticFeatureBundle,
    from_ud,
    to_categorial,
)


@dataclass
class StanzaProcess(Process):
    """A ``Process`` type to capture everything
    that the ``stanza`` project can do for a
    given language.

    .. note::
        ``stanza`` has only partial functionality available for some languages.

    >>> from cltk.languages.example_texts import get_example_text
    >>> process_stanza = StanzaProcess(language="lat")
    >>> isinstance(process_stanza, StanzaProcess)
    True
    >>> from stanza.models.common.doc import Document
    >>> output_doc = process_stanza.run(Doc(raw=get_example_text("lat")))
    >>> isinstance(output_doc.stanza_doc, Document)
    True
    """

    language: str = None

    @cachedproperty
    def algorithm(self):
        return StanzaWrapper.get_nlp(language=self.language)

    def run(self, input_doc: Doc) -> Doc:
        output_doc = deepcopy(input_doc)
        stanza_wrapper = self.algorithm
        if output_doc.normalized_text:
            input_text = output_doc.normalized_text
        else:
            input_text = output_doc.raw
        stanza_doc = stanza_wrapper.parse(input_text)
        cltk_words = self.stanza_to_cltk_word_type(stanza_doc)
        output_doc.words = cltk_words
        output_doc.stanza_doc = stanza_doc

        return output_doc

    @staticmethod
    def stanza_to_cltk_word_type(stanza_doc):
        """Take an entire ``stanza`` document, extract
        each word, and encode it in the way expected by
        the CLTK's ``Word`` type.

        >>> from cltk.dependency.processes import StanzaProcess
        >>> from cltk.languages.example_texts import get_example_text
        >>> process_stanza = StanzaProcess(language="lat")
        >>> cltk_words = process_stanza.run(Doc(raw=get_example_text("lat"))).words
        >>> isinstance(cltk_words, list)
        True
        >>> isinstance(cltk_words[0], Word)
        True
        >>> cltk_words[0]
        Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='Gallia', pos=noun, lemma='Gallia', stem=None, scansion=None, xpos='A1|grn1|casA|gen2', upos='NOUN', dependency_relation='nsubj', governor=1, features={Case: [nominative], Gender: [feminine], Number: [singular]}, category={F: [neg], N: [pos], V: [neg]}, stop=None, named_entity=None, syllables=None, phonetic_transcription=None, definition=None)

        """

        words_list = list()  # type: List[Word]

        for sentence_index, sentence in enumerate(stanza_doc.sentences):
            sent_words = dict()  # type: Dict[int, Word]
            indices = list()  # type: List[Tuple[int, int]]

            for token_index, token in enumerate(sentence.tokens):
                stanza_word = token.words[0]  # type: stanza.pipeline.doc.Word
                # TODO: Figure out how to handle the token indexes, esp 0 (root) and None (?)
                pos: Optional[MorphosyntacticFeature] = from_ud("POS", stanza_word.pos)
                cltk_word = Word(
                    index_token=int(stanza_word.id)
                    - 1,  # subtract 1 from id b/c Stanza starts their index at 1
                    index_sentence=sentence_index,
                    string=stanza_word.text,  # same as ``token.text``
                    pos=pos,
                    xpos=stanza_word.xpos,
                    upos=stanza_word.upos,
                    lemma=stanza_word.lemma,
                    dependency_relation=stanza_word.deprel,
                    governor=stanza_word.head - 1
                    if stanza_word.head
                    else -1,  # note: if val becomes ``-1`` then no governor, ie word is root
                )  # type: Word

                # convert UD features to the normalized CLTK features
                raw_features = (
                    [tuple(f.split("=")) for f in stanza_word.feats.split("|")]
                    if stanza_word.feats
                    else []
                )
                cltk_features = [
                    from_ud(feature_name, feature_value)
                    for feature_name, feature_value in raw_features
                ]
                cltk_word.features = MorphosyntacticFeatureBundle(*cltk_features)
                cltk_word.category = to_categorial(cltk_word.pos)
                cltk_word.stanza_features = stanza_word.feats

                # sent_words[cltk_word.index_token] = cltk_word
                words_list.append(cltk_word)

                # # TODO: Fix this, I forget what we were tracking in this
                # indices.append(
                #     (
                #         int(stanza_word.governor)
                #         - 1,  # -1 to match CLTK Word.index_token
                #         int(stanza_word.parent_token.index)
                #         - 1,  # -1 to match CLTK Word.index_token
                #     )
                # )
            # # TODO: Confirm that cltk_word.parent is ever getting filled out. Only for some lang models?
            # for idx, cltk_word in enumerate(sent_words.values()):
            #     governor_index, parent_index = indices[idx]  # type: int, int
            #     cltk_word.governor = governor_index if governor_index >= 0 else None
            #     if cltk_word.index_token != sent_words[parent_index].index_token:
            #         cltk_word.parent = parent_index

        return words_list


@dataclass
class GreekStanzaProcess(StanzaProcess):
    """Stanza processor for Ancient Greek."""

    language: str = "grc"
    description: str = "Default process for Stanza for the Ancient Greek language."


@dataclass
class LatinStanzaProcess(StanzaProcess):
    """Stanza processor for Latin."""

    language: str = "lat"
    description: str = "Default process for Stanza for the Latin language."


@dataclass
class OCSStanzaProcess(StanzaProcess):
    """Stanza processor for Old Church Slavonic."""

    language: str = "chu"
    description: str = (
        "Default process for Stanza for the Old Church Slavonic language."
    )


@dataclass
class OldFrenchStanzaProcess(StanzaProcess):
    """Stanza processor for Old French."""

    language: str = "fro"
    description: str = "Default process for Stanza for the Old French language."


@dataclass
class GothicStanzaProcess(StanzaProcess):
    """Stanza processor for Gothic."""

    language: str = "got"
    description: str = "Default process for Stanza for the Gothic language."


@dataclass
class CopticStanzaProcess(StanzaProcess):
    """Stanza processor for Coptic."""

    language: str = "cop"
    description: str = "Default process for Stanza for the Coptic language."


@dataclass
class ChineseStanzaProcess(StanzaProcess):
    """Stanza processor for Classical Chinese."""

    language: str = "lzh"
    description: str = "Default process for Stanza for the Classical Chinese language."


class TreeBuilderProcess(Process):
    """A ``Process`` that takes a doc containing sentences of CLTK words
    and returns a dependency tree for each sentence.

    TODO: JS help to make this work, illustrate better.

    >>> from cltk import NLP
    >>> nlp = NLP(language="got", suppress_banner=True)
    >>> from cltk.dependency.processes import TreeBuilderProcess

    >>> nlp.pipeline.add_process(TreeBuilderProcess)  # doctest: +SKIP
    >>> from cltk.languages.example_texts import get_example_text  # doctest: +SKIP
    >>> doc = nlp.analyze(text=get_example_text("got"))  # doctest: +SKIP
    >>> len(doc.trees)  # doctest: +SKIP
    4
    """

    def algorithm(self, doc):
        doc.trees = [DependencyTree.to_tree(sentence) for sentence in doc.sentences]
        return doc
