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

   This sentence tokenizer appears to work well, though it was trained on a small training set of ~12K words  (Cicero's *Catilinarians*).

.. note::
   The files within `~/cltk/cltk/tokenizers/` are copied from the `CLTK repository dedicated to Latin language sentence tokenization <https://github.com/kylepjohnson/cltk_latin_sentence_tokenizer>`_. See this for more about to improve this training set.

To create a training set, based off a file in which each line begins a new sentece, try the following from within `~/cltk/cltk/tokenizers/`.

.. code-block:: python

   In [1]: from sentence_tokenizer import train_from_file

   In [2]: train_from_file('training_sentences.txt')
     Abbreviation: [12.4351] q
     Abbreviation: [47.2533] c
     Abbreviation: [47.2533] l
     Abbreviation: [0.9149] pl
     Abbreviation: [0.9149] sp
     Abbreviation: [0.3366] kal
     Abbreviation: [2.4870] t
     Abbreviation: [37.3053] p
     Abbreviation: [1.8298] ti
     Abbreviation: [0.9149] cn
     Abbreviation: [14.0461] m
     Abbreviation: [2.4870] d
     Rare Abbrev: fateatur.
     Rare Abbrev: ingravescet.
     Rare Abbrev: ceterorum.
     Sent Starter: [63.1264] 'nam'
     Sent Starter: [40.0581] 'nunc'
     Sent Starter: [51.3624] 'etenim'
     Sent Starter: [55.7801] 'quodsi'
     Sent Starter: [31.5105] 'itaque'

To tokenize a text, such as Cicero's *Catiline* 1, pass it to `tokenize_sentences()` as follows.

.. code-block:: python

   In [1]: from sentence_tokenizer import tokenize_sentences
   
   In [2]: tokenize_sentences('transform/cat1.txt')
   ['Cicero: In Catilinam I\n\t\t \n\n\t\t \n\t\t\n\t\t \n\t\t\n\t\t \n\t\t \n\t \n\t\n \n\n \n\n ORATIO IN L. CATILINAM PRIMA \n\n \n 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 \n \n\n \n[ 1 ] I.', 'Quo usque tandem abutere, Catilina, patientia nostra?', 'quam diu etiam furor iste tuus nos eludet?', 'quem ad finem sese effrenata iactabit audacia?', 'Nihilne te nocturnum praesidium Palati, nihil urbis vigiliae, nihil timor populi, nihil concursus bonorum omnium, nihil hic munitissimus habendi senatus locus, nihil horum ora voltusque moverunt?', 'Patere tua consilia non sentis, constrictam iam horum omnium scientia teneri coniurationem tuam non vides?', 'Quid proxima, quid superiore nocte egeris, ubi fueris, quos convocaveris, quid consilii ceperis, quem nostrum ignorare arbitraris?', ... ]


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
