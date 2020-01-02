"""Default processing pipelines for languages. The purpose of
these dataclasses is to represent:

1. the types of NLP processs that the CLTK can do
2. the order in which processs are to be executed
3. specifying what downstream features a particular implemented process requires
"""

from dataclasses import dataclass, field
from typing import Callable, List, Type

from cltkv1.languages import get_lang
from cltkv1.tokenizers import DefaultTokenizationProcess, LatinTokenizationProcess
from cltkv1.utils.data_types import Language, Pipeline, Process
from cltkv1.wrappers import StanfordNLPProcess


@dataclass
class LatinPipeline(Pipeline):
    """Default ``Pipeline`` for Latin.

    >>> from cltkv1.utils.pipelines import LatinPipeline
    >>> a_pipeline = LatinPipeline()
    >>> a_pipeline.description
    'Pipeline for the Latin language'
    >>> a_pipeline.language
    Language(name='Latin', glottolog_id='lati1261', latitude=41.9026, longitude=12.4502, dates=[], family_id='indo1319', parent_id='impe1234', level='language', iso_639_3_code='lat', type='a')
    >>> a_pipeline.language.name
    'Latin'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.wrappers.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Latin language"
    language: Language = get_lang("lat")
    processes: List[Type[Process]] = field(default_factory=lambda: [StanfordNLPProcess])


@dataclass
class GreekPipeline(Pipeline):
    """Default ``Pipeline`` for Ancient Greek.

    >>> from cltkv1.utils.pipelines import GreekPipeline
    >>> a_pipeline = GreekPipeline()
    >>> a_pipeline.description
    'Pipeline for the Greek language'
    >>> a_pipeline.language
    Language(name='Ancient Greek', glottolog_id='anci1242', latitude=39.8155, longitude=21.9129, dates=[], family_id='indo1319', parent_id='east2798', level='language', iso_639_3_code='grc', type='h')
    >>> a_pipeline.language.name
    'Ancient Greek'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.wrappers.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Greek language"
    language: Language = get_lang("grc")
    processes: List[Type[Process]] = field(default_factory=lambda: [StanfordNLPProcess])


@dataclass
class OCSPipeline(Pipeline):
    """Default ``Pipeline`` for Old Church Slavonic.

    >>> from cltkv1.utils.pipelines import OCSPipeline
    >>> a_pipeline = OCSPipeline()
    >>> a_pipeline.description
    'Pipeline for the Old Church Slavonic language'
    >>> a_pipeline.language
    Language(name='Church Slavic', glottolog_id='chur1257', latitude=43.7171, longitude=22.8442, dates=[], family_id='indo1319', parent_id='east2269', level='language', iso_639_3_code='chu', type='a')
    >>> a_pipeline.language.name
    'Church Slavic'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.wrappers.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Old Church Slavonic language"
    language: Language = get_lang("chu")
    processes: List[Type[Process]] = field(default_factory=lambda: [StanfordNLPProcess])


@dataclass
class OldFrenchPipeline(Pipeline):
    """Default ``Pipeline`` for Old French.

    >>> from cltkv1.utils.pipelines import OldFrenchPipeline
    >>> a_pipeline = OldFrenchPipeline()
    >>> a_pipeline.description
    'Pipeline for the Old French language'
    >>> a_pipeline.language
    Language(name='Old French (842-ca. 1400)', glottolog_id='oldf1239', latitude=0.0, longitude=0.0, dates=[], family_id='indo1319', parent_id='oila1234', level='language', iso_639_3_code='fro', type='h')
    >>> a_pipeline.language.name
    'Old French (842-ca. 1400)'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.wrappers.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Old French language"
    language: Language = get_lang("fro")
    processes: List[Type[Process]] = field(default_factory=lambda: [StanfordNLPProcess])


@dataclass
class GothicPipeline(Pipeline):
    """Default ``Pipeline`` for Gothic.

    >>> from cltkv1.utils.pipelines import GothicPipeline
    >>> a_pipeline = GothicPipeline()
    >>> a_pipeline.description
    'Pipeline for the Gothic language'
    >>> a_pipeline.language
    Language(name='Gothic', glottolog_id='goth1244', latitude=46.9304, longitude=29.9786, dates=[], family_id='indo1319', parent_id='east2805', level='language', iso_639_3_code='got', type='a')
    >>> a_pipeline.language.name
    'Gothic'
    >>> a_pipeline.processes[0]
    <class 'cltkv1.wrappers.StanfordNLPProcess'>
    """

    description: str = "Pipeline for the Gothic language"
    language: Language = get_lang("got")
    processes: List[Type[Process]] = field(default_factory=lambda: [StanfordNLPProcess])
