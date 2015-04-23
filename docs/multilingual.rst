Multilingual
*************

Some functions in the CLTK are language independent.

Concordance
===========

.. note:: This is a new feature. Advice regarding readability is encouraged!

The ``philology`` module can produce a concordance. Currently there are two methods that write a concordance to file, one which takes one or more paths and another which takes a text string. Texts in Latin characters are alphabetized.

.. code-block:: python

   In [1]: from cltk.utils.philology import Philology

   In [2]: p = Philology()

   In [3]: iliad = '~/cltk_data/greek/text/tlg/individual_works/TLG0012.TXT-001.txt'

   In [4]: p.write_concordance_from_file(iliad, 'iliad')


This will print a traditional, human–readable, 120,000–line concordance at ``~/cltk_data/user_data/concordance_iliad.txt``.

Multiple files can be passed as a list into this method.

.. code-block:: python

   In [5]: odyssey = '~/cltk_data/greek/text/tlg/individual_works/TLG0012.TXT-002.txt'

   In [6]: p.write_concordance_from_file([iliad, odyssey], 'homer')

This creates the file ``~/cltk_data/user_data/concordance_homer.txt``.

``write_concordance_from_string()`` takes a string and will build the concordance from it.


.. code-block:: python

   In [7]: from cltk.corpus.utils.formatter import phi5_plaintext_cleanup

   In [8]: import os

   In [9]: tibullus = os.path.expanduser('~/cltk_data/latin/text/phi5/plaintext/LAT0660.TXT')

   In [10]: with open(tibullus) as f:
   ....:     tib_read = f.read()

   In [10]: tib_clean = phi5_plaintext_cleanup(tib_read).lower()

   In [11]: p.write_concordance_from_string(tib_clean, 'tibullus')

The resulting concordance looks like:

.. code-block:: none

   modulatus eburno felices cantus ore sonante dedit. sed postquam fuerant digiti cum voce locuti , edidit haec tristi dulcia verba modo : 'salve , cura
    caveto , neve cubet laxo pectus aperta sinu , neu te decipiat nutu , digitoque liquorem ne trahat et mensae ducat in orbe notas. exibit quam saepe ,
    acerbi : non ego sum tanti , ploret ut illa semel. nec lacrimis oculos digna est foedare loquaces : lena nocet nobis , ipsa puella bona est. lena ne
   eaera tamen.” “carmine formosae , pretio capiuntur avarae. gaudeat , ut digna est , versibus illa tuis. lutea sed niveum involvat membrana libellum ,
   umnus olympo mille habet ornatus , mille decenter habet. sola puellarum digna est , cui mollia caris vellera det sucis bis madefacta tyros , possidea
    velim , sed peccasse iuvat , voltus conponere famae taedet : cum digno digna fuisse ferar. invisus natalis adest , qui rure molesto et sine cerintho
   a phoebe superbe lyra. hoc sollemne sacrum multos consummet in annos : dignior est vestro nulla puella choro. parce meo iuveni , seu quis bona pascua
  a para. sic bene conpones : ullae non ille puellae servire aut cuiquam dignior illa viro. nec possit cupidos vigilans deprendere custos , fallendique



Corpora
=======

The CLTK uses languages in its organization of data, however some good corpora do not and cannot be easily broken apart. Furthermore, some, such as parallel text corpora, are inherently multilingual. Use ``CorpusImporter()`` or browse the `CLTK GitHub repository <https://github.com/cltk>`_ (anything beginning with ``multilingual_``) to discover available multilingual corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('multilingual')

   In [3]: c.list_corpora
   Out[3]: ['multilingual_treebank_proiel']


N–grams
=======


 .. code-block:: python

   In [1]: from nltk.tokenize.punkt import PunktLanguageVars

   In [2]: from nltk.util import bigrams

   In [3]: from nltk.util import trigrams

   In [4]: from nltk.util import ngrams

   In [5]: s = 'Ut primum nocte discussa sol novus diem fecit, et somno simul emersus et lectulo, anxius alioquin et nimis cupidus cognoscendi quae rara miraque sunt, reputansque me media Thessaliae loca tenere qua artis magicae nativa cantamina totius orbis consono orbe celebrentur fabulamque illam optimi comitis Aristomenis de situ civitatis huius exortam, suspensus alioquin et voto simul et studio, curiose singula considerabam. Nec fuit in illa civitate quod aspiciens id esse crederem quod esset, sed omnia prorsus ferali murmure in aliam effigiem translata, ut et lapides quos offenderem de homine duratos et aves quas audirem indidem plumatas et arbores quae pomerium ambirent similiter foliatas et fontanos latices de corporibus humanis fluxos crederem; iam statuas et imagines incessuras, parietes locuturos, boves et id genus pecua dicturas praesagium, de ipso vero caelo et iubaris orbe subito venturum oraculum.'.lower()

   In [6]: p = PunktLanguageVars()

   In [7]: tokens = p.word_tokenize(s)

   In [8]: b = bigrams(tokens)

   In [8]: [x for x in b]
   Out[8]:
   [('ut', 'primum'),
    ('primum', 'nocte'),
    ('nocte', 'discussa'),
    ('discussa', 'sol'),
    ('sol', 'novus'),
    ('novus', 'diem'),
    ...]

   In [9]: t = trigrams(tokens)
   In [9]: [x for x in t]
   [('ut', 'primum', 'nocte'),
    ('primum', 'nocte', 'discussa'),
    ('nocte', 'discussa', 'sol'),
    ('discussa', 'sol', 'novus'),
    ('sol', 'novus', 'diem'),
    …]

   In [10]: five_gram = ngrams(tokens, 5)

   In [11]: [x for x in five_gram]
   Out[11]:
   [('ut', 'primum', 'nocte', 'discussa', 'sol'),
    ('primum', 'nocte', 'discussa', 'sol', 'novus'),
    ('nocte', 'discussa', 'sol', 'novus', 'diem'),
    ('discussa', 'sol', 'novus', 'diem', 'fecit'),
    ('sol', 'novus', 'diem', 'fecit', ','),
    ('novus', 'diem', 'fecit', ',', 'et'),
    …]


