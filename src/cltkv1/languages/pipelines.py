"""Default processing pipelines for languages. The purpose of
these dataclasses is to represent:

1. the types of NLP processs that the CLTK can do
2. the order in which processs are to be executed
3. specifying what downstream features a particular implemented process requires
"""

from dataclasses import dataclass, field
from typing import List, Type

from cltkv1.core.data_types import Language, Pipeline, Process
from cltkv1.dependency.stanford import StanfordNLPProcess
from cltkv1.embeddings.processes import (
    ArabicEmbeddingsProcess,
    AramaicEmbeddingsProcess,
    GothicEmbeddingsProcess,
    LatinEmbeddingsProcess,
    PaliEmbeddingsProcess,
    SanskritEmbeddingsProcess,
)
from cltkv1.languages.utils import get_lang
from cltkv1.tokenizers.processes import (
    ArabicTokenizationProcess,
    DefaultTokenizationProcess,
    SanskritTokenizationProcess,
)


@dataclass
class ArabicPipeline(Pipeline):
    """Default ``Pipeline`` for Arabic.

    >>> from cltkv1.languages.pipelines import ArabicPipeline
    >>> a_pipeline = ArabicPipeline()
    >>> a_pipeline.description
    'Pipeline for the Arabic language'
    >>> a_pipeline.language
    Language(name='Standard Arabic', glottolog_id='stan1318', latitude=27.9625, longitude=43.8525, dates=[], family_id='afro1255', parent_id='arab1395', level='language', iso_639_3_code='arb', type='')
    >>> a_pipeline.language.name
    'Standard Arabic'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.tokenizers.processes.ArabicTokenizationProcess'>
    """

    description: str = "Pipeline for the Arabic language"
    language: Language = get_lang("arb")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [ArabicTokenizationProcess, ArabicEmbeddingsProcess]
    )


@dataclass
class AramaicPipeline(Pipeline):
    """Default ``Pipeline`` for Aramaic.

    TODO: Confirm with specialist what encodings should be expected.
    TODO: Replace ``ArabicTokenizationProcess`` with a multilingual one or a specific Aramaic.

    >>> from cltkv1.languages.pipelines import AramaicPipeline
    >>> a_pipeline = AramaicPipeline()
    >>> a_pipeline.description
    'Pipeline for the Aramaic language'
    >>> a_pipeline.language
    Language(name='Official Aramaic (700-300 BCE)', glottolog_id='', latitude=0.0, longitude=0.0, dates=[], family_id='', parent_id='', level='', iso_639_3_code='arc', type='a')
    >>> a_pipeline.language.name
    'Official Aramaic (700-300 BCE)'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.tokenizers.processes.ArabicTokenizationProcess'>
    """

    description: str = "Pipeline for the Aramaic language"
    language: Language = get_lang("arc")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [ArabicTokenizationProcess, AramaicEmbeddingsProcess]
    )


@dataclass
class GothicPipeline(Pipeline):
    """Default ``Pipeline`` for Gothic.

    >>> from cltkv1.languages.pipelines import GothicPipeline
    >>> a_pipeline = GothicPipeline()
    >>> a_pipeline.description
    'Pipeline for the Gothic language'
    >>> a_pipeline.language
    Language(name='Gothic', glottolog_id='goth1244', latitude=46.9304, longitude=29.9786, dates=[], family_id='indo1319', parent_id='east2805', level='language', iso_639_3_code='got', type='a')
    >>> a_pipeline.language.name
    'Gothic'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.dependency.stanford.StanfordNLPProcess'>
    >>> a_pipeline.processes[1]
    <class 'cltkv1.embeddings.processes.GothicEmbeddingsProcess'>
    """

    description: str = "Pipeline for the Gothic language"
    language: Language = get_lang("got")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [StanfordNLPProcess, GothicEmbeddingsProcess]
    )


