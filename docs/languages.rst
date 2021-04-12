Languages
=========


The :class:`cltk.nlp.NLP()` class accepts a :class:`cltk.core.data_types.Pipeline()` object. \
Module :mod:`cltk.languages.pipelines` contains all pre-configured pipelines.

.. contents::
   :depth: 2

Akkadian
--------
- :class:`cltk.languages.pipelines.AkkadianPipeline()`
- ISO Code: ``"akk"``

.. code-block:: python

   >>> from cltk.languages.pipelines import AkkadianPipeline
   >>> a_pipeline = AkkadianPipeline()
   >>> a_pipeline.description
   'Pipeline for the Akkadian language.'
   >>> a_pipeline.language
   Language(name='Akkadian', glottolog_id='akka1240', latitude=33.1, longitude=44.1, dates=[], family_id='afro1255', parent_id='east2678', level='language', iso_639_3_code='akk', type='a')
   >>> a_pipeline.language.name
   'Akkadian'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.AkkadianTokenizationProcess'>, <class 'cltk.stops.processes.StopsProcess'>]


Arabic
------
- :class:`cltk.languages.pipelines.ArabicPipeline()`
- ISO Code: ``"arb"``

.. code-block:: python

   >>> from cltk.languages.pipelines import ArabicPipeline
   >>> a_pipeline = ArabicPipeline()
   >>> a_pipeline.description
   'Pipeline for the Arabic language'
   >>> a_pipeline.language
   Language(name='Standard Arabic', glottolog_id='stan1318', latitude=27.9625, longitude=43.8525, dates=[], family_id='afro1255', parent_id='arab1395', level='language', iso_639_3_code='arb', type='')
   >>> a_pipeline.language.name
   'Standard Arabic'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.ArabicTokenizationProcess'>, <class 'cltk.embeddings.processes.ArabicEmbeddingsProcess'>, <class 'cltk.stops.processes.StopsProcess'>]


Aramaic
-------
- :class:`cltk.languages.pipelines.AramaicPipeline()`
- ISO Code: ``"arc"``

.. code-block:: python

   >>> from cltk.languages.pipelines import AramaicPipeline
   >>> a_pipeline = AramaicPipeline()
   >>> a_pipeline.description
   'Pipeline for the Aramaic language'
   >>> a_pipeline.language
   Language(name='Official Aramaic (700-300 BCE)', glottolog_id='', latitude=0.0, longitude=0.0, dates=[], family_id='', parent_id='', level='', iso_639_3_code='arc', type='a')
   >>> a_pipeline.language.name
   'Official Aramaic (700-300 BCE)'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.ArabicTokenizationProcess'>, <class 'cltk.embeddings.processes.AramaicEmbeddingsProcess'>]


Classical Chinese
-----------------
- :class:`cltk.languages.pipelines.ChinesePipeline()`
- ISO Code: ``"lzh"``

.. code-block:: python

   >>> from cltk.languages.pipelines import ChinesePipeline
   >>> a_pipeline = ChinesePipeline()
   >>> a_pipeline.description
   'Pipeline for the Classical Chinese language'
   >>> a_pipeline.language
   Language(name='Literary Chinese', glottolog_id='lite1248', latitude=0.0, longitude=0.0, dates=[], family_id='sino1245', parent_id='clas1255', level='language', iso_639_3_code='lzh', type='h')
   >>> a_pipeline.language.name
   'Literary Chinese'
   >>> a_pipeline.processes
   [<class 'cltk.dependency.processes.ChineseStanzaProcess'>]


Coptic
------
- :class:`cltk.languages.pipelines.CopticPipeline()`
- ISO Code: ``"cop"``

.. code-block:: python

   >>> from cltk.languages.pipelines import CopticPipeline
   >>> a_pipeline = CopticPipeline()
   >>> a_pipeline.description
   'Pipeline for the Coptic language'
   >>> a_pipeline.language
   Language(name='Coptic', glottolog_id='copt1239', latitude=29.472, longitude=31.2053, dates=[], family_id='afro1255', parent_id='egyp1245', level='language', iso_639_3_code='cop', type='')
   >>> a_pipeline.language.name
   'Coptic'
   >>> a_pipeline.processes
   [<class 'cltk.dependency.processes.CopticStanzaProcess'>, <class 'cltk.stops.processes.StopsProcess'>]


