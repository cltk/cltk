"""Module for sentence tokenizers."""

from copy import copy
from functools import cached_property
from types import FunctionType
from typing import Any, ClassVar, List, Optional, Tuple

from cltk.core.cltk_logger import logger
from cltk.core.data_types_v3 import Doc, Process
from cltk.core.exceptions import CLTKException
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
            "pali1273",  # Pali
            "sans1269",  # Sanskrit
            "clas1259",  # Classical Arabic
            "chur1257",  # Old Church Slavonic
            "midd1317",  # Middle English
            "midd1316",  # Middle French; broke fix later
            "oldf1239",  # Old French
            "midd1343",  # Middle High German
            "goth1244",  # Gothic
            "oldh1241",  # Old High German
            "lite1248",  # Literary Chinese
            "clas1252",  # Classical Syriac
            "oldp1254",  # Old Persian
            "oldi1245",  # Early Irish
            "ugar1238",  # Ugaritic
            "phoe1239",  # Phoenician
            "geez1241",  # Geez
            "midd1369",  # Middle Egyptian
            "olde1242",  # Old Egyptian
            "late1256",  # Late Egyptian
            "clas1254",  # Classical Tibetan
            "pahl1241",  # Middle Persian
            "part1239",  # Parthian
            "aves1237",  # Avestan
            "bact1239",  # Bactrian
            "sogd1245",  # Sogdian
            "khot1251",  # Khotanese
            "tums1237",  # Tumshuqese
            "oldw1239",  # Old Welsh
            "bret1244",  # Old-Middle Breton
            "corn1251",  # Cornish
            "prus1238",  # Old Prussian
            "lith1251",  # Lithuanian
            "latv1249",  # Latvian
            "gheg1238",  # Albanian
            "clas1256",  # Classical Armenian
            "midd1364",  # Middle Armenian
            "cune1239",  # Cuneiform Luwian
            "hier1240",  # Hieroglyphic Luwian
            "lyci1241",  # Lycian A
            "lydi1241",  # Lydian
            "pala1331",  # Palaic
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


class LycianASentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Lycian."""

    glottolog_id: Optional[str] = "lyci1241"


class LydianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Lydian."""

    glottolog_id: Optional[str] = "lydi1241"


class PalaicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Palaic."""

    glottolog_id: Optional[str] = "pala1331"


class CarianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Carian."""

    glottolog_id: Optional[str] = "cari1273"


class CuneiformLuwianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Cuneiform Luwian."""

    glottolog_id: Optional[str] = "cune1239"


class HieroglyphicLuwianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Hieroglyphic Luwian."""

    glottolog_id: Optional[str] = "hier1240"


class ClassicalArmenianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Armenian."""

    glottolog_id: Optional[str] = "clas1256"


class MiddleArmenianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle Armenian."""

    glottolog_id: Optional[str] = "midd1364"


class AkkadianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Akkadian."""

    glottolog_id: Optional[str] = "akka1240"


class AncientGreekSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Ancient Greek."""

    glottolog_id: Optional[str] = "anci1242"


class AncientHebrewSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Ancient Hebrew."""

    glottolog_id: Optional[str] = "anci1244"


class ClassicalSyriacSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Syriac."""

    glottolog_id: Optional[str] = "clas1252"


class ClassicalTibetanSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Tibetan."""

    glottolog_id: Optional[str] = "clas1254"


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

    glottolog_id: Optional[str] = "pali1273"


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


class MiddlePersianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle Persian."""

    glottolog_id: Optional[str] = "pahl1241"


class OldFrenchSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old French."""

    glottolog_id: Optional[str] = "oldf1239"


class MiddleHighGermanSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle High German."""

    glottolog_id: Optional[str] = "midd1343"


class OldHighGermanSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old High German."""

    glottolog_id: Optional[str] = "oldh1241"


class GothicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Gothic."""

    glottolog_id: Optional[str] = "goth1244"


class HindiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Hindi."""

    glottolog_id: Optional[str] = "hin"


class LiteraryChineseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Chinese."""

    glottolog_id: Optional[str] = "lite1248"


class PanjabiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Panjabi."""

    glottolog_id: Optional[str] = "pan"


class ParthianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Parthian."""

    glottolog_id: Optional[str] = "part1239"


class DemoticSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Egyptian."""

    glottolog_id: Optional[str] = "demo1234"


class HittiteSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Hittite (hit1242)."""

    glottolog_id: Optional[str] = "hit1242"


class TocharianASentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Tocharian A (toch1238)."""

    glottolog_id: Optional[str] = "toch1238"


class TocharianBSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Tocharian B (toch1237)."""

    glottolog_id: Optional[str] = "toch1237"


class AvestanSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Avestan (aves1237)."""

    glottolog_id: Optional[str] = "aves1237"


class BactrianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Bactrian (bact1239)."""

    glottolog_id: Optional[str] = "bact1239"


class SogdianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Sogdian (sogd1245)."""

    glottolog_id: Optional[str] = "sogd1245"


class KhotaneseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Khotanese (khot1251)."""

    glottolog_id: Optional[str] = "khot1251"


class TumshuqeseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Tumshuqese (tums1237)."""

    glottolog_id: Optional[str] = "tums1237"


class OldPersianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Old Persian (oldp1254)."""

    glottolog_id: Optional[str] = "oldp1254"


class EarlyIrishSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Old Irish (oldi1245)."""

    glottolog_id: Optional[str] = "oldi1245"


class UgariticSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Ugaritic (ugar1238)."""

    glottolog_id: Optional[str] = "ugar1238"


class PhoenicianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Phoenician (phoe1239)."""

    glottolog_id: Optional[str] = "phoe1239"


class GeezSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Geez (geez1241)."""

    glottolog_id: Optional[str] = "geez1241"


class MiddleEgyptianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Middle Egyptian (midd1369)."""

    glottolog_id: Optional[str] = "midd1369"


class OldEgyptianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Old Egyptian (olde1242)."""

    glottolog_id: Optional[str] = "olde1242"


class LateEgyptianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Late Egyptian (late1256)."""

    glottolog_id: Optional[str] = "late1256"


class OldMiddleWelshSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle Welsh."""

    glottolog_id: Optional[str] = "midd1254"


class MiddleBretonSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle Breton."""

    glottolog_id: Optional[str] = "midb1244"


class MiddleCornishSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Cornish."""

    glottolog_id: Optional[str] = "corn1251"


class OldPrussianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Prussian."""

    glottolog_id: Optional[str] = "prus1238"


class LithuanianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Lithuanian."""

    glottolog_id: Optional[str] = "lith1251"


class LatvianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Latvian."""

    glottolog_id: Optional[str] = "latv1249"


class AlbanianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Albanian."""

    glottolog_id: Optional[str] = "gheg1238"