@dataclass
class GreekPipeline(Pipeline):
    """Default ``Pipeline`` for Ancient Greek.

    >>> from cltkv1.languages.pipelines import GreekPipeline
    >>> a_pipeline = GreekPipeline()
    >>> a_pipeline.description
    'Pipeline for the Greek language'
    >>> a_pipeline.language
    Language(name='Ancient Greek', glottolog_id='anci1242', latitude=39.8155, longitude=21.9129, dates=[], family_id='indo1319', parent_id='east2798', level='language', iso_639_3_code='grc', type='h')
    >>> a_pipeline.language.name
    'Ancient Greek'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.dependency.stanford.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Greek language"
    language: Language = get_lang("grc")
    processes: List[Type[Process]] = field(default_factory=lambda: [StanfordNLPProcess])


@dataclass
class LatinPipeline(Pipeline):
    """Default ``Pipeline`` for Latin.

    >>> from cltkv1.languages.pipelines import LatinPipeline
    >>> a_pipeline = LatinPipeline()
    >>> a_pipeline.description
    'Pipeline for the Latin language'
    >>> a_pipeline.language
    Language(name='Latin', glottolog_id='lati1261', latitude=41.9026, longitude=12.4502, dates=[], family_id='indo1319', parent_id='impe1234', level='language', iso_639_3_code='lat', type='a')
    >>> a_pipeline.language.name
    'Latin'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.dependency.stanford.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Latin language"
    language: Language = get_lang("lat")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [StanfordNLPProcess, LatinEmbeddingsProcess]
    )


@dataclass
class OldFrenchPipeline(Pipeline):
    """Default ``Pipeline`` for Old French.

    >>> from cltkv1.languages.pipelines import OldFrenchPipeline
    >>> a_pipeline = OldFrenchPipeline()
    >>> a_pipeline.description
    'Pipeline for the Old French language'
    >>> a_pipeline.language
    Language(name='Old French (842-ca. 1400)', glottolog_id='oldf1239', latitude=0.0, longitude=0.0, dates=[], family_id='indo1319', parent_id='oila1234', level='language', iso_639_3_code='fro', type='h')
    >>> a_pipeline.language.name
    'Old French (842-ca. 1400)'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.dependency.stanford.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Old French language"
    language: Language = get_lang("fro")
    processes: List[Type[Process]] = field(default_factory=lambda: [StanfordNLPProcess])


@dataclass
class OCSPipeline(Pipeline):
    """Default ``Pipeline`` for Old Church Slavonic.

    >>> from cltkv1.languages.pipelines import OCSPipeline
    >>> a_pipeline = OCSPipeline()
    >>> a_pipeline.description
    'Pipeline for the Old Church Slavonic language'
    >>> a_pipeline.language
    Language(name='Church Slavic', glottolog_id='chur1257', latitude=43.7171, longitude=22.8442, dates=[], family_id='indo1319', parent_id='east2269', level='language', iso_639_3_code='chu', type='a')
    >>> a_pipeline.language.name
    'Church Slavic'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.dependency.stanford.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Old Church Slavonic language"
    language: Language = get_lang("chu")
    processes: List[Type[Process]] = field(default_factory=lambda: [StanfordNLPProcess])


@dataclass
class PaliPipeline(Pipeline):
    """Default ``Pipeline`` for Pali.

    TODO: Make better tokenizer for Pali.

    >>> from cltkv1.languages.pipelines import PaliPipeline
    >>> a_pipeline = PaliPipeline()
    >>> a_pipeline.description
    'Pipeline for the Pali language'
    >>> a_pipeline.language
    Language(name='Pali', glottolog_id='pali1273', latitude=24.5271, longitude=82.251, dates=[], family_id='indo1319', parent_id='biha1245', level='language', iso_639_3_code='pli', type='a')
    >>> a_pipeline.language.name
    'Pali'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.dependency.stanford.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Pali language"
    language: Language = get_lang("pli")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [DefaultTokenizationProcess, PaliEmbeddingsProcess]
    )


@dataclass
class SanskritPipeline(Pipeline):
    """Default ``Pipeline`` for Sanskrit.

    TODO: Make better tokenizer for Sanskrit.

    >>> from cltkv1.languages.pipelines import SanskritPipeline
    >>> a_pipeline = SanskritPipeline()
    >>> a_pipeline.description
    'Pipeline for the Sanskrit language'
    >>> a_pipeline.language
    XXX
    >>> a_pipeline.language.name
    'Sanskrit'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.dependency.stanford.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Sanskrit language"
    language: Language = get_lang("san")
    processes: List[Type[Process]] = field(
        default_factory=lambda: [SanskritTokenizationProcess, SanskritEmbeddingsProcess]
    )
