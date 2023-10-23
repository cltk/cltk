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
    MiddleEnglishEmbeddingsProcess,
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
    OldFrenchNERProcess,
)  # GreekNERProcess,; LatinNERProcess,; OldEnglishNERProcess,
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
    Language(name='Akkadian', glottolog_id='akka1240', latitude=33.1, longitude=44.1, family_id='afro1255', parent_id='east2678', level='language', iso_639_3_code='akk', type='a', dates=[])
    >>> a_pipeline.language.name
    'Akkadian'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.AkkadianTokenizationProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(
        self, processes=None, description="Pipeline for the Akkadian language."
    ):
        language = get_lang("akk")
        if not processes:
            processes = [AkkadianTokenizationProcess, StopsProcess]
        super().__init__(language, description, processes)


@dataclass
class ArabicPipeline(Pipeline):
    """Default ``Pipeline`` for Arabic.

    >>> from cltk.languages.pipelines import ArabicPipeline
    >>> a_pipeline = ArabicPipeline()
    >>> a_pipeline.description
    'Pipeline for the Arabic language'
    >>> a_pipeline.language
    Language(name='Standard Arabic', glottolog_id='stan1318', latitude=27.9625, longitude=43.8525, family_id='afro1255', parent_id='arab1395', level='language', iso_639_3_code='arb', type='', dates=[])
    >>> a_pipeline.language.name
    'Standard Arabic'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.ArabicTokenizationProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(self, processes=None, description="Pipeline for the Arabic language"):
        language = get_lang("arb")
        if not processes:
            processes = [
                ArabicTokenizationProcess,
                ArabicEmbeddingsProcess,
                StopsProcess,
            ]
        super().__init__(language, description, processes)


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
    Language(name='Official Aramaic (700-300 BCE)', glottolog_id='', latitude=0.0, longitude=0.0, family_id='', parent_id='', level='', iso_639_3_code='arc', type='a', dates=[])
    >>> a_pipeline.language.name
    'Official Aramaic (700-300 BCE)'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.ArabicTokenizationProcess'>
    """

    description: str = "Pipeline for the Aramaic language"
    language: Language = field(default_factory=lambda: get_lang("arc"))
    processes: List[Type[Process]] = field(
        default_factory=lambda: [
            ArabicTokenizationProcess,  # Note: Using Arabic tokenizer for Aramaic. Is this OK?
            AramaicEmbeddingsProcess,
        ]
    )

    def __init__(self, processes=None, description="Pipeline for the Latin language"):
        language = get_lang("lat")
        if not processes:
            processes = [
                LatinNormalizeProcess,
                # LatinTokenizationProcess,
                LatinStanzaProcess,
                LatinEmbeddingsProcess,
                StopsProcess,
                # LatinNERProcess,
                LatinLexiconProcess,
            ]
        super().__init__(language, description, processes)


@dataclass
class ChinesePipeline(Pipeline):
    """Default ``Pipeline`` for Classical Chinese.

    >>> from cltk.languages.pipelines import ChinesePipeline
    >>> a_pipeline = ChinesePipeline()
    >>> a_pipeline.description
    'Pipeline for the Classical Chinese language'
    >>> a_pipeline.language
    Language(name='Literary Chinese', glottolog_id='lite1248', latitude=0.0, longitude=0.0, family_id='sino1245', parent_id='clas1255', level='language', iso_639_3_code='lzh', type='h', dates=[])
    >>> a_pipeline.language.name
    'Literary Chinese'
    >>> a_pipeline.processes[0]
    <class 'cltk.dependency.processes.ChineseStanzaProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(
        self, processes=None, description="Pipeline for the Classical Chinese language"
    ):
        language = get_lang("lzh")
        if not processes:
            processes = [ChineseStanzaProcess]
        super().__init__(language, description, processes)


@dataclass
class CopticPipeline(Pipeline):
    """Default ``Pipeline`` for Coptic.

    >>> from cltk.languages.pipelines import CopticPipeline
    >>> a_pipeline = CopticPipeline()
    >>> a_pipeline.description
    'Pipeline for the Coptic language'
    >>> a_pipeline.language
    Language(name='Coptic', glottolog_id='copt1239', latitude=29.472, longitude=31.2053, family_id='afro1255', parent_id='egyp1245', level='language', iso_639_3_code='cop', type='', dates=[])
    >>> a_pipeline.language.name
    'Coptic'
    >>> a_pipeline.processes[0]
    <class 'cltk.dependency.processes.CopticStanzaProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(self, processes=None, description="Pipeline for the Coptic language"):
        language = get_lang("cop")
        if not processes:
            processes = [CopticStanzaProcess, StopsProcess]
        super().__init__(language, description, processes)


