"""Default processing pipelines for languages. The purpose of
these dataclasses is to represent:

1. the types of NLP processes that the CLTK can do
2. the order in which processes are to be executed
3. specifying what downstream features a particular implemented process requires
"""

from dataclasses import dataclass, field
from typing import List, Type

from cltk.alphabet.processes import GreekNormalizeProcess, LatinNormalizeProcess
from cltk.core.data_types import Language, Pipeline, Process
from cltk.dependency.processes import (
    ChineseStanzaProcess,
    CopticStanzaProcess,
    GothicStanzaProcess,
    GreekStanzaProcess,
    LatinStanzaProcess,
    OCSStanzaProcess,
    OldFrenchStanzaProcess,
)
from cltk.embeddings.processes import (
    ArabicEmbeddingsProcess,
    AramaicEmbeddingsProcess,
    GothicEmbeddingsProcess,
    GreekEmbeddingsProcess,
    LatinEmbeddingsProcess,
    OldEnglishEmbeddingsProcess,
    PaliEmbeddingsProcess,
    SanskritEmbeddingsProcess,
)
from cltk.languages.utils import get_lang
from cltk.lemmatize.processes import (
    GreekLemmatizationProcess,
    LatinLemmatizationProcess,
    OldEnglishLemmatizationProcess,
    OldFrenchLemmatizationProcess,
)
from cltk.lexicon.processes import LatinLexiconProcess, OldNorseLexiconProcess
from cltk.ner.processes import (
    # GreekNERProcess,
    # LatinNERProcess,
    # OldEnglishNERProcess,
    OldFrenchNERProcess,
)
from cltk.stops.processes import StopsProcess
from cltk.tokenizers.processes import (
    AkkadianTokenizationProcess,
    ArabicTokenizationProcess,
    GreekTokenizationProcess,
    LatinTokenizationProcess,
    MiddleEnglishTokenizationProcess,
    MiddleFrenchTokenizationProcess,
    MiddleHighGermanTokenizationProcess,
    MultilingualTokenizationProcess,
    OldFrenchTokenizationProcess,
    OldNorseTokenizationProcess,
)


@dataclass
class AkkadianPipeline(Pipeline):
    """Default ``Pipeline`` for Akkadian.

    >>> from cltk.languages.pipelines import AkkadianPipeline
    >>> a_pipeline = AkkadianPipeline()
    >>> a_pipeline.description
    'Pipeline for the Akkadian language.'
    >>> a_pipeline.language
    Language(name='Akkadian', glottolog_id='akka1240', latitude=33.1, longitude=44.1, dates=[], family_id='afro1255', parent_id='east2678', level='language', iso_639_3_code='akk', type='a')
    >>> a_pipeline.language.name
    'Akkadian'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.AkkadianTokenizationProcess'>
    """

    description: str = "Pipeline for the Akkadian language."
    language: Language = get_lang("akk")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [AkkadianTokenizationProcess, StopsProcess]
    )


@dataclass
class ArabicPipeline(Pipeline):
    """Default ``Pipeline`` for Arabic.

    >>> from cltk.languages.pipelines import ArabicPipeline
    >>> a_pipeline = ArabicPipeline()
    >>> a_pipeline.description
    'Pipeline for the Arabic language'
    >>> a_pipeline.language
    Language(name='Standard Arabic', glottolog_id='stan1318', latitude=27.9625, longitude=43.8525, dates=[], family_id='afro1255', parent_id='arab1395', level='language', iso_639_3_code='arb', type='')
    >>> a_pipeline.language.name
    'Standard Arabic'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.ArabicTokenizationProcess'>
    """

    description: str = "Pipeline for the Arabic language"
    language: Language = get_lang("arb")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [
            ArabicTokenizationProcess,
            ArabicEmbeddingsProcess,
            StopsProcess,
        ]
    )


