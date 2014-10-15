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

The POS tagger is a work in progress, based upon the Perseus treebank. The `CLTK's version of this data is available<https://github.com/cltk/latin_treebank_perseus>`_, along with tagging conventions and instructions on creating your own POS tagger.


Sentence Tokenization
=====================

In order to use the Latin sentence tokenizer, download the compressed rule and training sets, which can be fetched and installed with `the installation commands here <http://cltk.readthedocs.org/en/latest/import_corpora.html#cltk-sentence-tokenizer-latin>`_.

To tokenize sentences, give a string as argument to ``train_and_tokenize_latin()``, as follows.

.. code-block:: python

   In [1]: from cltk.tokenize.sentence_tokenizer_latin import tokenize_latin_sentences

   In [2]: untokenized_text = "Num qui exsules restituti? Unum aiebat, praeterea neminem. Num immunitates datae? 'Nullae', respondebat. Assentiri etiam nos Ser. Sulpicio, clarissimo viro, voluit, ne qua tabula post Idus Martias ullius decreti Caesaris aut beneficii figeretur. Multa praetereo, eaque praeclara; ad singulare enim M. Antoni factum festinat oratio. Dictaturam, quae iam vim regiae potestatis obsederat, funditus ex re publica sustulit; de qua re ne sententias quidem diximus. Scriptum senatus consultum, quod fieri vellet, attulit; quo recitato, auctoritatem eius summo studio secuti sumus eique amplissimis verbis per senatus consultum gratias egimus."

   In [3]: tokenize_latin_sentences(untokenized_text)
   Out[3]:
   ['Num qui exsules restituti?',
    'Unum aiebat, praeterea neminem.',
    'Num immunitates datae?',
    "'Nullae', respondebat.",
    'Assentiri etiam nos Ser.',
    'Sulpicio, clarissimo viro, voluit, ne qua tabula post Idus Martias ullius decreti Caesaris aut beneficii figeretur.',
    'Multa praetereo, eaque praeclara; ad singulare enim M. Antoni factum festinat oratio.',
    'Dictaturam, quae iam vim regiae potestatis obsederat, funditus ex re publica sustulit; de qua re ne sententias quidem diximus.',
   'Scriptum senatus consultum, quod fieri vellet, attulit; quo recitato, auctoritatem eius summo studio secuti sumus eique amplissimis verbis per senatus consultum gratias egimus.']


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