Stopword generator
==================

The stopword generator makes a list the most commonly occurring words in a text.

.. code-block:: python

   In [1]: from cltk.stop.make_stopwords_list import Stopwords

   In [2]: s = Stopwords('coptic')

   In [3]: text = 'ⲡⲁⲩⲗⲟⲥ ⲡ ⲁⲡⲟⲥⲧⲟⲗⲟⲥ ⲉⲧ ⲧⲁϩⲙ ⲙ ⲡⲉ ⲭⲣⲓⲥⲧⲟⲥ ⲓⲏⲥⲟⲩⲥ ϩⲓⲧⲙ ⲡ ⲟⲩⲱϣ ⲙ ⲡ ⲛⲟⲩⲧⲉ'

   In [4]: stops = s.make_list_from_str(text, 5)  # get 5 most common words

   In [5]: sentence = 'ⲡⲁⲩⲗⲟⲥ ⲡ ⲁⲡⲟⲥⲧⲟⲗⲟⲥ ⲉⲧ ⲧⲁϩⲙ ⲙ ⲡⲉ ⲭⲣⲓⲥⲧⲟⲥ ⲓⲏⲥⲟⲩⲥ ϩⲓⲧⲙ ⲡ ⲟⲩⲱϣ ⲙ ⲡ ⲛⲟⲩⲧⲉ ⲙⲛ ⲥⲱⲥⲑⲉⲛⲏⲥ ⲡ ⲥⲟⲛ ⲉ ⲩ ⲥϩⲁⲓ ⲛ ⲧ ⲉⲕⲕⲗⲏⲥⲓⲁ ⲙ ⲡ ⲛⲟⲩⲧⲉ ⲧⲁⲓ ⲉⲧ ϣⲟⲟⲡ ϩⲛ ⲕⲟⲣⲓⲛⲑⲟⲥ .'

   In [6]: tokens = p.word_tokenize(sentence)

   In [7]: no_stops = [w for w in tokens if not w in stops]

   In [8]: ' '.join(no_stops)
   Out[8]: 'ⲡⲁⲩⲗⲟⲥ ⲉⲧ ⲧⲁϩⲙ ⲡⲉ ⲭⲣⲓⲥⲧⲟⲥ ⲓⲏⲥⲟⲩⲥ ⲛⲟⲩⲧⲉ ⲙⲛ ⲥⲱⲥⲑⲉⲛⲏⲥ ⲥⲟⲛ ⲉ ⲩ ⲥϩⲁⲓ ⲛ ⲧ ⲉⲕⲕⲗⲏⲥⲓⲁ ⲛⲟⲩⲧⲉ ⲧⲁⲓ ⲉⲧ ϣⲟⲟⲡ ϩⲛ ⲕⲟⲣⲓⲛⲑⲟⲥ .'


Word count
==========

For a dictionary-like object of word frequencies, use the NLTK's ``Text()``.

 .. code-block:: python

   In [1]: from nltk.tokenize.punkt import PunktLanguageVars

   In [2]: from nltk.text import Text

   In [3]: s = 'At at at ego ego tibi'.lower()

   In [4]: p = PunktLanguageVars()

   In [5]: tokens = p.word_tokenize(s)

   In [6]: t = Text(tokens)

   In [7]: vocabulary_count = t.vocab()

   In [8]: vocabulary_count['at']
   Out[8]: 3

   In [9]: vocabulary_count['ego']
   Out[9]: 2

   In [10]: vocabulary_count['tibi']
   Out[10]: 1



Word tokenization
=================

The NLTK offers several methods for word tokenization. The ``PunktLanguageVars`` is the latest tokenizer.

.. code-block:: python

   In [1]: from cltk.corpus.utils.formatter import phi5_plaintext_cleanup

   In [2]: from nltk.text import Text

   In [3]: from nltk.tokenize.punkt import PunktLanguageVars

   In [4]: import os

   In [5]: path = '~/cltk_data/latin/text/phi5/individual_works/LAT0690.TXT-003.txt'

   In [6]: path = os.path.expanduser(path)

   In [7]: with open(path) as f:
      ...:     r = f.read()
      ...:

   In [8]: cleaned = phi5_plaintext_cleanup(r)

   In [9]: p = PunktLanguageVars()

   In [10]: tokens = p.word_tokenize(cleaned)

   In [13]: tokens[:10]
   Out[13]:
   ['Arma',
    'uirumque',
    'cano',
    ',',
    'Troiae',
    'qui',
    'primus',
    'ab',
    'oris',
    'Italiam']


Another, simpler tokenizer can tokenize on word breaks and whatever other regular expressions you add.

.. code-block:: python

   In [14]: from nltk.tokenize import RegexpTokenizer

   In [15]: word_breaks = RegexpTokenizer(r'\w+')

   In [16]: tokens = word_breaks.tokenize(cleaned)

   In [17]: tokens[:10]
   Out[17]: ['Arma',
    'uirumque',
    'cano',
    'Troiae',
    'qui',
    'primus',
    'ab',
    'oris',
    'Italiam',
    'fato']