@dataclass
class AramaicPipeline(Pipeline):
    """Default ``Pipeline`` for Aramaic.

    TODO: Confirm with specialist what encodings should be expected.
    TODO: Replace ``ArabicTokenizationProcess`` with a multilingual one or a specific Aramaic.

    >>> from cltk.languages.pipelines import AramaicPipeline
    >>> a_pipeline = AramaicPipeline()
    >>> a_pipeline.description
    'Pipeline for the Aramaic language'
    >>> a_pipeline.language
    Language(name='Official Aramaic (700-300 BCE)', glottolog_id='', latitude=0.0, longitude=0.0, dates=[], family_id='', parent_id='', level='', iso_639_3_code='arc', type='a')
    >>> a_pipeline.language.name
    'Official Aramaic (700-300 BCE)'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.ArabicTokenizationProcess'>
    """

    description: str = "Pipeline for the Aramaic language"
    language: Language = get_lang("arc")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [
            ArabicTokenizationProcess,  # Note: Using Arabic tokenizer for Aramaic. Is this OK?
            AramaicEmbeddingsProcess,
        ]
    )


@dataclass
class ChinesePipeline(Pipeline):
    """Default ``Pipeline`` for Classical Chinese.

    >>> from cltk.languages.pipelines import ChinesePipeline
    >>> a_pipeline = ChinesePipeline()
    >>> a_pipeline.description
    'Pipeline for the Classical Chinese language'
    >>> a_pipeline.language
    Language(name='Literary Chinese', glottolog_id='lite1248', latitude=0.0, longitude=0.0, dates=[], family_id='sino1245', parent_id='clas1255', level='language', iso_639_3_code='lzh', type='h')
    >>> a_pipeline.language.name
    'Literary Chinese'
    >>> a_pipeline.processes[0]
    <class 'cltk.dependency.processes.ChineseStanzaProcess'>
    """

    description: str = "Pipeline for the Classical Chinese language"
    language: Language = get_lang("lzh")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [ChineseStanzaProcess]
    )


@dataclass
class CopticPipeline(Pipeline):
    """Default ``Pipeline`` for Coptic.

    >>> from cltk.languages.pipelines import CopticPipeline
    >>> a_pipeline = CopticPipeline()
    >>> a_pipeline.description
    'Pipeline for the Coptic language'
    >>> a_pipeline.language
    Language(name='Coptic', glottolog_id='copt1239', latitude=29.472, longitude=31.2053, dates=[], family_id='afro1255', parent_id='egyp1245', level='language', iso_639_3_code='cop', type='')
    >>> a_pipeline.language.name
    'Coptic'
    >>> a_pipeline.processes[0]
    <class 'cltk.dependency.processes.CopticStanzaProcess'>
    """

    description: str = "Pipeline for the Coptic language"
    language: Language = get_lang("cop")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [CopticStanzaProcess, StopsProcess]
    )


@dataclass
class GothicPipeline(Pipeline):
    """Default ``Pipeline`` for Gothic.

    >>> from cltk.languages.pipelines import GothicPipeline
    >>> a_pipeline = GothicPipeline()
    >>> a_pipeline.description
    'Pipeline for the Gothic language'
    >>> a_pipeline.language
    Language(name='Gothic', glottolog_id='goth1244', latitude=46.9304, longitude=29.9786, dates=[], family_id='indo1319', parent_id='east2805', level='language', iso_639_3_code='got', type='a')
    >>> a_pipeline.language.name
    'Gothic'
    >>> a_pipeline.processes[0]
    <class 'cltk.dependency.processes.GothicStanzaProcess'>
    >>> a_pipeline.processes[1]
    <class 'cltk.embeddings.processes.GothicEmbeddingsProcess'>
    """

    description: str = "Pipeline for the Gothic language"
    language: Language = get_lang("got")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [GothicStanzaProcess, GothicEmbeddingsProcess]
    )