@dataclass
class GothicPipeline(Pipeline):
    """Default ``Pipeline`` for Gothic.

    >>> from cltk.languages.pipelines import GothicPipeline
    >>> a_pipeline = GothicPipeline()
    >>> a_pipeline.description
    'Pipeline for the Gothic language'
    >>> a_pipeline.language
    Language(name='Gothic', glottolog_id='goth1244', latitude=46.9304, longitude=29.9786, family_id='indo1319', parent_id='east2805', level='language', iso_639_3_code='got', type='a', dates=[])
    >>> a_pipeline.language.name
    'Gothic'
    >>> a_pipeline.processes[0]
    <class 'cltk.dependency.processes.GothicStanzaProcess'>
    >>> a_pipeline.processes[1]
    <class 'cltk.embeddings.processes.GothicEmbeddingsProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(self, processes=None, description="Pipeline for the Gothic language"):
        language = get_lang("got")
        if not processes:
            processes = [GothicStanzaProcess, GothicEmbeddingsProcess]
        super().__init__(language, description, processes)


@dataclass
class GreekPipeline(Pipeline):
    """Default ``Pipeline`` for Ancient Greek.

    >>> from cltk.languages.pipelines import GreekPipeline
    >>> a_pipeline = GreekPipeline()
    >>> a_pipeline.description
    'Pipeline for the Greek language'
    >>> a_pipeline.language
    Language(name='Ancient Greek', glottolog_id='anci1242', latitude=39.8155, longitude=21.9129, family_id='indo1319', parent_id='east2798', level='language', iso_639_3_code='grc', type='h', dates=[])
    >>> a_pipeline.language.name
    'Ancient Greek'
    >>> a_pipeline.processes[0]
    <class 'cltk.alphabet.processes.GreekNormalizeProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(self, processes=None, description="Pipeline for the Greek language"):
        language = get_lang("grc")
        if not processes:
            processes = [
                # GreekTokenizationProcess,
                GreekNormalizeProcess,
                GreekStanzaProcess,
                GreekEmbeddingsProcess,
                StopsProcess,
                # GreekNERProcess,
            ]
        super().__init__(language, description, processes)


