Classical Latin
************************

POS Tagging
===========

.. warning::

   POS tagging is a work in progress. A new tagging dictionary has been created, though a tagger has not yet been written.

First, `obtain the Latin POS tagging files <http://cltk.readthedocs.org/en/latest/import_corpora.html#pos-tagging>`_. The important file here is ``cltk_latin_pos_dict.txt``, which is saved at ``~/cltk_data/compiled/pos_latin``. This file is a Python ``dict`` type which aims to give all possible parts-of-speech for any given form, though this is based off the incomplete Perseus ``latin-analyses.txt``. Thus, there may be gaps in (i) the inflected forms defined and (ii) the comprehensiveness of the analyses of any given form. ``cltk_latin_pos_dict.txt`` looks like:

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

In order to use the Latin sentence tokenizer, download the compressed rule set, which can be automatically fetched and installed with `the installation commands here <http://cltk.readthedocs.org/en/latest/import_corpora.html#cltk-sentence-tokenizer-latin>`_.

In order to tokenize Latin text by sentence, use one of the following two functions. The function ``tokenize_sentences()`` takes two arguments, the first (file to tokenize) being mandatory and the latter (output file) optional. If no output is given as argument, the list of sentence tokens are simply returned. This example outputs to a specific directory:

.. code-block:: python

   In [1]: from cltk.tokenizers.sentence_tokenizer import tokenize_sentences

   In [2]: tokenize_sentences('/Users/kyle/cltk_data/compiled/latin_library/cicero/phil1.txt', '/Users/kyle/cltk_data/philippics_1_sentence_tokenized.txt')
   ['Cicero: Philippic I\n\t\t \n\n\t\t \n\t\t \n\t \n\t\n \n\n M. TVLLI CICERONIS IN M. ANTONIVM ORATIO PHILIPPICA PRIMA\n \n\n \n\n \n 1 \t 2 \t 3 \t 4 \t 5 \t 6 \t 7 \t 8 \t 9 \t 10 \t 11 \t 12 \t 13 \t 14 \t 15 \t 16 \t 17 \t 18 \t 19 \t 20 \t 21 \t 22 \t 23 \t 24 \t 25 \t 26 \t 27 \t 28 \t 29 \t 30 \t 31 \t 32 \t 33 \t 34 \t 35 \t 36 \t 37 \t 38 \n \n\n \n\n \n[ 1 ] Antequam de republica, patres conscripti, dicam ea, quae dicenda hoc tempore arbitror, exponam vobis breviter consilium et profectionis et reversionis meae.', 'Ego cum sperarem aliquando ad vestrum consilium auctoritatemque rem publicam esse revocatam, manendum mihi statuebam, quasi in vigilia quadam consulari ac senatoria.', 'Nec vero usquam discedebam nec a re publica deiciebam oculos ex eo die, quo in aedem Telluris convocati sumus.', 'In quo templo, quantum in me fuit, ieci fundamenta pacis Atheniensiumque renovavi vetus exemplum; Graecum etiam verbum usurpavi, quo tum in sedandis discordiis usa erat civitas illa, atque omnem memoriam discordiarum oblivione sempiterna delendam censui.', ... ]

The other tokenizing function, `tokenize_sentences_from_str()`, takes raw Latin text as argument, then returns a tokenized list. As with the above, there is an optional output to file. This takes a Latin string and returns the tokens.

.. code-block:: python

   In [1]: from cltk.tokenizers.sentence_tokenizer import tokenize_sentences_from_str

   In [2]: tokenize_sentences_from_str("Quo usque tandem abutere, Catilina, patientia nostra? quam diu etiam furor iste tuus nos eludet? quem ad finem sese effrenata iactabit audacia? Nihilne te nocturnum praesidium Palati, nihil urbis vigiliae, nihil timor populi, nihil concursus bonorum omnium, nihil hic munitissimus habendi senatus locus, nihil horum ora voltusque moverunt? Patere tua consilia non sentis, constrictam iam horum omnium scientia teneri coniurationem tuam non vides? Quid proxima, quid superiore nocte egeris, ubi fueris, quos convocaveris, quid consilii ceperis, quem nostrum ignorare arbitraris? O tempora, o mores! Senatus haec intellegit. Consul videt; hic tamen vivit. Vivit? immo vero etiam in senatum venit, fit publici consilii particeps, notat et designat oculis ad caedem unum quemque nostrum. Nos autem fortes viri satis facere rei publicae videmur, si istius furorem ac tela vitemus. Ad mortem te, Catilina, duci iussu consulis iam pridem oportebat, in te conferri pestem, quam tu in nos [omnes iam diu] machinaris.")
   Out[2]: 
   ['Quo usque tandem abutere, Catilina, patientia nostra?',
    'quam diu etiam furor iste tuus nos eludet?',
    'quem ad finem sese effrenata iactabit audacia?',
    'Nihilne te nocturnum praesidium Palati, nihil urbis vigiliae, nihil timor populi, nihil concursus bonorum omnium, nihil hic munitissimus habendi senatus locus, nihil horum ora voltusque moverunt?',
    'Patere tua consilia non sentis, constrictam iam horum omnium scientia teneri coniurationem tuam non vides?',
    'Quid proxima, quid superiore nocte egeris, ubi fueris, quos convocaveris, quid consilii ceperis, quem nostrum ignorare arbitraris?',
    'O tempora, o mores!',
    'Senatus haec intellegit.',
    'Consul videt; hic tamen vivit.',
    'Vivit?',
    'immo vero etiam in senatum venit, fit publici consilii particeps, notat et designat oculis ad caedem unum quemque nostrum.',
    'Nos autem fortes viri satis facere rei publicae videmur, si istius furorem ac tela vitemus.',
    'Ad mortem te, Catilina, duci iussu consulis iam pridem oportebat, in te conferri pestem, quam tu in nos [omnes iam diu] machinaris.']

.. note::
   This sentence tokenizer appears to work well, though it was trained on a small training set of ~12K words  (Cicero's *Catilinarians*). In the first example, semicolons are not breaking sentences (which should be investivaged).

To create a new training set, based off a file in which each line begins a new sentence, do the following from within the `tokenize` directory.

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
