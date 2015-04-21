Latin
*****
For most of the following operations, you must first `import the CLTK Latin linguistic data <http://docs.cltk.org/en/latest/importing_corpora.html>`_ (named ``latin_models_cltk``).

Note that for most of the following operations, the j/i and v/u replacer ``JVReplacer()`` and ``.lower()`` should be used on the input string first, if necessary.

Converting J to I, V to U
=========================
.. code-block:: python

   In [1]: from cltk.stem.latin.j_v import JVReplacer

   In [2]: j = JVReplacer()

   In [3]: j.replace('vem jam')
   Out[3]: 'uem iam'



Converting PHI texts with TLGU
==============================

.. note::

   1) Update this section with new post-TLGU processors in formatter.py

The `TLGU <http://tlgu.carmen.gr/>`_ is C-language software which does an excellent job at converting the TLG and PHI corpora into various forms of human-readable Unicode plaintext. The CLTK has an automated downloader and installer, as well as a wrapper which facilitates its use. Download and installation is handled in the background. When ``TLGU()`` is instantiated, it checks the local OS for a functioning version of the software. If not found it is installed.

Most users will want to do a bulk conversion of the entirety of a corpus without any text markup (such as chapter or line numbers).

.. code-block:: python

   In [1]: from cltk.corpus.greek.tlgu import TLGU

   In [2]: t = TLGU()

   In [3]: t.convert_corpus(corpus='phi5')  # ~/cltk_data/latin/text/tlg/plaintext/ #! This isn't working!


You can also divide the texts into a file for each individual work.

.. code-block:: python

   In [4]: t.divide_works('phi5')  # ~/cltk_data/latin/text/phi5/individual_works/



Lemmatization
=============
.. code-block:: python

   In [1]: from cltk.stem.lemma import LemmaReplacer

   In [2]: from cltk.stem.latin.j_v import JVReplacer

   In [3]: sentence = 'Aeneadum genetrix, hominum divomque voluptas, alma Venus, caeli subter labentia signa quae mare navigerum, quae terras frugiferentis concelebras, per te quoniam genus omne animantum concipitur visitque exortum lumina solis.'

   In [4]: j = JVReplacer()

   In [5]: sentence = j.replace(sentence)

   In [6]: sentence = sentence.lower()

   In [7]: lemmatizer = LemmaReplacer('latin')

   In [8]: lemmatizer.lemmatize(sentence)
   Out[8]: 'aeneadum genetrix, homo divus voluptas, almus venus2, caelus subter labor1 signum qui1 marum nauigerum, qui1 terra frugiferens concelebro, per tu quoniam genus1 omnicanus animantum concipio uisitque exortus2 lumen solus1.'



Making POS training sets
========================
.. warning::

   POS tagging is a work in progress. A new tagging dictionary has been created, though a tagger has not yet been written.

First, `obtain the Latin POS tagging files <http://docs.cltk.org/en/latest/importing_corpora.html#pos-tagging>`_. The important file here is ``cltk_latin_pos_dict.txt``, which is saved at ``~/cltk_data/compiled/pos_latin``. This file is a Python ``dict`` type which aims to give all possible parts-of-speech for any given form, though this is based off the incomplete Perseus ``latin-analyses.txt``. Thus, there may be gaps in (i) the inflected forms defined and (ii) the comprehensiveness of the analyses of any given form. ``cltk_latin_pos_dict.txt`` looks like:

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