@dataclass
class HindiPipeline(Pipeline):
    """Default ``Pipeline`` for Hindi.

    >>> from cltk.languages.pipelines import HindiPipeline
    >>> a_pipeline = HindiPipeline()
    >>> a_pipeline.description
    'Pipeline for the Hindi language.'
    >>> a_pipeline.language
    Language(name='Hindi', glottolog_id='hind1269', latitude=25.0, longitude=77.0, family_id='indo1319', parent_id='hind1270', level='language', iso_639_3_code='hin', type='', dates=[])
    >>> a_pipeline.language.name
    'Hindi'
    >>> a_pipeline.processes[1]
    <class 'cltk.stops.processes.StopsProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(self, processes=None, description="Pipeline for the Hindi language."):
        language = get_lang("hin")
        if not processes:
            processes = [MultilingualTokenizationProcess, StopsProcess]
        super().__init__(language, description, processes)


@dataclass
class LatinPipeline(Pipeline):
    """Default ``Pipeline`` for Latin.

    TODO: Add stopword annotation for all relevant pipelines.

    >>> from cltk.languages.pipelines import LatinPipeline
    >>> a_pipeline = LatinPipeline()
    >>> a_pipeline.description
    'Pipeline for the Latin language'
    >>> a_pipeline.language
    Language(name='Latin', glottolog_id='lati1261', latitude=41.9026, longitude=12.4502, family_id='indo1319', parent_id='impe1234', level='language', iso_639_3_code='lat', type='a', dates=[])
    >>> a_pipeline.language.name
    'Latin'
    >>> a_pipeline.processes[0]
    <class 'cltk.alphabet.processes.LatinNormalizeProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(self, processes=None, description="Pipeline for the Latin language"):
        language = get_lang("lat")
        if not processes:
            processes = [
                LatinNormalizeProcess,
                # LatinTokenizationProcess,
                LatinStanzaProcess,
                LatinEmbeddingsProcess,
                StopsProcess,
                # LatinNERProcess,
                LatinLexiconProcess,
            ]
        super().__init__(language, description, processes)


@dataclass
class MiddleHighGermanPipeline(Pipeline):
    """Default ``Pipeline`` for Middle High German.

    >>> a_pipeline = MiddleHighGermanPipeline()
    >>> a_pipeline.description
    'Pipeline for the Middle High German language.'
    >>> a_pipeline.language
    Language(name='Middle High German', glottolog_id='midd1343', latitude=0.0, longitude=0.0, family_id='indo1319', parent_id='midd1349', level='language', iso_639_3_code='gmh', type='h', dates=[])
    >>> a_pipeline.language.name
    'Middle High German'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.MiddleHighGermanTokenizationProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(
        self,
        processes=None,
        description="Pipeline for the Middle High German language.",
    ):
        language = get_lang("gmh")
        if not processes:
            processes = [MiddleHighGermanTokenizationProcess, StopsProcess]
        super().__init__(language, description, processes)


@dataclass
class MiddleEnglishPipeline(Pipeline):
    """Default ``Pipeline`` for Middle English.

    TODO: Figure out whether this the dedicated tokenizer is good enough or necessary; we have stanza for Old English, which might be able to tokenizer fine.

    >>> from cltk.languages.pipelines import MiddleEnglishPipeline
    >>> a_pipeline = MiddleEnglishPipeline()
    >>> a_pipeline.description
    'Pipeline for the Middle English language'
    >>> a_pipeline.language
    Language(name='Middle English', glottolog_id='midd1317', latitude=0.0, longitude=0.0, family_id='indo1319', parent_id='merc1242', level='language', iso_639_3_code='enm', type='h', dates=[])
    >>> a_pipeline.language.name
    'Middle English'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.MiddleEnglishTokenizationProcess'>
    >>> from cltk import NLP
    >>> middle_english_nlp = NLP(language="enm", suppress_banner=True)
    >>> from cltk.languages.example_texts import get_example_text
    >>> doc = middle_english_nlp.analyze(get_example_text("enm"))
    >>> doc[2].embedding.shape
    (50,)

    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(
        self, processes=None, description="Pipeline for the Middle English language"
    ):
        language = get_lang("enm")
        if not processes:
            processes = [
                MiddleEnglishTokenizationProcess,
                StopsProcess,
                MiddleEnglishEmbeddingsProcess,
            ]
        super().__init__(language, description, processes)


