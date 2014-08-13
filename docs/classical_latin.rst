Classical Latin
************************

   
Converting J to I, V to U
======================

.. code-block:: python

   In [1]: from cltk.stem.classical_latin.j_and_v_converter import JVReplacer

   In [2]: j = JVReplacer()

   In [3]: j.replace('vem jam')
   Out[3]: 'uem iam'


Lemmatization
=========

.. code-block:: python

   In [1]: from cltk.stem.classical_latin.lemmatizer import LemmaReplacer

   In [2]: l = LemmaReplacer()

   In [3]: SENTENCE = 'Quo usque tandem abutere, Catilina, patientia nostra?'

   In [4]: l.lemmatize(SENTENCE)
   Out[4]: 'Quo usque tandem abutor, Catilina, patior noster?'


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

In order to use the Latin sentence tokenizer, download the compressed rule and training sets, which can be fetched and installed with `the installation commands here <http://cltk.readthedocs.org/en/latest/import_corpora.html#cltk-sentence-tokenizer-latin>`_.

To tokenize sentences, give a string as argument to ``train_and_tokenize_latin()``, as follows.

.. code-block:: python

   In [1]: from cltk.tokenizers.sentence_tokenizer import train_and_tokenize_latin

   In [2]: phil_14 = """Si, ut ex litteris, quae recitatae sunt, patres conscripti, sceleratissimorum hostium exercitum caesum fusumque cognovi, sic id, quod et omnes maxime optamus et ex ea victoria, quae parta est, consecutum arbitramur, D. Brutum egressum iam Mutina esse cognovissem, propter cuius periculum ad saga issemus, propter eiusdem salutem redeundum ad pristinum vestitum sine ulla dubitatione censerem. Ante vero quam sit ea res, quam avidissime civitas exspectat, allata, laetitia frui satis est maximae praeclarissimaeque pugnae; reditum ad vestitum confectae victoriae reservate. Confectio autem huius belli est D. Bruti salus. Quae autem est ista sententia, ut in hodiernum diem vestitus mutetur, deinde cras sagati prodeamus? Nos vero cum semel ad eum, quem cupimus optamusque, vestitum redierimus, id agamus, ut eum in perpetuum retineamus. Nam hoc quidem cum turpe est, tum ne dis quidem immortalibus gratum, ab eorum aris, ad quas togati adierimus, ad saga sumenda discedere. Atque animadverto , patres conscripti, quosdam huic favere sententiae; quorum ea mens idque consilium est, ut, cum videant gloriosissimum illum D. Bruto futurum diem, quo die propter eius salutem redierimus ad vestitum, hunc ei fructum eripere cupiant, ne memoriae posteritatique prodatur propter unius civis periculum populum Romanum ad saga isse, propter eiusdem salutem redisse ad togas. Tollite hanc; nullam tam pravae sententiae causam reperietis. Vos vero, patres conscripti, conservate auctoritatem vestram, manete in sententia, tenete vestra memoria, quod saepe ostendistis, huius totius belli in unius viri fortissimi et maximi vita positum esse discrimen. Ad D. Brutum liberandum legati missi principes civitatis, qui illi hosti ac parricidae denuntiarent, ut a Mutina discederet; eiusdem D. Bruti conservandi gratia consul sortitu ad bellum profectus A. Hirtius, cuius inbecillitatem valetudinis animi virtus et spes victoriae confirmavit; Caesar cum exercitu per se comparato, cum prius pestibus rem publicam liberasset, ne quid postea sceleris oriretur, profectus est ad eundem Brutum liberandum vicitque dolorem aliquem domesticum patriae caritate."""

   In [3]: train_and_tokenize_latin(phil_14)
     Abbreviation: [12.4351] q
     Abbreviation: [2.4870] t
     Abbreviation: [47.2533] c
     Abbreviation: [1.8298] ti
     Abbreviation: [0.9149] cn
     Abbreviation: [14.0461] m
     Abbreviation: [47.2533] l
     Abbreviation: [0.9149] pl
     Removed abbreviation: [-0.0000] ceterorum
     Abbreviation: [2.4870] d
     Abbreviation: [37.3053] p
     Removed abbreviation: [-0.0000] fateatur
     Abbreviation: [0.9149] sp
     Abbreviation: [0.3366] kal
     Rare Abbrev: fateatur.
     Rare Abbrev: ceterorum.
     Sent Starter: [51.3932] 'etenim'
     Sent Starter: [31.5289] 'itaque'
     Sent Starter: [63.1635] 'nam'
     Sent Starter: [40.0909] 'nunc'
     Sent Starter: [55.8081] 'quodsi'
   Out[7]: 
   ['Si, ut ex litteris, quae recitatae sunt, patres conscripti, sceleratissimorum hostium exercitum caesum fusumque cognovi, sic id, quod et omnes maxime optamus et ex ea victoria, quae parta est, consecutum arbitramur, D. Brutum egressum iam Mutina esse cognovissem, propter cuius periculum ad saga issemus, propter eiusdem salutem redeundum ad pristinum vestitum sine ulla dubitatione censerem.',
    'Ante vero quam sit ea res, quam avidissime civitas exspectat, allata, laetitia frui satis est maximae praeclarissimaeque pugnae;',
    'reditum ad vestitum confectae victoriae reservate.',
    'Confectio autem huius belli est D. Bruti salus.',
    'Quae autem est ista sententia, ut in hodiernum diem vestitus mutetur, deinde cras sagati prodeamus?',
    'Nos vero cum semel ad eum, quem cupimus optamusque, vestitum redierimus, id agamus, ut eum in perpetuum retineamus.',
    'Nam hoc quidem cum turpe est, tum ne dis quidem immortalibus gratum, ab eorum aris, ad quas togati adierimus, ad saga sumenda discedere.',
    'Atque animadverto , patres conscripti, quosdam huic favere sententiae;',
    'quorum ea mens idque consilium est, ut, cum videant gloriosissimum illum D. Bruto futurum diem, quo die propter eius salutem redierimus ad vestitum, hunc ei fructum eripere cupiant, ne memoriae posteritatique prodatur propter unius civis periculum populum Romanum ad saga isse, propter eiusdem salutem redisse ad togas.',
    'Tollite hanc;',
    'nullam tam pravae sententiae causam reperietis.',
    'Vos vero, patres conscripti, conservate auctoritatem vestram, manete in sententia, tenete vestra memoria, quod saepe ostendistis, huius totius belli in unius viri fortissimi et maximi vita positum esse discrimen.',
    'Ad D. Brutum liberandum legati missi principes civitatis, qui illi hosti ac parricidae denuntiarent, ut a Mutina discederet;',
    'eiusdem D. Bruti conservandi gratia consul sortitu ad bellum profectus A. Hirtius, cuius inbecillitatem valetudinis animi virtus et spes victoriae confirmavit;',
    'Caesar cum exercitu per se comparato, cum prius pestibus rem publicam liberasset, ne quid postea sceleris oriretur, profectus est ad eundem Brutum liberandum vicitque dolorem aliquem domesticum patriae caritate.']


.. note::

   The tokenizer (`latin.pickle`) is not persisting after it is made (that or it is being incorrectly read), which is why right now the tokenizer recreates it for every use.


Stemming
========
The stemmer strip suffixes via an algorithm. It is much faster than the lemmatizer, which uses a replacement list.

.. code-block:: python
   
   In [1]: from cltk.stem.classical_latin.stemmer import Stemmer

   In [2]: from cltk.stem.classical_latin.j_and_v_converter import JVReplacer

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

   In [2]: from cltk.stop.classical_latin.stops import LATIN_STOPS_LIST

   In [3]: SENTENCE = 'Quo usque tandem abutere, Catilina, patientia nostra?'

   In [4]: lowered = SENTENCE.lower()

   In [5]: tokens = PunktWordTokenizer().tokenize(lowered)

   In [6]: [w for w in tokens if not w in LATIN_STOPS_LIST]
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
