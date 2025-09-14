"""Sentence splitting processes.

This module exposes a lightweight, language‑aware sentence splitter built
around regular expressions per language (identified by Glottolog codes).
It defines a generic ``SentenceSplittingProcess`` and many concrete
subclasses, one per language or stage.
"""

from copy import copy
from functools import cached_property
from typing import Callable, Optional

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import Doc, Process
from cltk.core.logging_utils import bind_from_doc
from cltk.sentence.utils import split_sentences_multilang

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class SentenceSplittingProcess(Process):
    """Base class for sentence splitting processes.

    Subclasses set ``glottolog_id`` and inherit the default algorithm,
    which delegates to a multi‑language regex splitter.

    Attributes:
      glottolog_id: Target language Glottolog code used to choose
        punctuation rules for sentence boundaries.

    """

    @cached_property
    def algorithm(self) -> Callable[[str, str], list[tuple[int, int]]]:
        """Return the language‑appropriate sentence boundary function.

        The returned callable takes ``(text, glottolog_id)`` and
        returns a list of ``(start, stop)`` character offsets for each
        sentence.

        Returns:
          A callable implementing sentence boundary detection.

        Raises:
          ValueError: If the ``glottolog_id`` is not supported.

        """
        # TODO: Consider stripping section numbers before splitting
        log = bind_context(glottolog_id=self.glottolog_id)
        log.debug(
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
            "vedi1234",  # Vedic Sanskrit
            "clas1258",  # Classical Sanskrit
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
            "cari1274",  # Carian
            "saur1252",  # Sauraseni Prakrit
            "maha1305",  # Maharastri Prakrit
            "maga1260",  # Magadhi Prakrit
            "gand1259",  # Gandhari
            # Canaanite / Northwest Semitic
            "moab1234",  # Moabite
            "ammo1234",  # Ammonite
            "edom1234",  # Edomite
            "sama1234",  # Samʾalian
            # Aramaic continuum
            "olda1246",  # Old Aramaic
            "olda1245",  # Old Aramaic–Samʾalian
            "midd1366",  # Middle Aramaic
            "clas1253",  # Classical Mandaic
            "hatr1234",  # Hatran
            "jewi1240",  # Jewish Babylonian Aramaic
            # Newly added: Hindi family lects
            "hind1269",  # Hindi (glottocode)
            "khad1239",  # Khari Boli (Hindi dialect)
            "braj1242",  # Braj Bhasha
            "awad1243",  # Awadhi
            "urdu1245",  # Urdu
            # Eastern Indo-Aryan and neighbors
            "beng1280",  # Bengali
            "oriy1255",  # Odia (Oriya)
            "assa1263",  # Assamese
            # Western Indo-Aryan
            "guja1252",  # Gujarati
            "mara1378",  # Marathi
            "bagr1243",  # Bagri (Rajasthani)
            # Southern Indo-Aryan / Indo-Aryan adjacency
            "sinh1246",  # Sinhala
            # Northwestern frontier
            "panj1256",  # Eastern Panjabi
            "sind1272",  # Sindhi
            "kash1277",  # Kashmiri
            # Sino-Tibetan
            "oldc1244",  # Old Chinese
            "midd1344",  # Middle Chinese
            "clas1255",  # Early Vernacular Chinese (Baihua)
            "oldb1235",  # Old Burmese
            "nucl1310",  # Classical Burmese
            "tang1334",  # Tangut
            "newa1246",  # Newar
            "mani1292",  # Meitei (Classical Manipuri)
            "sgaw1245",  # Sgaw Karen
            # Mongolic
            "mong1329",  # Middle Mongol
            "mong1331",  # Classical Mongolian
            "mogh1245",  # Mogholi (Moghol)
            # Afroasiatic (Berber/Cushitic/Chadic)
            "numi1241",  # Numidian
            "tait1247",  # Cushitic Taita
            "haus1257",  # Hausa
            # Altaic-Adj / Tungusic
            "jurc1239",  # Old Jurchen
            # Japonic / Uralic
            "japo1237",  # Old Japanese
            "oldh1242",  # Old Hungarian
            # Turkic / Dravidian
            "chag1247",  # Chagatai
            "oldu1238",  # Old Turkic
            "oldt1248",  # Old Tamil
        ]:
            log.debug(
                f"`SentenceSplittingProcess.algorithm()`: Selecting sentence splitter algorithm for {self.glottolog_id}"
            )
            return split_sentences_multilang
        else:
            msg: str = f"`Sentence splitter not available for {self.glottolog_id}`"
            log.error(msg)
            raise ValueError(msg)

    def run(self, input_doc: Doc) -> Doc:
        """Compute sentence boundaries and return an updated document.

        Args:
          input_doc: Document whose ``normalized_text`` will be segmented.

        Returns:
          A shallow copy of ``input_doc`` with ``sentence_boundaries`` set to
          a list of ``(start, stop)`` character indices.

        Raises:
          ValueError: If ``normalized_text`` is missing or if ``glottolog_id``
            is not set on the process.

        """
        output_doc = copy(input_doc)
        log = bind_from_doc(output_doc)
        if not output_doc.normalized_text:
            msg: str = "Doc must have `normalized_text`."
            log.error(msg)
            raise ValueError(msg)
        log.debug(
            f"Sentence splitter passed to split_sentences_multilang: {self.glottolog_id}"
        )
        # Ensure required attributes are present
        if self.glottolog_id is None:
            raise ValueError("glottolog_id must be set for sentence splitting")
        # Callable typing does not retain keyword names; pass positionally
        output_doc.sentence_boundaries = self.algorithm(
            output_doc.normalized_text,
            self.glottolog_id,
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

    glottolog_id: Optional[str] = "cari1274"


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


class ClassicalSanskritSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Sanskrit."""

    glottolog_id: Optional[str] = "clas1258"


class VedicSanskritSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Vedic Sanskrit."""

    glottolog_id: Optional[str] = "vedi1234"


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

    glottolog_id: Optional[str] = "hind1269"


class KhariBoliSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Khari Boli (Hindi dialect)."""

    glottolog_id: Optional[str] = "khad1239"


class BrajSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Braj Bhasha."""

    glottolog_id: Optional[str] = "braj1242"


class AwadhiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Awadhi."""

    glottolog_id: Optional[str] = "awad1243"


class UrduSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Urdu."""

    glottolog_id: Optional[str] = "urdu1245"


class LiteraryChineseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Chinese."""

    glottolog_id: Optional[str] = "lite1248"


class OldChineseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Chinese."""

    glottolog_id: Optional[str] = "oldc1244"


class MiddleChineseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle Chinese."""

    glottolog_id: Optional[str] = "midd1344"


class BaihuaChineseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Early Vernacular Chinese (Baihua)."""

    glottolog_id: Optional[str] = "clas1255"


class PanjabiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Panjabi."""

    glottolog_id: Optional[str] = "panj1256"


class ParthianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Parthian."""

    glottolog_id: Optional[str] = "part1239"


class DemoticSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Egyptian."""

    glottolog_id: Optional[str] = "demo1234"


class BengaliSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Bengali."""

    glottolog_id: Optional[str] = "beng1280"


class OdiaSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Odia (Oriya)."""

    glottolog_id: Optional[str] = "oriy1255"


class AssameseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Assamese."""

    glottolog_id: Optional[str] = "assa1263"


class GujaratiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Gujarati."""

    glottolog_id: Optional[str] = "guja1252"


class MarathiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Marathi."""

    glottolog_id: Optional[str] = "mara1378"


class BagriSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Bagri (Rajasthani)."""

    glottolog_id: Optional[str] = "bagr1243"


class SinhalaSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Sinhala."""

    glottolog_id: Optional[str] = "sinh1246"


class SindhiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Sindhi."""

    glottolog_id: Optional[str] = "sind1272"


class KashmiriSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Kashmiri."""

    glottolog_id: Optional[str] = "kash1277"


class OldBurmeseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Burmese."""

    glottolog_id: Optional[str] = "oldb1235"


class ClassicalBurmeseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Burmese."""

    glottolog_id: Optional[str] = "nucl1310"


class TangutSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Tangut."""

    glottolog_id: Optional[str] = "tang1334"


class NewarSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Newar (Classical Nepal Bhasa)."""

    glottolog_id: Optional[str] = "newa1246"


class MeiteiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Meitei (Classical Manipuri)."""

    glottolog_id: Optional[str] = "mani1292"


class SgawKarenSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Sgaw Karen."""

    glottolog_id: Optional[str] = "sgaw1245"


class MiddleMongolSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle Mongol."""

    glottolog_id: Optional[str] = "mong1329"


class ClassicalMongolianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Mongolian."""

    glottolog_id: Optional[str] = "mong1331"


class MogholiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Mogholi (Moghol)."""

    glottolog_id: Optional[str] = "mogh1245"


class NumidianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Numidian (Ancient Berber)."""

    glottolog_id: Optional[str] = "numi1241"


class TaitaSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Cushitic Taita."""

    glottolog_id: Optional[str] = "tait1247"


class HausaSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Hausa."""

    glottolog_id: Optional[str] = "haus1257"


class OldJurchenSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Jurchen."""

    glottolog_id: Optional[str] = "jurc1239"


class OldJapaneseSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Japanese."""

    glottolog_id: Optional[str] = "japo1237"


class OldHungarianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Hungarian."""

    glottolog_id: Optional[str] = "oldh1242"


class ChagataiSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Chagatai."""

    glottolog_id: Optional[str] = "chag1247"


class OldTurkicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Turkic."""

    glottolog_id: Optional[str] = "oldu1238"


class OldTamilSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Tamil."""

    glottolog_id: Optional[str] = "oldt1248"


class HittiteSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitter for Hittite (hit1242)."""

    glottolog_id: Optional[str] = "hitt1242"


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


class SauraseniPrakritSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Sauraseni Prakrit."""

    glottolog_id: Optional[str] = "saur1252"


class MaharastriPrakritSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Maharastri Prakrit."""

    glottolog_id: Optional[str] = "maha1305"


class MagadhiPrakritSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Magadhi Prakrit."""

    glottolog_id: Optional[str] = "maga1260"


class GandhariSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Gandhari."""

    glottolog_id: Optional[str] = "gand1259"


class MoabiteSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Moabite."""

    glottolog_id: Optional[str] = "moab1234"


class AmmoniteSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Ammonite."""

    glottolog_id: Optional[str] = "ammo1234"


class EdomiteSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Edomite."""

    glottolog_id: Optional[str] = "edom1234"


class OldAramaicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Aramaic (up to 700 BCE)."""

    glottolog_id: Optional[str] = "olda1246"


class OldAramaicSamalianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Old Aramaic–Samʾalian."""

    glottolog_id: Optional[str] = "olda1245"


class MiddleAramaicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Middle Aramaic."""

    glottolog_id: Optional[str] = "midd1366"


class ClassicalMandaicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Classical Mandaic."""

    glottolog_id: Optional[str] = "clas1253"


class HatranSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Hatran."""

    glottolog_id: Optional[str] = "hatr1234"


class JewishBabylonianAramaicSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Jewish Babylonian Aramaic."""

    glottolog_id: Optional[str] = "jewi1240"


class SamalianSentenceSplittingProcess(SentenceSplittingProcess):
    """Sentence splitting process for Samʾalian."""

    glottolog_id: Optional[str] = "sama1234"