@dataclass
class GreekPipeline(Pipeline):
    """Default ``Pipeline`` for Ancient Greek.

    >>> from cltk.languages.pipelines import GreekPipeline
    >>> a_pipeline = GreekPipeline()
    >>> a_pipeline.description
    'Pipeline for the Greek language'
    >>> a_pipeline.language
    Language(name='Ancient Greek', glottolog_id='anci1242', latitude=39.8155, longitude=21.9129, dates=[], family_id='indo1319', parent_id='east2798', level='language', iso_639_3_code='grc', type='h')
    >>> a_pipeline.language.name
    'Ancient Greek'
    >>> a_pipeline.processes[0]
    <class 'cltk.alphabet.processes.GreekNormalizeProcess'>
    """

    description: str = "Pipeline for the Greek language"
    language: Language = get_lang("grc")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [
            # GreekTokenizationProcess,
            GreekNormalizeProcess,
            GreekStanzaProcess,
            GreekEmbeddingsProcess,
            StopsProcess,
            # GreekNERProcess,
        ]
    )


@dataclass
class HindiPipeline(Pipeline):
    """Default ``Pipeline`` for Hindi.

    >>> from cltk.languages.pipelines import HindiPipeline
    >>> a_pipeline = HindiPipeline()
    >>> a_pipeline.description
    'Pipeline for the Hindi language.'
    >>> a_pipeline.language
    Language(name='Hindi', glottolog_id='hind1269', latitude=25.0, longitude=77.0, dates=[], family_id='indo1319', parent_id='hind1270', level='language', iso_639_3_code='hin', type='')
    >>> a_pipeline.language.name
    'Hindi'
    >>> a_pipeline.processes[1]
    <class 'cltk.stops.processes.StopsProcess'>
    """

    description: str = "Pipeline for the Hindi language."
    language: Language = get_lang("hin")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [MultilingualTokenizationProcess, StopsProcess]
    )


@dataclass
class LatinPipeline(Pipeline):
    """Default ``Pipeline`` for Latin.

    TODO: Add stopword annotation for all relevant pipelines.

    >>> from cltk.languages.pipelines import LatinPipeline
    >>> a_pipeline = LatinPipeline()
    >>> a_pipeline.description
    'Pipeline for the Latin language'
    >>> a_pipeline.language
    Language(name='Latin', glottolog_id='lati1261', latitude=41.9026, longitude=12.4502, dates=[], family_id='indo1319', parent_id='impe1234', level='language', iso_639_3_code='lat', type='a')
    >>> a_pipeline.language.name
    'Latin'
    >>> a_pipeline.processes[0]
    <class 'cltk.alphabet.processes.LatinNormalizeProcess'>
    """

    description: str = "Pipeline for the Latin language"
    language: Language = get_lang("lat")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [
            LatinNormalizeProcess,
            # LatinTokenizationProcess,
            LatinStanzaProcess,
            LatinEmbeddingsProcess,
            StopsProcess,
            # LatinNERProcess,
            LatinLexiconProcess,
        ]
    )


@dataclass
class MiddleHighGermanPipeline(Pipeline):
    """Default ``Pipeline`` for Middle High German.

    >>> a_pipeline = MiddleHighGermanPipeline()
    >>> a_pipeline.description
    'Pipeline for the Middle High German language.'
    >>> a_pipeline.language
    Language(name='Middle High German', glottolog_id='midd1343', latitude=0.0, longitude=0.0, dates=[], family_id='indo1319', parent_id='midd1349', level='language', iso_639_3_code='gmh', type='h')
    >>> a_pipeline.language.name
    'Middle High German'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.MiddleHighGermanTokenizationProcess'>
    """

    description: str = "Pipeline for the Middle High German language."
    language: Language = get_lang("gmh")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [MiddleHighGermanTokenizationProcess, StopsProcess]
    )


@dataclass
class MiddleEnglishPipeline(Pipeline):
    """Default ``Pipeline`` for Middle English.

    TODO: Figure out whether this the dedicated tokenizer is good enough or necessary; we have stanza for Old English, which might be able to tokenizer fine.

    >>> from cltk.languages.pipelines import MiddleEnglishPipeline
    >>> a_pipeline = MiddleEnglishPipeline()
    >>> a_pipeline.description
    'Pipeline for the Middle English language'
    >>> a_pipeline.language
    Language(name='Middle English', glottolog_id='midd1317', latitude=0.0, longitude=0.0, dates=[], family_id='indo1319', parent_id='merc1242', level='language', iso_639_3_code='enm', type='h')
    >>> a_pipeline.language.name
    'Middle English'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.MiddleEnglishTokenizationProcess'>
    """

    description: str = "Pipeline for the Middle English language"
    language: Language = get_lang("enm")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [MiddleEnglishTokenizationProcess, StopsProcess]
    )


