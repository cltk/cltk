"""``Process`` classes for accessing the Stanza project."""

from copy import copy
from dataclasses import dataclass
from typing import Any, Literal, Optional

import spacy
import stanza
from boltons.cacheutils import cachedproperty

from cltk.core.data_types import Doc, MorphosyntacticFeature, Process, Word
from cltk.dependency.spacy_wrapper import SpacyWrapper
from cltk.dependency.stanza_wrapper import StanzaWrapper
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
        output_doc = copy(input_doc)
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
         Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='Gallia', pos=noun, lemma='Gallia', stem=None, scansion=None, xpos='A1|grn1|casA|gen2', upos='NOUN', dependency_relation='nsubj', governor=1, features={Case: [nominative], Gender: [feminine], InflClass: [ind_eur_a], Number: [singular]}, category={F: [neg], N: [pos], V: [neg]}, stop=None, named_entity=None, syllables=None, phonetic_transcription=None, definition=None)

        """

        words_list: list[Word] = list()

        for sentence_index, sentence in enumerate(stanza_doc.sentences):
            sent_words: dict[int, Word] = dict()
            indices: list[tuple[int, int]] = list()

            for token_index, token in enumerate(sentence.tokens):
                stanza_word: stanza.pipeline.doc.Word = token.words[0]
                # TODO: Figure out how to handle the token indexes, esp 0 (root) and None (?)
                pos: Optional[MorphosyntacticFeature] = None
                if stanza_word.pos:
                    pos = from_ud("POS", stanza_word.pos)
                cltk_word = Word(
                    index_token=int(stanza_word.id)
                    - 1,  # subtract 1 from id b/c Stanza starts their index at 1
                    index_sentence=sentence_index,
                    string=stanza_word.text,  # same as ``token.text``
                    pos=pos,
                    xpos=stanza_word.xpos,
                    upos=stanza_word.upos,
                    lemma=stanza_word.lemma if stanza_word.lemma else stanza_word.text,
                    dependency_relation=stanza_word.deprel,
                    governor=stanza_word.head - 1
                    if stanza_word.head
                    else -1,  # note: if val becomes ``-1`` then no governor, ie word is root
                )

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
    authorship_info: str = "``LatinSpacyProcess`` using Stanza model by Stanford University from https://stanfordnlp.github.io/stanza/ . Please cite: https://arxiv.org/abs/2003.07082"


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


@dataclass
class SpacyProcess(Process):
    """A ``Process`` type to capture everything, that the ``spaCy`` project can do for a given language.

    .. note::
        ``spacy`` has only partial functionality available for some languages.

    >>> from cltk.languages.example_texts import get_example_text
    >>> process_spacy = SpacyProcess(language="lat")
    >>> isinstance(process_spacy, SpacyProcess)
    True

    # >>> from spacy.models.common.doc import Document
    # >>> output_doc = process_spacy.run(Doc(raw=get_example_text("lat")))
    # >>> isinstance(output_doc.spacy_doc, Document)
    True
    """

    # language: Optional[str] = None

    @cachedproperty
    def algorithm(self):
        return SpacyWrapper.get_nlp(language=self.language)

    def run(self, input_doc: Doc) -> Doc:
        output_doc = copy(input_doc)
        spacy_wrapper = self.algorithm
        if output_doc.normalized_text:
            input_text = output_doc.normalized_text
        else:
            input_text = output_doc.raw
        spacy_doc = spacy_wrapper.parse(input_text)
        cltk_words = self.spacy_to_cltk_word_type(spacy_doc)
        output_doc.words = cltk_words
        output_doc.spacy_doc = spacy_doc

        return output_doc

    @staticmethod
    def spacy_to_cltk_word_type(spacy_doc: spacy.tokens.doc.Doc):
        """Take an entire ``spacy`` document, extract
        each word, and encode it in the way expected by
        the CLTK's ``Word`` type.

        It works only if there is some sentence boundaries has been set by the loaded model.

        See note in code about starting word token index at 1

        >>> from cltk.dependency.processes import SpacyProcess
        >>> from cltk.languages.example_texts import get_example_text
        >>> process_spacy = SpacyProcess(language="lat")
        >>> cltk_words = process_spacy.run(Doc(raw=get_example_text("lat"))).words
        >>> isinstance(cltk_words, list)
        True
        >>> isinstance(cltk_words[0], Word)
        True
        >>> cltk_words[0]
        Word(index_char_start=0, index_char_stop=6, index_token=0, index_sentence=0, string='Gallia', pos=None, lemma='Gallia', stem=None, scansion=None, xpos='proper_noun', upos='PROPN', dependency_relation='nsubj', governor=None, features={}, category={}, stop=False, named_entity=None, syllables=None, phonetic_transcription=None, definition=None)

        """
        words_list: list[Word] = []
        for sentence_index, sentence in enumerate(spacy_doc.doc.sents):
            sent_words: dict[int, Word] = {}
            for spacy_word in sentence:
                pos: Optional[MorphosyntacticFeature] = None
                if spacy_word.pos_:
                    pos = from_ud("POS", spacy_word.pos_)
                cltk_word = Word(
                    # Note: In order to match how Stanza orders token output
                    # (index starting at 1, not 0), we must add an extra 1 to each
                    index_token=spacy_word.i + 1,
                    index_char_start=spacy_word.idx,
                    index_char_stop=spacy_word.idx + len(spacy_word),
                    index_sentence=sentence_index,
                    string=spacy_word.text,  # same as ``token.text``
                    pos=pos,
                    xpos=spacy_word.tag_,
                    upos=spacy_word.pos_,
                    lemma=spacy_word.lemma_,
                    dependency_relation=spacy_word.dep_,  # str
                    stop=spacy_word.is_stop,
                    # Note: Must increment this, too
                    governor=spacy_word.head.i + 1,  # TODO: Confirm this is the index
                )
                raw_features: list[tuple[str, str]] = (
                    [
                        (feature, value)
                        for feature, value in spacy_word.morph.to_dict().items()
                    ]
                    if spacy_word.morph
                    else []
                )
                cltk_features = [
                    from_ud(feature_name, feature_value)
                    for feature_name, feature_value in raw_features
                ]
                cltk_word.features = MorphosyntacticFeatureBundle(*cltk_features)
                cltk_word.category = to_categorial(cltk_word.pos)
                sent_words[cltk_word.index_token] = cltk_word
                words_list.append(cltk_word)
        return words_list


@dataclass
class LatinSpacyProcess(SpacyProcess):
    """Run a Spacy model.

    <https://huggingface.co/latincy>_
    """

    language: Literal["lat"] = "lat"
    description: str = "Process for Spacy for Patrick Burn's Latin model."
    authorship_info: str = "``LatinSpacyProcess`` using LatinCy model by Patrick Burns from https://huggingface.co/latincy . Please cite: https://arxiv.org/abs/2305.04365"

@dataclass
class GreekSpacyProcess(SpacyProcess):
    """Run a Spacy model.

    <https://huggingface.co/chcaa>_
    """

    language: Literal["grc"] = "grc"
    description: str = "Process for Spacy for OdyCy's Greek model."
    authorship_info: str = "``GreekSpacyProcess`` using OdyCy model by Center for Humanities Computing Aarhus from https://huggingface.co/chcaa . Please cite: https://aclanthology.org/2023.latechclfl-1.14"
