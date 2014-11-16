Latin
*****

   
Converting J to I, V to U
======================

.. code-block:: python

   In [1]: from cltk.stem.latin.j_and_v_converter import JVReplacer

   In [2]: j = JVReplacer()

   In [3]: j.replace('vem jam')
   Out[3]: 'uem iam'


Lemmatization
=========

.. code-block:: python

   In [1]: from cltk.stem.latin.lemmatizer import LemmaReplacer

   In [2]: l = LemmaReplacer()

   In [3]: SENTENCE = 'Quo usque tandem abutere, Catilina, patientia nostra?'

   In [4]: l.lemmatize(SENTENCE)
   Out[4]: 'Quo usque tandem abutor, Catilina, patior noster?'


Making POS training sets
========================

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

If you wish to edit the POS dictionary creator, see ``cltk_latin_pos_dict.txt``.For more, see the [pos_latin](https://github.com/kylepjohnson/pos_latin) repository.


POS tagging
===========

To tag parts-of-speech, you must first `import the CLTK Latin linguistic data <http://docs.cltk.org/en/latest/importing_corpora.html#cltk-linguistic-data-latin>`_. The POS tagger is a work in progress, based upon the Perseus treebank. The `CLTK's version of this data is available <https://github.com/cltk/latin_treebank_perseus>`_, along with tagging conventions and instructions on creating your own tagger.

Unigram
```````

.. code-block:: python

   In [1]: from cltk.tag.pos.pos_tagger import POSTag

   In [2]: p = POSTag()

   In [3]: p.unigram_tagger('Gallia est omnis divisa in partes tres', 'latin')
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

   In [4]: p.bigram_tagger('Gallia est omnis divisa in partes tres', 'latin')
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

   In [5]: p.trigram_tagger('Gallia est omnis divisa in partes tres', 'latin')
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

   In [6]: p.ngram_123_backoff_tagger('Gallia est omnis divisa in partes tres', 'latin')
   Out[6]:
   [('Gallia', 'N-S---FB-'),
    ('est', 'V3SPIA---'),
    ('omnis', 'A-S---MN-'),
    ('divisa', 'T-PRPPNN-'),
    ('in', 'R--------'),
    ('partes', 'N-P---FA-'),
    ('tres', 'M--------')]



TnT tagger
`````````````````````````

.. code-block:: python

   In [7]: p.tnt_tagger('Gallia est omnis divisa in partes tres', 'latin')
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

To tokenize sentences, you must first `import the CLTK Latin linguistic data <http://docs.cltk.org/en/latest/importing_corpora.html#cltk-linguistic-data-latin>`_. For more on the tokenizer, or to make your own, see `the CLTK's Latin sentence tokenizer training set repository <https://github.com/cltk/latin_training_set_sentence>`_.

.. code-block:: python

   In [1]: from cltk.tokenize.sentence import tokenize_sentences

   In [2]: untokenized_text = "Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti. Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum."

   In [3]: tokenize_sentences(untokenized_text, 'latin')
   Out[3]:
   ['Itaque cum M. Aurelio et P. Minidio et Cn. Cornelio ad apparationem balistarum et scorpionem reliquorumque tormentorum refectionem fui praesto et cum eis commoda accepi, quae cum primo mihi tribuisiti recognitionem, per sorosis commendationem servasti.',
    'Cum ergo eo beneficio essem obligatus, ut ad exitum vitae non haberem inopiae timorem, haec tibi scribere coepi, quod animadverti multa te aedificavisse et nunc aedificare, reliquo quoque tempore et publicorum et privatorum aedificiorum, pro amplitudine rerum gestarum ut posteris memoriae traderentur curam habiturum.']

Stemming
========
The stemmer strips suffixes via an algorithm. It is much faster than the lemmatizer, which uses a replacement list.

.. code-block:: python
   
   In [1]: from cltk.stem.latin.stemmer import Stemmer

   In [2]: from cltk.stem.latin.j_and_v_converter import JVReplacer

   In [3]: cato = "Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit, et item foenerari, si tam honestum. Maiores nostri sic habuerunt et ita in legibus posiverunt: furem dupli condemnari, foeneratorem quadrupli. Quanto peiorem civem existimarint foeneratorem quam furem, hinc licet existimare. Et virum bonum quom laudabant, ita laudabant: bonum agricolam bonumque colonum; amplissime laudari existimabatur qui ita laudabatur. Mercatorem autem strenuum studiosumque rei quaerendae existimo, verum, ut supra dixi, periculosum et calamitosum. At ex agricolis et viri fortissimi et milites strenuissimi gignuntur, maximeque pius quaestus stabilissimusque consequitur minimeque invidiosus, minimeque male cogitantes sunt qui in eo studio occupati sunt. Nunc, ut ad rem redeam, quod promisi institutum principium hoc erit."

   In [4]: j = JVReplacer()

   In [5]: iu_cato = j.replace(cato.lower())

   In [6]: s = Stemmer()
   
   In [7]: s.stem(iu_cato)
   Out[7]: 'est interd praestar mercatur r quaerere, nisi tam periculos sit, et it foenerari, si tam honestum. maior nostr sic habueru et ita in leg posiuerunt: fur dupl condemnari, foenerator quadrupli. quant peior ciu existimari foenerator quam furem, hinc lice existimare. et uir bon quo laudabant, ita laudabant: bon agricol bon colonum; amplissim laudar existimaba qui ita laudabatur. mercator autem strenu studios re quaerend existimo, uerum, ut supr dixi, periculos et calamitosum. at ex agricol et uir fortissim et milit strenuissim gignuntur, maxim p quaest stabilissim consequi minim inuidiosus, minim mal cogitant su qui in e studi occupat sunt. nunc, ut ad r redeam, quod promis institut principi hoc erit. '


Stopword Filtering
================

.. code-block:: python

   In [1]: from nltk.tokenize.punkt import PunktWordTokenizer

   In [2]: from cltk.stop.latin.stops import STOPS_LIST

   In [3]: SENTENCE = 'Quo usque tandem abutere, Catilina, patientia nostra?'

   In [4]: lowered = SENTENCE.lower()

   In [5]: tokens = PunktWordTokenizer().tokenize(lowered)

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