@dataclass
class MiddleFrenchPipeline(Pipeline):
    """Default ``Pipeline`` for Middle French.

    TODO: Figure out whether this the dedicated tokenizer is good enough or necessary; we have stanza for Old French, which might be able to tokenizer fine.

    >>> from cltk.languages.pipelines import MiddleFrenchPipeline
    >>> a_pipeline = MiddleFrenchPipeline()
    >>> a_pipeline.description
    'Pipeline for the Middle French language'
    >>> a_pipeline.language
    Language(name='Middle French', glottolog_id='midd1316', latitude=0.0, longitude=0.0, dates=[], family_id='indo1319', parent_id='stan1290', level='dialect', iso_639_3_code='frm', type='h')
    >>> a_pipeline.language.name
    'Middle French'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.MiddleFrenchTokenizationProcess'>
    """

    description: str = "Pipeline for the Middle French language"
    language: Language = get_lang("frm")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [MiddleFrenchTokenizationProcess]
    )


@dataclass
class OCSPipeline(Pipeline):
    """Default ``Pipeline`` for Old Church Slavonic.

    >>> from cltk.languages.pipelines import OCSPipeline
    >>> a_pipeline = OCSPipeline()
    >>> a_pipeline.description
    'Pipeline for the Old Church Slavonic language'
    >>> a_pipeline.language
    Language(name='Church Slavic', glottolog_id='chur1257', latitude=43.7171, longitude=22.8442, dates=[], family_id='indo1319', parent_id='east2269', level='language', iso_639_3_code='chu', type='a')
    >>> a_pipeline.language.name
    'Church Slavic'
    >>> a_pipeline.processes[0]
    <class 'cltk.dependency.processes.OCSStanzaProcess'>
    """

    description: str = "Pipeline for the Old Church Slavonic language"
    language: Language = get_lang("chu")
    processes: List[Type[Process]] = field(default_factory=lambda: [OCSStanzaProcess])


@dataclass
class OldEnglishPipeline(Pipeline):
    """Default ``Pipeline`` for Old English.

    >>> from cltk.languages.pipelines import OldEnglishPipeline
    >>> a_pipeline = OldEnglishPipeline()
    >>> a_pipeline.description
    'Pipeline for the Old English language'
    >>> a_pipeline.language
    Language(name='Old English (ca. 450-1100)', glottolog_id='olde1238', latitude=51.06, longitude=-1.31, dates=[], family_id='indo1319', parent_id='angl1265', level='language', iso_639_3_code='ang', type='h')
    >>> a_pipeline.language.name
    'Old English (ca. 450-1100)'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.MultilingualTokenizationProcess'>
    """

    description: str = "Pipeline for the Old English language"
    language: Language = get_lang("ang")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [
            MultilingualTokenizationProcess,
            OldEnglishLemmatizationProcess,
            OldEnglishEmbeddingsProcess,
            StopsProcess,
            # OldEnglishNERProcess,
        ]
    )


@dataclass
class OldFrenchPipeline(Pipeline):
    """Default ``Pipeline`` for Old French.

    >>> from cltk.languages.pipelines import OldFrenchPipeline
    >>> a_pipeline = OldFrenchPipeline()
    >>> a_pipeline.description
    'Pipeline for the Old French language'
    >>> a_pipeline.language
    Language(name='Old French (842-ca. 1400)', glottolog_id='oldf1239', latitude=0.0, longitude=0.0, dates=[], family_id='indo1319', parent_id='oila1234', level='language', iso_639_3_code='fro', type='h')
    >>> a_pipeline.language.name
    'Old French (842-ca. 1400)'
    >>> a_pipeline.processes[0]
    <class 'cltk.dependency.processes.OldFrenchStanzaProcess'>
    """

    description: str = "Pipeline for the Old French language"
    language: Language = get_lang("fro")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [
            # OldFrenchTokenizationProcess,
            OldFrenchStanzaProcess,
            StopsProcess,
            OldFrenchNERProcess,
        ]
    )