@dataclass
class MiddleFrenchPipeline(Pipeline):
    """Default ``Pipeline`` for Middle French.

    TODO: Figure out whether this the dedicated tokenizer is good enough or necessary; we have stanza for Old French, which might be able to tokenizer fine.

    >>> from cltk.languages.pipelines import MiddleFrenchPipeline
    >>> a_pipeline = MiddleFrenchPipeline()
    >>> a_pipeline.description
    'Pipeline for the Middle French language'
    >>> a_pipeline.language
    Language(name='Middle French', glottolog_id='midd1316', latitude=0.0, longitude=0.0, family_id='indo1319', parent_id='stan1290', level='dialect', iso_639_3_code='frm', type='h', dates=[])
    >>> a_pipeline.language.name
    'Middle French'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.MiddleFrenchTokenizationProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(
        self, processes=None, description="Pipeline for the Middle French language"
    ):
        language = get_lang("frm")
        if not processes:
            processes = [MiddleFrenchTokenizationProcess]
        super().__init__(language, description, processes)


@dataclass
class OCSPipeline(Pipeline):
    """Default ``Pipeline`` for Old Church Slavonic.

    >>> from cltk.languages.pipelines import OCSPipeline
    >>> a_pipeline = OCSPipeline()
    >>> a_pipeline.description
    'Pipeline for the Old Church Slavonic language'
    >>> a_pipeline.language
    Language(name='Church Slavic', glottolog_id='chur1257', latitude=43.7171, longitude=22.8442, family_id='indo1319', parent_id='east2269', level='language', iso_639_3_code='chu', type='a', dates=[])
    >>> a_pipeline.language.name
    'Church Slavic'
    >>> a_pipeline.processes[0]
    <class 'cltk.dependency.processes.OCSStanzaProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(
        self,
        processes=None,
        description="Pipeline for the Old Church Slavonic language",
    ):
        language = get_lang("chu")
        if not processes:
            processes = [OCSStanzaProcess]
        super().__init__(language, description, processes)


@dataclass
class OldEnglishPipeline(Pipeline):
    """Default ``Pipeline`` for Old English.

    >>> from cltk.languages.pipelines import OldEnglishPipeline
    >>> a_pipeline = OldEnglishPipeline()
    >>> a_pipeline.description
    'Pipeline for the Old English language'
    >>> a_pipeline.language
    Language(name='Old English (ca. 450-1100)', glottolog_id='olde1238', latitude=51.06, longitude=-1.31, family_id='indo1319', parent_id='angl1265', level='language', iso_639_3_code='ang', type='h', dates=[])
    >>> a_pipeline.language.name
    'Old English (ca. 450-1100)'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.MultilingualTokenizationProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(
        self, processes=None, description="Pipeline for the Old English language"
    ):
        language = get_lang("ang")
        if not processes:
            processes = [
                MultilingualTokenizationProcess,
                OldEnglishLemmatizationProcess,
                OldEnglishEmbeddingsProcess,
                StopsProcess,
                # OldEnglishNERProcess,
            ]
        super().__init__(language, description, processes)


@dataclass
class OldFrenchPipeline(Pipeline):
    """Default ``Pipeline`` for Old French.

    >>> from cltk.languages.pipelines import OldFrenchPipeline
    >>> a_pipeline = OldFrenchPipeline()
    >>> a_pipeline.description
    'Pipeline for the Old French language'
    >>> a_pipeline.language
    Language(name='Old French (842-ca. 1400)', glottolog_id='oldf1239', latitude=0.0, longitude=0.0, family_id='indo1319', parent_id='oila1234', level='language', iso_639_3_code='fro', type='h', dates=[])
    >>> a_pipeline.language.name
    'Old French (842-ca. 1400)'
    >>> a_pipeline.processes[0]
    <class 'cltk.dependency.processes.OldFrenchStanzaProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(
        self, processes=None, description="Pipeline for the Old French language"
    ):
        language = get_lang("fro")
        if not processes:
            processes = [
                # OldFrenchTokenizationProcess,
                OldFrenchStanzaProcess,
                StopsProcess,
                OldFrenchNERProcess,
            ]
        super().__init__(language, description, processes)


# TODO: Add Old Marathi ("omr")