Gothic
------
- :class:`cltk.languages.pipelines.GothicPipeline()`
- ISO Code: ``"got"``

.. code-block:: python

   >>> from cltk.languages.pipelines import GothicPipeline
   >>> a_pipeline = GothicPipeline()
   >>> a_pipeline.description
   'Pipeline for the Gothic language'
   >>> a_pipeline.language
   Language(name='Gothic', glottolog_id='goth1244', latitude=46.9304, longitude=29.9786, dates=[], family_id='indo1319', parent_id='east2805', level='language', iso_639_3_code='got', type='a')
   >>> a_pipeline.language.name
   'Gothic'
   >>> a_pipeline.processes
   [<class 'cltk.dependency.processes.GothicStanzaProcess'>, <class 'cltk.embeddings.processes.GothicEmbeddingsProcess'>]



Greek
-----
- :class:`cltk.languages.pipelines.GreekPipeline()`
- ISO Code: ``"grc"``

.. code-block:: python

   >>> from cltk.languages.pipelines import GreekPipeline
   >>> a_pipeline = GreekPipeline()
   >>> a_pipeline.description
   'Pipeline for the Greek language'
   >>> a_pipeline.language
   Language(name='Ancient Greek', glottolog_id='anci1242', latitude=39.8155, longitude=21.9129, dates=[], family_id='indo1319', parent_id='east2798', level='language', iso_639_3_code='grc', type='h')
   >>> a_pipeline.language.name
   'Ancient Greek'
   >>> a_pipeline.processes
   [<class 'cltk.alphabet.processes.GreekNormalizeProcess'>, <class 'cltk.dependency.processes.GreekStanzaProcess'>, <class 'cltk.embeddings.processes.GreekEmbeddingsProcess'>, <class 'cltk.stops.processes.StopsProcess'>, <class 'cltk.ner.processes.GreekNERProcess'>]


Hindi
-----
- :class:`cltk.languages.pipelines.HindiPipeline()`
- ISO Code: ``"hin"``

.. code-block:: python

   >>> from cltk.languages.pipelines import HindiPipeline
   >>> a_pipeline = HindiPipeline()
   >>> a_pipeline.description
   'Pipeline for the Hindi language.'
   >>> a_pipeline.language
   Language(name='Hindi', glottolog_id='hind1269', latitude=25.0, longitude=77.0, dates=[], family_id='indo1319', parent_id='hind1270', level='language', iso_639_3_code='hin', type='')
   >>> a_pipeline.language.name
   'Hindi'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.MultilingualTokenizationProcess'>, <class 'cltk.stops.processes.StopsProcess'>]



Latin
-----
- :class:`cltk.languages.pipelines.LatinPipeline()`
- ISO Code: ``"lat"``

.. code-block:: python

   >>> from cltk.languages.pipelines import LatinPipeline
   >>> a_pipeline = LatinPipeline()
   >>> a_pipeline.description
   'Pipeline for the Latin language'
   >>> a_pipeline.language
   Language(name='Latin', glottolog_id='lati1261', latitude=41.9026, longitude=12.4502, dates=[], family_id='indo1319', parent_id='impe1234', level='language', iso_639_3_code='lat', type='a')
   >>> a_pipeline.language.name
   'Latin'
   >>> a_pipeline.processes
   [<class 'cltk.alphabet.processes.LatinNormalizeProcess'>, <class 'cltk.dependency.processes.LatinStanzaProcess'>, <class 'cltk.embeddings.processes.LatinEmbeddingsProcess'>, <class 'cltk.stops.processes.StopsProcess'>, <class 'cltk.ner.processes.LatinNERProcess'>, <class 'cltk.lexicon.processes.LatinLexiconProcess'>]



Middle High German
------------------
- :class:`cltk.languages.pipelines.MHGPipeline()`
- ISO Code: ``"gmh"``