If you wish to edit the POS dictionary creator, see ``cltk_latin_pos_dict.txt``.For more, see the [pos_latin](https://github.com/kylepjohnson/pos_latin) repository.


PHI Indices
===========

Located at ``cltk/corpus/latin/phi5_index.py`` of the source are indices for the PHI5, one of just id and name (``PHI5_INDEX``) and another also containing information on the authors' works (``PHI5_WORKS_INDEX``).

.. code-block:: python

   In [1]: from cltk.corpus.latin.phi5_index import PHI5_INDEX

   In [2]: PHI5_INDEX
   Out[2]:
   {'LAT1050': 'Lucius Verginius Rufus',
    'LAT2335': 'Anonymi de Differentiis [Fronto]',
    'LAT1345': 'Silius Italicus',
    ... }

   In [3]: from cltk.corpus.latin.phi5_index import PHI5_WORKS_INDEX

   In [4]: PHI5_WORKS_INDEX
   Out [4]:
   {'LAT2335': {'works': ['001'], 'name': 'Anonymi de Differentiis [Fronto]'},
    'LAT1345': {'works': ['001'], 'name': 'Silius Italicus'},
    'LAT1351': {'works': ['001', '002', '003', '004', '005'],
     'name': 'Cornelius Tacitus'},
    'LAT2349': {'works': ['001', '002', '003', '004', '005', '006', '007'],
     'name': 'Maurus Servius Honoratus, Servius'},
     ...}


In addition to these indices there are several helper functions which will build filepaths for your particular computer. Not that you will need to have run ``convert_corpus(corpus='phi5')`` and ``divide_works('phi5')`` from the ``TLGU()`` class, respectively, for the following two functions.

.. code-block:: python

   In [1]: from cltk.corpus.utils.formatter import assemble_phi5_author_filepaths

   In [2]: assemble_phi5_author_filepaths()
   Out[2]:
   ['/Users/kyle/cltk_data/latin/text/phi5/plaintext/LAT0636.TXT',
    '/Users/kyle/cltk_data/latin/text/phi5/plaintext/LAT0658.TXT',
    '/Users/kyle/cltk_data/latin/text/phi5/plaintext/LAT0827.TXT',
    ...]

   In [3]: from cltk.corpus.utils.formatter import assemble_phi5_works_filepaths

   In [4]: assemble_phi5_works_filepaths()
   Out[4]:
   ['/Users/kyle/cltk_data/latin/text/phi5/individual_works/LAT0636.TXT-001.txt',
    '/Users/kyle/cltk_data/latin/text/phi5/individual_works/LAT0902.TXT-001.txt',
    '/Users/kyle/cltk_data/latin/text/phi5/individual_works/LAT0472.TXT-001.txt',
    '/Users/kyle/cltk_data/latin/text/phi5/individual_works/LAT0472.TXT-002.txt',
    ...]

These two functions are useful when, for example, needing to process all authors of the PHI5 corpus, all works of the corpus, or all works of one particular author.


POS tagging
===========

Unigram
```````
.. code-block:: python

   In [1]: from cltk.tag.pos import POSTag

   In [2]: tagger = POSTag('latin')

   In [3]: tagger.tag_unigram('Gallia est omnis divisa in partes tres')
   Out[3]:
   [('Gallia', 'N-S---FB-'),
    ('est', 'V3SPIA---'),
    ('omnis', 'A-P---MA-'),
    ('divisa', 'T-SRPPFN-'),
    ('in', 'R--------'),
    ('partes', 'N-P---FA-'),
    ('tres', 'M--------')]


Bigram
``````
.. code-block:: python

   In [4]: tagger.tag_bigram('Gallia est omnis divisa in partes tres')
   Out[4]:
   [('Gallia', None),
    ('est', None),
    ('omnis', None),
    ('divisa', None),
    ('in', None),
    ('partes', None),
    ('tres', None)]


Trigram
```````
.. code-block:: python

   In [5]: tagger.tag_trigram('Gallia est omnis divisa in partes tres')
   Out[5]:
   [('Gallia', None),
    ('est', None),
    ('omnis', None),
    ('divisa', None),
    ('in', None),
    ('partes', None),
    ('tres', None)]


1–2–3–gram backoff tagger
`````````````````````````
.. code-block:: python

   In [6]: tagger.tag_ngram_123_backoff('Gallia est omnis divisa in partes tres')
   Out[6]:
   [('Gallia', 'N-S---FB-'),
    ('est', 'V3SPIA---'),
    ('omnis', 'A-S---MN-'),
    ('divisa', 'T-PRPPNN-'),
    ('in', 'R--------'),
    ('partes', 'N-P---FA-'),
    ('tres', 'M--------')]



TnT tagger
``````````
.. code-block:: python

   In [7]: tagger.tag_tnt('Gallia est omnis divisa in partes tres')
   Out[7]:
   [('Gallia', 'N-S---FB-'),
    ('est', 'V3SPIA---'),
    ('omnis', 'N-S---MN-'),
    ('divisa', 'T-SRPPFN-'),
    ('in', 'R--------'),
    ('partes', 'N-P---FA-'),
    ('tres', 'M--------')]


Sentence Tokenization
=====================
The sentence tokenizer takes a string input into ``tokenize_sentences()`` and returns a list of strings. For more on the tokenizer, or to make your own, see `the CLTK's Latin sentence tokenizer training set repository <https://github.com/cltk/latin_training_set_sentence>`_.

.. code-block:: python

   In [1]: from cltk.tokenize.sentence import TokenizeSentence

   In [2]: tokenizer = TokenizeSentence('latin')

   In [3]: untokenized_text = 'Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti. Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum.'

   In [4]: tokenizer.tokenize_sentences(untokenized_text)
   Out[4]:
   ['Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti.',
    'Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum.']

Stemming
========
The stemmer strips suffixes via an algorithm. It is much faster than the lemmatizer, which uses a replacement list.

.. code-block:: python

   In [1]: from cltk.stem.latin.stem import Stemmer

   In [2]: sentence = 'Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit, et item foenerari, si tam honestum. Maiores nostri sic habuerunt et ita in legibus posiuerunt: furem dupli condemnari, foeneratorem quadrupli. Quanto peiorem ciuem existimarint foeneratorem quam furem, hinc licet existimare. Et uirum bonum quom laudabant, ita laudabant: bonum agricolam bonumque colonum; amplissime laudari existimabatur qui ita laudabatur. Mercatorem autem strenuum studiosumque rei quaerendae existimo, uerum, ut supra dixi, periculosum et calamitosum. At ex agricolis et uiri fortissimi et milites strenuissimi gignuntur, maximeque pius quaestus stabilissimusque consequitur minimeque inuidiosus, minimeque male cogitantes sunt qui in eo studio occupati sunt. Nunc, ut ad rem redeam, quod promisi institutum principium hoc erit.'

   In [3]: stemmer = Stemmer()
   
   In [4]: stemmer.stem(sentence.lower())
   Out[4]: 'est interd praestar mercatur r quaerere, nisi tam periculos sit, et it foenerari, si tam honestum. maior nostr sic habueru et ita in leg posiuerunt: fur dupl condemnari, foenerator quadrupli. quant peior ciu existimari foenerator quam furem, hinc lice existimare. et uir bon quo laudabant, ita laudabant: bon agricol bon colonum; amplissim laudar existimaba qui ita laudabatur. mercator autem strenu studios re quaerend existimo, uerum, ut supr dixi, periculos et calamitosum. at ex agricol et uir fortissim et milit strenuissim gignuntur, maxim p quaest stabilissim consequi minim inuidiosus, minim mal cogitant su qui in e studi occupat sunt. nunc, ut ad r redeam, quod promis institut principi hoc erit. '

Syllabifier
========
The syllabifier splits a given input Latin word into a list of syllables based on an algorithm and set of syllable specifications for Latin.

.. code-block:: python

   In [1]: from cltk.stem.latin.syllabifier import Syllabifier

   In [2]: word = 'sidere' 

   In [3]: syllabifier = Syllabifier()
   
   In [4]: syllabifier.syllabify(word)
   Out[4]: ['si', 'de', 're']


Stopword Filtering
==================
.. code-block:: python

   In [1]: from nltk.tokenize.punkt import PunktLanguageVars

   In [2]: from cltk.stop.latin.stops import STOPS_LIST

   In [3]: sentence = 'Quo usque tandem abutere, Catilina, patientia nostra?'

   In [4]: p = PunktLanguageVars()

   In [5]: tokens = p.word_tokenize(sentence.lower())

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


Text Cleanup
============

Intended for use on the TLG after processing by ``TLGU()``.

.. code-block::

   In [1]: from cltk.corpus.utils.formatter import phi5_plaintext_cleanup

   In [2]: import os

   In [3]: file = os.path.expanduser('~/cltk_data/latin/text/phi5/individual_works/LAT0031.TXT-001.txt')

   In [4]: with open(file) as f:
   ...:     r = f.read()
   ...:

   In [5]: r[:500]
   Out[5]: '\nDices pulchrum esse inimicos \nulcisci. id neque maius neque pulchrius cuiquam atque mihi esse uide-\ntur, sed si liceat re publica salua ea persequi. sed quatenus id fieri non  \npotest, multo tempore multisque partibus inimici nostri non peribunt \natque, uti nunc sunt, erunt potius quam res publica profligetur atque \npereat. \n    Verbis conceptis deierare ausim, praeterquam qui \nTiberium Gracchum necarunt, neminem inimicum tantum molestiae \ntantumque laboris, quantum te ob has res, mihi tradidis'

   In [6]: phi5_plaintext_cleanup(r)[:500]
   Out[6]: ' Dices pulchrum esse inimicos  ulcisci. id neque maius neque pulchrius cuiquam atque mihi esse uidetur, sed si liceat re publica salua ea persequi. sed quatenus id fieri non   potest, multo tempore multisque partibus inimici nostri non peribunt  atque, uti nunc sunt, erunt potius quam res publica profligetur atque  pereat.      Verbis conceptis deierare ausim, praeterquam qui  Tiberium Gracchum necarunt, neminem inimicum tantum molestiae  tantumque laboris, quantum te ob has res, mihi tradidisse'



If you have a text of a language in Latin characters which contain a lot of junk, ``remove_non_ascii()`` might be of use.

.. code-block::

   In [1]: from cltk.corpus.utils.formatter import remove_non_ascii

   In [2]: text =  'Dices ἐστιν ἐμός pulchrum esse inimicos ulcisci.'

   In [3]: remove_non_ascii(text)
   Out[3]: 'Dices   pulchrum esse inimicos ulcisci.