@dataclass
class OldNorsePipeline(Pipeline):
    """Default ``Pipeline`` for Old Norse.

    >>> from cltk.languages.pipelines import OldNorsePipeline
    >>> a_pipeline = OldNorsePipeline()
    >>> a_pipeline.description
    'Pipeline for the Old Norse language'
    >>> a_pipeline.language
    Language(name='Old Norse', glottolog_id='oldn1244', latitude=63.42, longitude=10.38, family_id='indo1319', parent_id='west2805', level='language', iso_639_3_code='non', type='h', dates=[])
    >>> a_pipeline.language.name
    'Old Norse'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.OldNorseTokenizationProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(
        self, processes=None, description="Pipeline for the Old Norse language"
    ):
        language = get_lang("non")
        if not processes:
            processes = [
                OldNorseTokenizationProcess,
                StopsProcess,
                OldNorseLexiconProcess,
            ]
        super().__init__(language, description, processes)


@dataclass
class PaliPipeline(Pipeline):
    """Default ``Pipeline`` for Pali.

    TODO: Make better tokenizer for Pali.

    >>> from cltk.languages.pipelines import PaliPipeline
    >>> a_pipeline = PaliPipeline()
    >>> a_pipeline.description
    'Pipeline for the Pali language'
    >>> a_pipeline.language
    Language(name='Pali', glottolog_id='pali1273', latitude=24.5271, longitude=82.251, family_id='indo1319', parent_id='biha1245', level='language', iso_639_3_code='pli', type='a', dates=[])
    >>> a_pipeline.language.name
    'Pali'
    >>> a_pipeline.processes[0]
    <class 'cltk.tokenizers.processes.MultilingualTokenizationProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(self, processes=None, description="Pipeline for the Pali language"):
        language = get_lang("pli")
        if not processes:
            processes = [MultilingualTokenizationProcess, PaliEmbeddingsProcess]
        super().__init__(language, description, processes)


@dataclass
class PanjabiPipeline(Pipeline):
    """Default ``Pipeline`` for Panjabi.

    >>> from cltk.languages.pipelines import SanskritPipeline
    >>> a_pipeline = PanjabiPipeline()
    >>> a_pipeline.description
    'Pipeline for the Panjabi language.'
    >>> a_pipeline.language
    Language(name='Eastern Panjabi', glottolog_id='panj125', latitude=30.0368, longitude=75.6702, family_id='indo1319', parent_id='east2727', level='language', iso_639_3_code='pan', type='', dates=[])
    >>> a_pipeline.language.name
    'Eastern Panjabi'
    >>> a_pipeline.processes[1]
    <class 'cltk.stops.processes.StopsProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(
        self, processes=None, description="Pipeline for the Panjabi language."
    ):
        language = get_lang("pan")
        if not processes:
            processes = [MultilingualTokenizationProcess, StopsProcess]
        super().__init__(language, description, processes)


@dataclass
class SanskritPipeline(Pipeline):
    """Default ``Pipeline`` for Sanskrit.

    TODO: Make better tokenizer for Sanskrit.

    >>> from cltk.languages.pipelines import SanskritPipeline
    >>> a_pipeline = SanskritPipeline()
    >>> a_pipeline.description
    'Pipeline for the Sanskrit language.'
    >>> a_pipeline.language
    Language(name='Sanskrit', glottolog_id='sans1269', latitude=20.0, longitude=77.0, family_id='indo1319', parent_id='indo1321', level='language', iso_639_3_code='san', type='a', dates=[])
    >>> a_pipeline.language.name
    'Sanskrit'
    >>> a_pipeline.processes[1]
    <class 'cltk.embeddings.processes.SanskritEmbeddingsProcess'>
    """

    description: str
    language: Language
    processes: List[Type[Process]]

    def __init__(
        self, processes=None, description="Pipeline for the Sanskrit language."
    ):
        language = get_lang("sab")
        if not processes:
            processes = [
                MultilingualTokenizationProcess,
                SanskritEmbeddingsProcess,
                StopsProcess,
            ]
        super().__init__(language, description, processes)
