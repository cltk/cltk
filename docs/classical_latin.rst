Classical Latin
************************

POS Tagging
===========

.. warning::

   POS tagging is a work in progress. A new tagging dictionary has been created, though a tagger has not yet been written.

First, `obtain the Latin POS tagging files <http://cltk.readthedocs.org/en/latest/import_corpora.html#pos-tagging>`_. The important file here is ``cltk_latin_pos_dict.txt``, which is saved at ``~/cltk_data/compiled/pos_latin``. This file is a Python ``dict`` type which aims to give all possible parts-of-speech for any given form, though this is based off the incomplete Perseus ``latin-analyses.txt``. Thus, there may be gaps either in (i) the inflected forms defined and (ii) the comprehensiveness of the analyses of any given form. ``cltk_latin_pos_dict.txt`` looks like:

.. code-block:: python

   {'-nam': {'perseus_pos': [{'pos0': {'case': 'indeclform',
                                       'gloss': '',
                                       'type': 'conj'}}]},
    '-namque': {'perseus_pos': [{'pos0': {'case': 'indeclform',
                                          'gloss': '',
                                          'type': 'conj'}}]},
    '-sed': {'perseus_pos': [{'pos0': {'case': 'indeclform',
                                       'gloss': '',
                                       'type': 'conj'}}]},
    'Aaron': {'perseus_pos': [{'pos0': {'case': 'nom',
                                        'gender': 'masc',
                                        'gloss': 'Aaron',
                                        'number': 'sg',
                                        'type': 'substantive'}}]},
   }

If you wish to edit the POS dictionary creator, ``cltk_latin_pos_dict.txt`` may be recreated with:

.. code-block:: python

   In [1]: from cltk.tag.classical_latin.pos_latin import MakePOSTagger

   In [2]: m = MakePOSTagger()

   In [3]: m.make_file()

Sentence Tokenization
=====================

.. warning::

   Sentence tagging works with the following recipe. It remains to be run on a larger, known training set, then the results saved to a Latin tokenization data file.

All of the following commands were done with IPython in the directory `~/cltk/cltk/tokenizers/`.

.. code-block:: python

In [1]: import nltk

In [2]: language_punkt_vars = nltk.tokenize.punkt.PunktLanguageVars

In [3]: language_punkt_vars.sent_end_chars=('.', '?', ';', ':')

In [4]: with open('sents_cael.txt') as f:
    train_data = f.read()

In [5]: trainer = nltk.tokenize.punkt.PunktTrainer(train_data, language_punkt_vars)
  Abbreviation: [5.0545] c
  Abbreviation: [0.3420] sex
  Abbreviation: [50.5447] m
  Abbreviation: [15.1634] q
  Abbreviation: [17.6906] l
  Abbreviation: [0.9297] cn
  Abbreviation: [10.1089] p
  Rare Abbrev: putaverunt.
  Sent Starter: [42.0636] 'sed'
  Sent Starter: [48.3138] 'nam'

In [6]: params = trainer.get_params()

In [7]: sbd = nltk.tokenize.punkt.PunktSentenceTokenizer(params)

In [8]: with open('phil1.txt') as f:
   ....:     to_be_tokenized = f.read()
   ....:     

for sentence in sbd.sentences_from_text(to_be_tokenized, realign_boundaries=True):
    print(sentence)
    print('---')


Text Processing
===============

Filter Stopwords
----------------

.. code-block:: python

   In [1]: import nltk.tokenize

   In [2]: from cltk.stop.classical_latin.stops import STOPS_LIST

   In [3]: SENTENCE = 'Quo usque tandem abutere, Catilina, patientia nostra?'

   In [4]: lowered = SENTENCE.lower()

   In [5]: tokens = nltk.word_tokenize(lowered)

   In [6]: [w for w in tokens if not w in STOPS_LIST]
   Out[6]: 
   ['usque',
    'tandem',
    'abutere',
    ',',
    'catilina',
    ',',
    'patientia',
    'nostra',
    '?']

   
Convert J to I, V to U
----------------------

.. code-block:: python

   In [1]: from cltk.stem.classical_latin.j_and_v_converter import JVReplacer

   In [2]: j = JVReplacer()

   In [3]: j.replace('vem jam')
   Out[3]: 'uem iam'