.. code-block:: python

   >>> from cltk.languages.pipelines import MiddleHighGermanPipeline
   >>> a_pipeline = MiddleHighGermanPipeline()
   >>> a_pipeline.description
   'Pipeline for the Middle High German language.'
   >>> a_pipeline.language
   Language(name='Middle High German', glottolog_id='midd1343', latitude=0.0, longitude=0.0, dates=[], family_id='indo1319', parent_id='midd1349', level='language', iso_639_3_code='gmh', type='h')
   >>> a_pipeline.language.name
   'Middle High German'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.MiddleHighGermanTokenizationProcess'>, <class 'cltk.stops.processes.StopsProcess'>]


English
-------
Old English
***********
- :class:`cltk.languages.pipelines.OldEnglishPipeline()`
- ISO Code: ``"ang"``

.. code-block:: python

   >>> from cltk.languages.pipelines import OldEnglishPipeline
   >>> a_pipeline = OldEnglishPipeline()
   >>> a_pipeline.description
   'Pipeline for the Old English language'
   >>> a_pipeline.language
   Language(name='Old English (ca. 450-1100)', glottolog_id='olde1238', latitude=51.06, longitude=-1.31, dates=[], family_id='indo1319', parent_id='angl1265', level='language', iso_639_3_code='ang', type='h')
   >>> a_pipeline.language.name
   'Old English (ca. 450-1100)'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.MultilingualTokenizationProcess'>, <class 'cltk.lemmatize.processes.OldEnglishLemmatizationProcess'>, <class 'cltk.embeddings.processes.OldEnglishEmbeddingsProcess'>, <class 'cltk.stops.processes.StopsProcess'>, <class 'cltk.ner.processes.OldEnglishNERProcess'>]


Middle English
**************
- :class:`cltk.languages.pipelines.MiddleEnglishPipeline()`
- ISO Code: ``"enm"``

.. code-block:: python

   >>> from cltk.languages.pipelines import MiddleEnglishPipeline
   >>> a_pipeline = MiddleEnglishPipeline()
   >>> a_pipeline.description
   'Pipeline for the Middle English language'
   >>> a_pipeline.language
   Language(name='Middle English', glottolog_id='midd1317', latitude=0.0, longitude=0.0, dates=[], family_id='indo1319', parent_id='merc1242', level='language', iso_639_3_code='enm', type='h')
   >>> a_pipeline.language.name
   'Middle English'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.MiddleEnglishTokenizationProcess'>, <class 'cltk.stops.processes.StopsProcess'>]


French
------
Old French
**********
- :class:`cltk.languages.pipelines.OldFrenchPipeline()`
- ISO Code: ``"fro"``

.. code-block:: python

   >>> from cltk.languages.pipelines import OldFrenchPipeline
   >>> a_pipeline = OldFrenchPipeline()
   >>> a_pipeline.description
   'Pipeline for the Old French language'
   >>> a_pipeline.language
   Language(name='Old French (842-ca. 1400)', glottolog_id='oldf1239', latitude=0.0, longitude=0.0, dates=[], family_id='indo1319', parent_id='oila1234', level='language', iso_639_3_code='fro', type='h')
   >>> a_pipeline.language.name
   'Old French (842-ca. 1400)'
   >>> a_pipeline.processes
   [<class 'cltk.dependency.processes.OldFrenchStanzaProcess'>, <class 'cltk.stops.processes.StopsProcess'>, <class 'cltk.ner.processes.OldFrenchNERProcess'>]


Middle French
*************
- :class:`cltk.languages.pipelines.MiddleFrenchPipeline()`
- ISO Code: ``"frm"``

.. code-block:: python

   >>> from cltk.languages.pipelines import MiddleFrenchPipeline
   >>> a_pipeline = MiddleFrenchPipeline()
   >>> a_pipeline.description
   'Pipeline for the Middle French language'
   >>> a_pipeline.language
   Language(name='Middle French', glottolog_id='midd1316', latitude=0.0, longitude=0.0, dates=[], family_id='indo1319', parent_id='stan1290', level='dialect', iso_639_3_code='frm', type='h')
   >>> a_pipeline.language.name
   'Middle French'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.MiddleFrenchTokenizationProcess'>]



