Old Norse
*********

Old Norse was a North Germanic language that was spoken by inhabitants of Scandinavia and inhabitants of their overseas settlements during about the 9th to 13th centuries. The Proto-Norse language developed into Old Norse by the 8th century, and Old Norse began to develop into the modern North Germanic languages in the mid- to late-14th century, ending the language phase known as Old Norse. These dates, however, are not absolute, since written Old Norse is found well into the 15th century. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Old_Norse>`_)


Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``old_norse_``) to discover available Old_norse corpora.

.. code-block:: python

   >>> from cltk.corpus.utils.importer import CorpusImporter

   >>> corpus_importer = CorpusImporter("old_norse")

   >>> corpus_importer.list_corpora
   ['old_norse_text_perseus', 'old_norse_models_cltk']


Stopword Filtering
==================

To use the CLTK's built-in stopwords list, We use an example from `Eiríks saga rauða
<http://www.heimskringla.no/wiki/Eir%C3%ADks_saga_rau%C3%B0a>`_:
.. code-block:: python

   >>> from nltk.tokenize.punkt import PunktLanguageVars

   >>> from cltk.stop.old_norse.stops import STOPS_LIST

   >>> sentence = 'Þat var einn morgin, er þeir Karlsefni sá fyrir ofan rjóðrit flekk nökkurn, sem glitraði við þeim'

   >>> p = PunktLanguageVars()

   >>> tokens = p.word_tokenize(sentence.lower())

   >>> [w for w in tokens if not w in STOPS_LIST]
   ['var',
    'einn',
    'morgin',
    ',',
    'karlsefni',
    'rjóðrit',
    'flekk',
    'nökkurn',
    ',',
    'glitraði']


Swadesh
=======
The corpus module has a class for generating a Swadesh list for Old Norse.

.. code-block:: python

   In [1]: from cltk.corpus.swadesh import Swadesh

   In [2]: swadesh = Swadesh('old_norse')

   In [3]: swadesh.words()[:10]
   Out[3]: ['ek', 'þú', 'hann', 'vér', 'þér', 'þeir', 'sjá, þessi', 'sá', 'hér', 'þar']


Word Tokenizing
===============
A very simple tokenizer is available for Old Norse. For now, it does not take into account specific Old Norse constructions like the merge of conjugated verbs with þú and with sik.
Here is a sentence extracted from Gylfaginning.
.. code-block:: python

   >>> word_tokenizer = WordTokenizer('old_norse')
   >>> sentence = "Gylfi konungr var maðr vitr ok fjölkunnigr."
   >>> result = word_tokenizer.tokenize(sentence)
   >>> result
   ['Gylfi', 'konungr', 'var', 'maðr', 'vitr', 'ok', 'fjölkunnigr', '.']


POS tagging
===========

You can get the POS tags of Old Norse texts using the CLTK's wrapper around the NLTK tokenizer. First, download the model by importing the ``old_norse_models_cltk`` corpus. This TnT tagger was trained from annotated data from `Icelandic Parsed Historical Corpus <http://www.linguist.is/icelandic_treebank/Download>`_ (version 0.9, license: LGPL).

TnT tagger
``````````

The following sentence is from the first verse of Völuspá (a poem describing destiny of Agards gods).

.. code-block:: python

   >>> from cltk.tag.pos import POSTag

   >>> tagger = POSTag('old_norse')

   >> sent = 'Hlióðs bið ek allar.'
   >>> tagger.tag_tnt(sent)
   [('Hlióðs', 'Unk'),
    ('bið', 'VBPI'),
    ('ek', 'PRO-N'),
    ('allar', 'Q-A'),
    ('.', '.')]