# TODO: Add Old Marathi ("omr")


@dataclass
class OldNorsePipeline(Pipeline):
    """Default ``Pipeline`` for Old Norse.

    >>> from cltk.languages.pipelines import OldNorsePipeline
    >>> a_pipeline = OldNorsePipeline()
    >>> a_pipeline.description
    'Pipeline for the Old Norse language'
    >>> a_pipeline.language
    Language(name='Old Norse', glottolog_id='oldn1244', latitude=63.42, longitude=10.38, dates=[], family_id='indo1319', parent_id='west2805', level='language', iso_639_3_code='non', type='h')
    >>> a_pipeline.language.name
    'Old Norse'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.OldNorseTokenizationProcess'>
    """

    description: str = "Pipeline for the Old Norse language"
    language: Language = get_lang("non")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [
            OldNorseTokenizationProcess,
            StopsProcess,
            OldNorseLexiconProcess,
        ]
    )


@dataclass
class PaliPipeline(Pipeline):
    """Default ``Pipeline`` for Pali.

    TODO: Make better tokenizer for Pali.

    >>> from cltk.languages.pipelines import PaliPipeline
    >>> a_pipeline = PaliPipeline()
    >>> a_pipeline.description
    'Pipeline for the Pali language'
    >>> a_pipeline.language
    Language(name='Pali', glottolog_id='pali1273', latitude=24.5271, longitude=82.251, dates=[], family_id='indo1319', parent_id='biha1245', level='language', iso_639_3_code='pli', type='a')
    >>> a_pipeline.language.name
    'Pali'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.MultilingualTokenizationProcess'>
    """

    description: str = "Pipeline for the Pali language"
    language: Language = get_lang("pli")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [MultilingualTokenizationProcess, PaliEmbeddingsProcess]
    )


@dataclass
class PanjabiPipeline(Pipeline):
    """Default ``Pipeline`` for Panjabi.

    >>> from cltk.languages.pipelines import SanskritPipeline
    >>> a_pipeline = PanjabiPipeline()
    >>> a_pipeline.description
    'Pipeline for the Panjabi language.'
    >>> a_pipeline.language
    Language(name='Eastern Panjabi', glottolog_id='panj125', latitude=30.0368, longitude=75.6702, dates=[], family_id='indo1319', parent_id='east2727', level='language', iso_639_3_code='pan', type='')
    >>> a_pipeline.language.name
    'Eastern Panjabi'
    >>> a_pipeline.processes[1]
    <class 'cltk.stops.processes.StopsProcess'>
    """

    description: str = "Pipeline for the Panjabi language."
    language: Language = get_lang("pan")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [MultilingualTokenizationProcess, StopsProcess]
    )


@dataclass
class SanskritPipeline(Pipeline):
    """Default ``Pipeline`` for Sanskrit.

    TODO: Make better tokenizer for Sanskrit.

    >>> from cltk.languages.pipelines import SanskritPipeline
    >>> a_pipeline = SanskritPipeline()
    >>> a_pipeline.description
    'Pipeline for the Sanskrit language.'
    >>> a_pipeline.language
    Language(name='Sanskrit', glottolog_id='sans1269', latitude=20.0, longitude=77.0, dates=[], family_id='indo1319', parent_id='indo1321', level='language', iso_639_3_code='san', type='a')
    >>> a_pipeline.language.name
    'Sanskrit'
    >>> a_pipeline.processes[1]
    <class 'cltk.embeddings.processes.SanskritEmbeddingsProcess'>
    """

    description: str = "Pipeline for the Sanskrit language."
    language: Language = get_lang("san")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [
            MultilingualTokenizationProcess,
            SanskritEmbeddingsProcess,
            StopsProcess,
        ]
    )