Old Church Slavonic
-------------------
- :class:`cltk.languages.pipelines.OCSPipeline()`
- ISO Code: ``"chu"``

.. code-block:: python

   >>> from cltk.languages.pipelines import OCSPipeline
   >>> a_pipeline = OCSPipeline()
   >>> a_pipeline.description
   'Pipeline for the Old Church Slavonic language'
   >>> a_pipeline.language
   Language(name='Church Slavic', glottolog_id='chur1257', latitude=43.7171, longitude=22.8442, dates=[], family_id='indo1319', parent_id='east2269', level='language', iso_639_3_code='chu', type='a')
   >>> a_pipeline.language.name
   'Church Slavic'
   >>> a_pipeline.processes
   [<class 'cltk.dependency.processes.OCSStanzaProcess'>]


Old Norse
---------
- :class:`cltk.languages.pipelines.OldNorsePipeline()`
- ISO Code: ``"non"``

.. code-block:: python

   >>> from cltk.languages.pipelines import OldNorsePipeline
   >>> a_pipeline = OldNorsePipeline()
   >>> a_pipeline.description
   'Pipeline for the Old Norse language'
   >>> a_pipeline.language
   Language(name='Old Norse', glottolog_id='oldn1244', latitude=63.42, longitude=10.38, dates=[], family_id='indo1319', parent_id='west2805', level='language', iso_639_3_code='non', type='h')
   >>> a_pipeline.language.name
   'Old Norse'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.OldNorseTokenizationProcess'>, <class 'cltk.stops.processes.StopsProcess'>, <class 'cltk.lexicon.processes.OldNorseLexiconProcess'>]


Pali
----
- :class:`cltk.languages.pipelines.PaliPipeline()`
- ISO Code: ``"pli"``

.. code-block:: python

   >>> from cltk.languages.pipelines import PaliPipeline
   >>> a_pipeline = PaliPipeline()
   >>> a_pipeline.description
   'Pipeline for the Pali language'
   >>> a_pipeline.language
   Language(name='Pali', glottolog_id='pali1273', latitude=24.5271, longitude=82.251, dates=[], family_id='indo1319', parent_id='biha1245', level='language', iso_639_3_code='pli', type='a')
   >>> a_pipeline.language.name
   'Pali'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.MultilingualTokenizationProcess'>, <class 'cltk.embeddings.processes.PaliEmbeddingsProcess'>]


Panjabi
-------
- :class:`cltk.languages.pipelines.PanjabiPipeline()`
- ISO Code: ``"pan"``

.. code-block:: python

   >>> from cltk.languages.pipelines import PanjabiPipeline
   >>> a_pipeline = PanjabiPipeline()
   >>> a_pipeline.description
   'Pipeline for the Panjabi language.'
   >>> a_pipeline.language
   Language(name='Eastern Panjabi', glottolog_id='panj125', latitude=30.0368, longitude=75.6702, dates=[], family_id='indo1319', parent_id='east2727', level='language', iso_639_3_code='pan', type='')
   >>> a_pipeline.language.name
   'Eastern Panjabi'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.MultilingualTokenizationProcess'>, <class 'cltk.stops.processes.StopsProcess'>]


Sanskrit
--------
- :class:`cltk.languages.pipelines.SanskritPipeline()`
- ISO Code: ``"san"``

.. code-block:: python

   >>> from cltk.languages.pipelines import SanskritPipeline
   >>> a_pipeline = SanskritPipeline()
   >>> a_pipeline.description
   'Pipeline for the Sanskrit language.'
   >>> a_pipeline.language
   Language(name='Sanskrit', glottolog_id='sans1269', latitude=20.0, longitude=77.0, dates=[], family_id='indo1319', parent_id='indo1321', level='language', iso_639_3_code='san', type='a')
   >>> a_pipeline.language.name
   'Sanskrit'
   >>> a_pipeline.processes
   [<class 'cltk.tokenizers.processes.MultilingualTokenizationProcess'>, <class 'cltk.embeddings.processes.SanskritEmbeddingsProcess'>, <class 'cltk.stops.processes.StopsProcess'>]

