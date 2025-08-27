"""Module for sentence tokenizers."""

from copy import copy
from functools import cached_property
from types import FunctionType
from typing import Any, ClassVar, Optional

from cltk.core.cltk_logger import logger
from cltk.core.data_types_v3 import Doc, Process
from cltk.core.exceptions import CLTKException

# from cltk.sentence.non import OldNorseRegexSentenceTokenizer
# from cltk.sentence.sentence import SentenceTokenizer
from cltk.sentence.utils import split_sentences_multilang

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class SentenceSplittingProcess(Process):
    """Base class for sentence splitting processes."""

    @cached_property
    def algorithm(self) -> FunctionType:
        # TODO: Decide whether to strip out section numbers with `text = strip_section_numbers(text)`
        logger.debug(
            f"Selecting normalization algorithm for language: {self.glottolog_id}"
        )
        if self.glottolog_id in [
            "akka1240",  # Akkadian
            "olde1238",  # Old English
            "impe1235",  # Imperial Aramaic
            "copt1239",  # Coptic
            "demo1234",  # Demotic
            "anci1242",  # Ancient Greek
            "anci1244",  # Biblical Hebrew
            "lati1261",  # Latin
            "oldn1244",  # Old Norse
            # "pli",
            "sans1269",  # Sanskrit
            "clas1259",  # Classical Arabic
            "chur1257",  # Old Church Slavonic
            "midd1317",  # Middle English
            "midd1316",  # Middle French; broke fix later
            "oldf1239",  # Old French
            "midd1343",  # Middle High German
            "oldh1241",  # Gothic
            # "got", #?
            # "hin",
            "lite1248",  # Literary Chinese
            # "pan",
        ]:
            logger.debug(
                f"`SentenceSplittingProcess.algorithm()`: Selecting sentence splitter algorithm for {self.glottolog_id}"
            )
            return split_sentences_multilang
        else:
            msg: str = f"`Sentence splitter not available for {self.glottolog_id}`"
            logger.error(msg)
            raise ValueError(msg)

    def run(self, input_doc: Doc) -> Doc:
        output_doc = copy(input_doc)
        if not output_doc.normalized_text:
            msg: str = "Doc must have `normalized_text`."
            logger.error(msg)
            raise ValueError(msg)
        logger.debug(
            f"Sentence splitter passed to split_sentences_multilang: {self.glottolog_id}"
        )
        output_doc.sentence_boundaries = self.algorithm(
            text=output_doc.normalized_text,
            glottolog_id=self.glottolog_id,
        )
        return output_doc


class AkkadianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Akkadian."""

    glottolog_id: Optional[str] = "akka1240"


class AncientGreekSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Ancient Greek."""

    glottolog_id: Optional[str] = "anci1242"


class AncientHebrewSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Ancient Hebrew."""

    glottolog_id: Optional[str] = "anci1244"


class CopticSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Coptic."""

    glottolog_id: Optional[str] = "copt1239"


class LatinSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Latin."""

    glottolog_id: Optional[str] = "lati1261"


class OfficialAramaicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Official Aramaic."""

    glottolog_id: Optional[str] = "impe1235"


class OldEnglishSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old English."""

    glottolog_id: Optional[str] = "olde1238"


class OldNorseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Norse."""

    glottolog_id: Optional[str] = "oldn1244"


class PaliSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Pali."""

    glottolog_id: Optional[str] = "pli"


class SanskritSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Sanskrit."""

    glottolog_id: Optional[str] = "sans1269"


class ClassicalArabicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Arabic."""

    glottolog_id: Optional[str] = "clas1259"


class ChurchSlavonicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Church Slavonic."""

    glottolog_id: Optional[str] = "chur1257"


class MiddleEnglishSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle English."""

    glottolog_id: Optional[str] = "midd1317"


class MiddleFrenchSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle French."""

    glottolog_id: Optional[str] = "midd1316"


class OldFrenchSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old French."""

    glottolog_id: Optional[str] = "oldf1239"


class MiddleHighGermanSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle High German."""

    glottolog_id: Optional[str] = "midd1343"


class OldHighGermanSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old High German."""

    glottolog_id: Optional[str] = "goh"


class GothicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Gothic."""

    glottolog_id: Optional[str] = "oldh1241"


class HindiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Hindi."""

    glottolog_id: Optional[str] = "hin"


class LiteraryChineseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Chinese."""

    glottolog_id: Optional[str] = "lite1248"


class PanjabiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Panjabi."""

    glottolog_id: Optional[str] = "pan"


class DemoticSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Egyptian."""

    glottolog_id: Optional[str] = "demo1234"


# V1 below
# class SentenceTokenizationProcessV1(Process):
#     """To be inherited for each language's tokenization declarations.

#     Example: ``SentenceTokenizationProcess`` -> ``OldNorseTokenizationProcess``

#     >>> from cltk.tokenizers.processes import TokenizationProcess
#     >>> from cltk.core.data_types import Process
#     >>> issubclass(SentenceTokenizationProcess, Process)
#     True
#     >>> tok = SentenceTokenizationProcess()

#     """

#     # model = None
#     model: ClassVar[Any] = None

#     @cached_property
#     def algorithm(self):
#         raise CLTKException(
#             f"No sentence tokenization algorithm for language '{self.glottolog_id}'."
#         )

#     def run(self, input_doc: Doc) -> Doc:
#         output_doc = copy(input_doc)
#         sentence_tokenizer = self.algorithm
#         if not isinstance(sentence_tokenizer, SentenceTokenizer):
#             raise CLTKException(
#                 "Algorithm must be an instance of SentenceTokenizer subclass"
#             )

#         sentences = sentence_tokenizer.tokenize(output_doc.raw, self.model)
#         sentence_indices = []
#         for i, sentence in enumerate(sentences):
#             if i >= 1:
#                 sentence_indices.append(sentence_indices[-1] + len(sentences[i]))
#             else:
#                 sentence_indices.append(len(sentence))
#         sentence_index = 0
#         for j, word in enumerate(output_doc.words):
#             if sentence_indices[
#                 sentence_index
#             ] < word.index_char_stop and sentence_index + 1 < len(sentence_indices):
#                 sentence_index += 1
#             word.index_sentence = sentence_index
#         return output_doc


# class OldNorseSentenceTokenizationProcess(SentenceTokenizationProcessV1):
#     """
#     The default Old Norse sentence tokenization algorithm.

#     >>> from cltk.core.data_types import Process, Pipeline
#     >>> from cltk.sentence.processes import OldNorseSentenceTokenizationProcess
#     >>> from cltk.tokenizers import OldNorseTokenizationProcess
#     >>> from cltk.languages.utils import get_lang
#     >>> from cltk.languages.example_texts import get_example_text

#     >>> from cltk.nlp import NLP
#     >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
#     processes=[OldNorseTokenizationProcess, OldNorseSentenceTokenizationProcess], \
#     language=get_lang("non"))
#     >>> nlp = NLP(language='non', custom_pipeline=pipe, suppress_banner=True)
#     >>> output_doc = nlp.analyze(get_example_text("non"))
#     >>> len(output_doc.sentences_strings)
#     7
#     """

#     @cached_property
#     def algorithm(self):
#         return OldNorseRegexSentenceTokenizer()
