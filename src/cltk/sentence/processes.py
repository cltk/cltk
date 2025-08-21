"""Module for sentence tokenizers."""

from copy import copy
from functools import cached_property
from types import FunctionType
from typing import Any, ClassVar

from cltk.core import CLTKException
from cltk.core.cltk_logger import logger
from cltk.core.data_types_v2 import Doc, Process
from cltk.sentence.non import OldNorseRegexSentenceTokenizer
from cltk.sentence.sentence import SentenceTokenizer
from cltk.sentence.utils import split_sentences_multilang

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class SentenceSplittingProcess(Process):
    """Base class for sentence splitting processes."""

    @cached_property
    def algorithm(self) -> FunctionType:
        # TODO: Decide whether to strip out section numbers with `text = strip_section_numbers(text)`
        logger.debug(f"Selecting normalization algorithm for language: {self.language}")
        if self.language in [
            "akk",
            "ang",
            "arc",
            "cop",
            "grc",
            "hbo",
            "lat",
            "non",
            "pli",
            "san",
            "arb",
            "chu",
            "enm",
            "frm",
            "fro",
            "gmh",
            "goh",
            "got",
            "hin",
            "lzh",
            "pan",
        ]:
            logger.debug(
                f"`SentenceSplittingProcess.algorithm()`: Selecting sentence splitter algorithm for {self.language}"
            )
            return split_sentences_multilang
        else:
            msg: str = f"`Sentence splitter not available for {self.language}`"
            logger.error(msg)
            raise ValueError(msg)

    def run(self, input_doc: Doc) -> Doc:
        output_doc = copy(input_doc)
        if not output_doc.normalized_text:
            msg: str = "Doc must have `normalized_text`."
            logger.error(msg)
            raise ValueError(msg)
        output_doc.sentence_boundaries = self.algorithm(
            text=output_doc.normalized_text, iso=output_doc.language.iso
        )
        return output_doc


class AkkadianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Akkadian."""


class AncientGreekSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Ancient Greek."""


class AncientHebrewSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Ancient Hebrew."""


class CopticSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Coptic."""


class LatinSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Latin."""


class OfficialAramaicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Official Aramaic."""


class OldEnglishSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old English."""


class OldNorseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Norse."""


class PaliSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Pali."""


class SanskritSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Sanskrit."""


class ArabicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Arabic."""


class ChurchSlavonicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Church Slavonic."""


class MiddleEnglishSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle English."""


class MiddleFrenchSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle French."""


class OldFrenchSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old French."""


class MiddleHighGermanSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle High German."""


class OldHighGermanSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old High German."""


class GothicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Gothic."""


class HindiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Hindi."""


class LiteraryChineseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Chinese."""


class PanjabiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Panjabi."""


# V1 below
class SentenceTokenizationProcessV1(Process):
    """To be inherited for each language's tokenization declarations.

    Example: ``SentenceTokenizationProcess`` -> ``OldNorseTokenizationProcess``

    >>> from cltk.tokenizers.processes import TokenizationProcess
    >>> from cltk.core.data_types import Process
    >>> issubclass(SentenceTokenizationProcess, Process)
    True
    >>> tok = SentenceTokenizationProcess()

    """

    # model = None
    model: ClassVar[Any] = None

    @cached_property
    def algorithm(self):
        raise CLTKException(
            f"No sentence tokenization algorithm for language '{self.language}'."
        )

    def run(self, input_doc: Doc) -> Doc:
        output_doc = copy(input_doc)
        sentence_tokenizer = self.algorithm
        if not isinstance(sentence_tokenizer, SentenceTokenizer):
            raise CLTKException(
                "Algorithm must be an instance of SentenceTokenizer subclass"
            )

        sentences = sentence_tokenizer.tokenize(output_doc.raw, self.model)
        sentence_indices = []
        for i, sentence in enumerate(sentences):
            if i >= 1:
                sentence_indices.append(sentence_indices[-1] + len(sentences[i]))
            else:
                sentence_indices.append(len(sentence))
        sentence_index = 0
        for j, word in enumerate(output_doc.words):
            if sentence_indices[
                sentence_index
            ] < word.index_char_stop and sentence_index + 1 < len(sentence_indices):
                sentence_index += 1
            word.index_sentence = sentence_index
        return output_doc


class OldNorseSentenceTokenizationProcess(SentenceTokenizationProcessV1):
    """
    The default Old Norse sentence tokenization algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.sentence.processes import OldNorseSentenceTokenizationProcess
    >>> from cltk.tokenizers import OldNorseTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text

    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
    processes=[OldNorseTokenizationProcess, OldNorseSentenceTokenizationProcess], \
    language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline=pipe, suppress_banner=True)
    >>> output_doc = nlp.analyze(get_example_text("non"))
    >>> len(output_doc.sentences_strings)
    7
    """

    @cached_property
    def algorithm(self):
        return OldNorseRegexSentenceTokenizer()
