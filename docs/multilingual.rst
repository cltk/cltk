Multilingual
************

Some functions in the CLTK are language independent.

Concordance
===========

.. note:: This is a new feature. Advice regarding readability is encouraged!

The ``philology`` module can produce a concordance. Currently there are two methods that write a concordance to file, one which takes one or more paths and another which takes a text string. Texts in Latin characters are alphabetized.

.. code-block:: python

   In [1]: from cltk.utils import philology

   In [2]: iliad = '~/cltk_data/greek/text/tlg/individual_works/TLG0012.TXT-001.txt'

   In [3]: philology.write_concordance_from_file(iliad, 'iliad')


This will print a traditional, human–readable 120,000–line concordance at ``~/cltk_data/user_data/concordance_iliad.txt``.

Multiple files can be passed as a list into this method.

.. code-block:: python

   In [5]: odyssey = '~/cltk_data/greek/text/tlg/individual_works/TLG0012.TXT-002.txt'

   In [6]: philology.write_concordance_from_file([iliad, odyssey], 'homer')

This creates the file ``~/cltk_data/user_data/concordance_homer.txt``.

``write_concordance_from_string()`` takes a string and will build the concordance from it.


.. code-block:: python

   In [7]: from cltk.corpus.utils.formatter import phi5_plaintext_cleanup

   In [8]: import os

   In [9]: tibullus = os.path.expanduser('~/cltk_data/latin/text/phi5/plaintext/LAT0660.TXT')

   In [10]: with open(tibullus) as f:
   ....:     tib_read = f.read()

   In [10]: tib_clean = phi5_plaintext_cleanup(tib_read).lower()

   In [11]: philology.write_concordance_from_string(tib_clean, 'tibullus')

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

The CLTK uses languages in its organization of data, however some good corpora do not and cannot be easily broken apart. Furthermore, some, such as parallel text corpora, are inherently multilingual. Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``multilingual_``) to discover available multilingual corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('multilingual')

   In [3]: c.list_corpora
   Out[3]: ['multilingual_treebank_proiel']


Information Retrieval (regex, keyword expansion)
================================================

.. tip::

   To begin working with regular expressions, try `Pythex <http://pythex.org/>`_, a handy tool for developing patterns. For more thorough lessons, try `Learn Regex The Hard Way <http://regex.learncodethehardway.org/book/>`_.

.. tip::

   Read about `Word2Vec for Latin <http://docs.cltk.org/en/latest/latin.html#word2vec>`_ or `Greek <http://docs.cltk.org/en/latest/greek.html#word2vec>`_ for the powerful keyword expansion functionality.

Several functions are available for querying text in order to match regular expression patterns. ``match_regex()`` is the most basic. Punctuation rules are included for texts using Latin sentence–final punctuation ('.', '!', '?') and Greek ('.', ';'). For returned strings, you may choose between a context of the match's sentence, paragraph, or custom number of characters on each side of a hit. Note that this function and the next each return a generator.

Here is an example in Latin with a sentence context, case-insensitive:

.. code-block:: python

   In [1]: from cltk.ir.query import match_regex

   In [2]: text = 'Ita fac, mi Lucili; vindica te tibi. et tempus, quod adhuc aut auferebatur aut subripiebatur aut excidebat, collige et serva.'

   In [3]: matches = match_regex(text, r'tempus', language='latin', context='sentence', case_insensitive=True)

   In [4]: for match in matches:
       print(match)
      ...:
   et *tempus*, quod adhuc aut auferebatur aut subripiebatur aut excidebat, collige et serva.


And here with context of 40 characters:

.. code-block:: python

   In [5]: matches = match_regex(text, r'tempus', language='latin', context=40, case_insensitive=True)

   In [6]: for match in matches:
       print(match)
      ...:
   Ita fac, mi Lucili; vindica te tibi. et *tempus*, quod adhuc aut auferebatur aut subripi

For querying the entirety of a corpus, see ``search_corpus()``, which returns a tuple of ``('author_name': 'match_context')``.

.. code-block:: python

   In [7]: from cltk.ir.query import search_corpus

   In [8]: for match in search_corpus('ὦ ἄνδρες Ἀθηναῖοι', 'tlg', context='sentence'):
       print(match)
      ...:
   ('Ammonius Phil.', ' \nκαλοῦντας ἑτέρους ἢ προστάσσοντας ἢ ἐρωτῶντας ἢ εὐχομένους περί τινων, \nπολλάκις δὲ καὶ αὐτοπροσώπως κατά τινας τῶν ἐνεργειῶν τούτων ἐνεργοῦ-\nσι “πρῶτον μέν, *ὦ ἄνδρες Ἀθηναῖοι*, τοῖς θεοῖς εὔχομαι πᾶσι καὶ πάσαις” \nλέγοντες ἢ “ἀπόκριναι γὰρ δεῦρό μοι ἀναστάς”. οἱ οὖν περὶ τῶν τεχνῶν \nτούτων πραγματευόμενοι καὶ τοὺς λόγους εἰς θεωρίαν ')
   ('Sopater Rhet.', "θόντα, ἢ συγγνωμονηκέναι καὶ ἐλεῆσαι. ψυχῆς γὰρ \nπάθος ἐπὶ συγγνώμῃ προτείνεται. παθητικὴν οὖν ποιή-\nσῃ τοῦ πρώτου προοιμίου τὴν ἔννοιαν: ἁπάντων, ὡς ἔοι-\nκεν, *ὦ ἄνδρες Ἀθηναῖοι*, πειρασθῆναί με τῶν παραδό-\nξων ἀπέκειτο, πόλιν ἰδεῖν ἐν μέσῃ Βοιωτίᾳ κειμένην. καὶ \nμετὰ Θήβας οὐκ ἔτ' οὔσας, ὅτι μὴ στεφανοῦντας Ἀθη-\nναίους ἀπέδειξα παρὰ τὴ")
   …


Information Retrieval (boolean)
===============================

.. note::

   The API for the CLTK index and query will likely change. Consider this module an alpha. Please `report improvements or problems <https://github.com/cltk/cltk/issues>`_.

An index to a corpus allows for faster, and sometimes more nuanced, searches. The CLTK has built some indexing and querying \
functionality with the `Whoosh library <https://pythonhosted.org/Whoosh/index.html>`_. The following show how to make \
an index and then query it:

First, ensure that you have `imported and converted the PHI5 or TLG disks <http://docs.cltk.org/en/latest/greek.html#converting-tlg-texts-with-tlgu>`_ imported. \
If you want to use the author chunking, convert with ``convert_corpus()``, but for searching by work, convert with ``divide_works()``. ``CLTKIndex()`` has an optional argument ``chunk``, which defaults to ``chunk='author'``. ``chunk='work'`` is also available.

An index only needs to be made once. Then it can be queried with, e.g.:

.. code-block:: python

   In [1]: from cltk.ir.boolean import CLTKIndex

   In [2]: cltk_index = CLTKIndex('latin', 'phi5', chunk='work')

   In [3]: results = cltk_index.corpus_query('amicitia')

   In [4]: results[:500]
   Out[4]: 'Docs containing hits: 836.</br></br>Marcus Tullius Cicero, Cicero, Tully</br>/Users/kyle/cltk_data/latin/text/phi5/individual_works/LAT0474.TXT-052.TXT</br>Approximate hits: 132.</br>LAELIUS DE <b class="match term0">AMICITIA</b> LIBER </br>        AD T. POMPONIUM ATTICUM.} </br>    Q. Mucius augur multa narrare...incidisset, exposuit </br>nobis sermonem Laeli de <b class="match term1">amicitia</b> habitum ab illo </br>secum et cum altero genero, C. Fannio...videretur. </br>    Cum enim saepe me'

The function returns an string in HTML markup, which you can then parse yourself.

To save results, use the ``save_file`` parameter:

.. code-block:: python

 In [4]: cltk_index.corpus_query('amicitia', save_file='2016_amicitia')

This will save a file at ``~/cltk_data/user_data/search/2016_amicitia.html``, being a human-readable output \
with word-matches highlighted, of all authors (or texts, if ``chunk='work'``).


Lemmatization, backoff and others
=================================

CLTK offers 'multiplex' lemmatization, i.e. a series of lexicon-, rules-, or training data-based lemmatizers that can be chained together. The multiplex lemmatizers are based on backoff POS tagging in NLTK: 1. with Backoff lemmatization, tagging stops at the first successful instance of tagging by a sub-tagger; 2.  with Ensemble lemmatization, tagging continues through the entire sequence, all possible lemmas are returned, and a method for scoring/selecting from possible lemmas can be specified. All of the examples below are in Latin, but these lemmatizers are language-independent (at least, where lemmatization is a meaningful NLP task) and can be made language-specific by providing different training sentences, regex patterns, etc.

The backoff module offers DefaultLemmatizer which returns the same "lemma" for all tokens:

.. code-block:: python

   In [1]: from cltk.lemmatize.backoff import DefaultLemmatizer

   In [2]: lemmatizer = DefaultLemmatizer()

   In [3]: tokens = ['Quo', 'usque', 'tandem', 'abutere', ',', 'Catilina', ',', 'patientia', 'nostra', '?']

   In [4]: lemmatizer.lemmatize(tokens)
   Out[4]: [('Quo', None), ('usque', None), ('tandem', None), ('abutere', None), (',', None), ('Catilina', None), (',', None), ('patientia', None), ('nostra', None), ('?', None)]

DefaultLemmatizer can take as a parameter what "lemma" should be returned:

.. code-block:: python

   In [5]: lemmatizer = DefaultLemmatizer('UNK')

   In [6]: lemmatizer.lemmatize(tokens)
   Out[6]: [('Quo', 'UNK'), ('usque', 'UNK'), ('tandem', 'UNK'), ('abutere', 'UNK'), (',', 'UNK'), ('Catilina', 'UNK'), (',', 'UNK'), ('patientia', 'UNK'), ('nostra', 'UNK'), ('?', 'UNK')]

The backoff module also offers IdentityLemmatizer which returns the given token as the lemma:

.. code-block:: python

   In [7]: from cltk.lemmatize.backoff import IdentityLemmatizer

   In [8]: lemmatizer = IdentityLemmatizer()

   In [9]: lemmatizer.lemmatize(tokens)
   Out[9]: [('Quo', 'Quo'), ('usque', 'usque'), ('tandem', 'tandem'), ('abutere', 'abutere'), (',', ','), ('Catilina', 'Catilina'), (',', ','), ('patientia', 'patientia'), ('nostra', 'nostra'), ('?', '?')]

With the DictLemmatizer, the backoff module allows you to provide a dictionary of the form {'TOKEN1': 'LEMMA1', 'TOKEN2': 'LEMMA2'} for lemmatization.

.. code-block:: python

   In [10]: tokens = ['arma', 'uirum', '-que', 'cano', ',', 'troiae', 'qui', 'primus', 'ab', 'oris']

   In [11]: lemmas = {'arma': 'arma', 'uirum': 'uir', 'troiae': 'troia', 'oris': 'ora'}

   In [12]: from cltk.lemmatize.backoff import DictLemmatizer

   In [13]: lemmatizer = DictLemmatizer(lemmas=lemmas)

   In [14]: lemmatizer.lemmatize(tokens)
   Out[14]: [('arma', 'arma'), ('uirum', 'uir'), ('-que', None), ('cano', None), (',', None), ('troiae', 'troia'), ('qui', None), ('primus', None), ('ab', None), ('oris', 'ora')]

The DictLemmatizer—like all of the lemmatizers in this module—can take a second lemmatizer (or backoff lemmatizer) for any of the tokens that return 'None'. This is done with a 'backoff' parameter:

.. code-block:: python

   In [15]: default = DefaultLemmatizer('UNK')

   In [16]: lemmatizer = DictLemmatizer(lemmas=lemmas, backoff=default)

   In [17]: lemmatizer.lemmatize(tokens)
   Out[17]: [('arma', 'arma'), ('uirum', 'uir'), ('-que', 'UNK'), ('cano', 'UNK'), (',', 'UNK'), ('troiae', 'troia'), ('qui', 'UNK'), ('primus', 'UNK'), ('ab', 'UNK'), ('oris', 'ora')]

These lemmatizers also have a verbose mode that returns the specific tagger used for each lemma returned.

.. code-block:: python

   In [18]: default = DefaultLemmatizer('UNK', verbose=True)

   In [19]: lemmatizer = DictLemmatizer(lemmas=lemmas, backoff=default, verbose=True)

   In [20]: lemmatizer.lemmatize(tokens)
   Out[20]: [('arma', 'arma', "<DictLemmatizer: {'arma': 'arma', ...}>"), ('uirum', 'uir', "<DictLemmatizer: {'arma': 'arma', ...}>"), ('-que', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), ('cano', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), (',', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), ('troiae', 'troia', "<DictLemmatizer: {'arma': 'arma', ...}>"), ('qui', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), ('primus', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), ('ab', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), ('oris', 'ora', "<DictLemmatizer: {'arma': 'arma', ...}>")]

You can provide a name for the data source to make the verbose output clearer:

.. code-block:: python

   In [21]: default = DefaultLemmatizer('UNK')

   In [22]: lemmatizer = DictLemmatizer(lemmas=lemmas, source="CLTK Docs Example", backoff=default, verbose=True)

   In [23]: lemmatizer.lemmatize(tokens)
   Out[23]: [('arma', 'arma', '<DictLemmatizer: CLTK Docs Example>'), ('uirum', 'uir', '<DictLemmatizer: CLTK Docs Example>'), ('-que', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), ('cano', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), (',', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), ('troiae', 'troia', '<DictLemmatizer: CLTK Docs Example>'), ('qui', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), ('primus', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), ('ab', 'UNK', '<DefaultLemmatizer: lemma=UNK>'), ('oris', 'ora', '<DictLemmatizer: CLTK Docs Example>')]

With the UnigramLemmatizer, the backoff module allows you to provide a list of lists of sentences of the form `[[('TOKEN1', 'LEMMA1'), ('TOKEN2', 'LEMMA2')], [('TOKEN3', 'LEMMA3'), ('TOKEN4', 'LEMMA4')], ... ]` for lemmatization. The lemmatizer returns the the lemma that has the highest frequency based on the training sentences. So, for example, if the tuple ('est', 'sum') appears in the training sentences 99 times and ('est', 'edo') appears 1 time, the lemmatizer would return the lemma 'sum'.

Here is an example of the UnigramLemmatizer():

.. code-block:: python

   In [24]: train_data = [[('cum', 'cum2'), ('esset', 'sum'), ('caesar', 'caesar'), ('in', 'in'), ('citeriore', 'citer'), ('gallia', 'gallia'), ('in', 'in'), ('hibernis', 'hibernus'), (',', 'punc'), ('ita', 'ita'), ('uti', 'ut'), ('supra', 'supra'), ('demonstrauimus', 'demonstro'), (',', 'punc'), ('crebri', 'creber'), ('ad', 'ad'), ('eum', 'is'), ('rumores', 'rumor'), ('adferebantur', 'affero'), ('litteris', 'littera'), ('-que', '-que'), ('item', 'item'), ('labieni', 'labienus'), ('certior', 'certus'), ('fiebat', 'fio'), ('omnes', 'omnis'), ('belgas', 'belgae'), (',', 'punc'), ('quam', 'qui'), ('tertiam', 'tertius'), ('esse', 'sum'), ('galliae', 'gallia'), ('partem', 'pars'), ('dixeramus', 'dico'), (',', 'punc'), ('contra', 'contra'), ('populum', 'populus'), ('romanum', 'romanus'), ('coniurare', 'coniuro'), ('obsides', 'obses'), ('-que', '-que'), ('inter', 'inter'), ('se', 'sui'), ('dare', 'do'), ('.', 'punc')], [('coniurandi', 'coniuro'), ('has', 'hic'), ('esse', 'sum'), ('causas', 'causa'), ('primum', 'primus'), ('quod', 'quod'), ('uererentur', 'uereor'), ('ne', 'ne'), (',', 'punc'), ('omni', 'omnis'), ('pacata', 'paco'), ('gallia', 'gallia'), (',', 'punc'), ('ad', 'ad'), ('eos', 'is'), ('exercitus', 'exercitus'), ('noster', 'noster'), ('adduceretur', 'adduco'), (';', 'punc')]]

   In [25]: default = DefaultLemmatizer('UNK')

   In [26]: lemmatizer = UnigramLemmatizer(train_sents, backoff=default)

   In [27]: lemmatizer.lemmatize(tokens)
   Out[27]: [('arma', 'UNK'), ('uirum', 'UNK'), ('-que', '-que'), ('cano', 'UNK'), (',', 'punc'), ('troiae', 'UNK'), ('qui', 'UNK'), ('primus', 'UNK'), ('ab', 'UNK'), ('oris', 'UNK')]

There is also a regular-expression based lemmatizer that uses a tuple with substitution patterns to return lemmas:

  In [28]: regexps = [ ('(.)tat(is|i|em|e|es|um|ibus)$', r'\1tas'), ('(.)ion(is|i|em|e|es|um|ibus)$', r'\1io'), ('(.)av(i|isti|it|imus|istis|erunt|)$', r'\1o'),]

  In [29]: tokens = "iam a principio nobilitatis factionem disturbavit".split()

  In [30]: from cltk.lemmatize.backoff import RegexpLemmatizer

  In [31]: lemmatizer = RegexpLemmatizer(regexps=regexps)

  In [32]: lemmatizer.lemmatize(tokens)
  Out[32]: [('iam', None), ('a', None), ('principio', None), ('nobilitatis', 'nobilitas'), ('factionem', 'factio'), ('disturbavit', 'disturbo')]

Ensemble lemmatization are constructed in a similar manner, but all sub-lemmatizers return tags. A selection mechanism can be applied to the output. (NB: Selection and scoring mechanisms for use with the Ensemble Lemmatizer are under development.)

  In [33]: from cltk.lemmatize.ensemble import EnsembleDictLemmatizer, EnsembleUnigramLemmatizer, EnsembleRegexpLemmatizer

  In [34]: patterns = [(r'\b(.+)(o|is|it|imus|itis|unt)\b', r'\1o'), (r'\b(.+)(o|as|at|amus|atis|ant)\b', r'\1o'),]

  In [35]: tokens = "arma virumque cano qui".split()

  In [36]: EDL = EnsembleDictLemmatizer(lemmas = {'cano': 'cano'}, source='EDL', verbose=True)

  In [37]: EUL = EnsembleUnigramLemmatizer(train=[[('arma', 'arma'), ('virumque', 'vir'), ('cano', 'cano')], [('arma', 'arma'), ('virumque', 'virus'), ('cano', 'canus')], [('arma', 'arma'), ('virumque', 'vir'), ('cano', 'canis')], [('arma', 'arma'), ('virumque', 'vir'), ('cano', 'cano')],], verbose=True, backoff=EDL)

  In [38]: ERL = EnsembleRegexpLemmatizer(regexps=patterns, source='Latin Regex Patterns', verbose=True, backoff=EUL)

  In [39]: ERL.lemmatize(test, lemmas_only=True)
  Out[39]: [['arma'], ['vir', 'virus'], ['canis', 'cano', 'canus'], []]

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


Normalization
=============

If you are working from texts from different resources, it is likely a good idea to normalize them before
further processing (such as sting comparison). The CLTK provides a wrapper to the Python language's builtin \
``normalize()``. Here's an example its use in "compatibility" mode (``NFKC``):

.. code-block:: python

   In [1]: from cltk.corpus.utils.formatter import cltk_normalize

   In [2]: tonos = "ά"

   In [3]: oxia = "ά"

   In [4]: tonos == oxia
   Out[4]: False

   In [5]: tonos == cltk_normalize(oxia)
   Out[5]: True


One can turn off compatibility with:

.. code-block:: python

   In [6]: tonos == cltk_normalize(oxia, compatibility=False)
   Out[6]: True

For more on ``normalize()`` see the `Python Unicode docs <https://docs.python.org/3.5/library/unicodedata.html#unicodedata.normalize>`_.



Skipgrams
=========
The NLTK has a handy `skipgram <https://en.wikipedia.org/wiki/N-gram#Skip-gram>`_ function. Use it like this:

.. code-block:: python

   In [1]: from cltk.tokenize.word import WordTokenizer

   In [2]: from nltk.util import skipgrams

   In [3]: text = 'T. Pomponis Atticus, ab origine ultima stirpis Romanae generatus, \
      ...:    perpetuo a maioribus acceptam equestrem obtinuit dignitatem.'

   In [4]: word_tokenizer = WordTokenizer('latin')

   In [5]: unigrams = word_tokenizer.tokenize(text)

   In [6]: for ngram in skipgrams(unigrams, 3, 5):
      ...:     print(ngram)
      ...:
   ('T.', 'Pomponis', 'Atticus')
   ('T.', 'Pomponis', ',')
   ('T.', 'Pomponis', 'ab')
   ('T.', 'Pomponis', 'origine')
   ('T.', 'Pomponis', 'ultima')
   ('T.', 'Pomponis', 'stirpis')
   ('T.', 'Atticus', ',')
   ('T.', 'Atticus', 'ab')
   ('T.', 'Atticus', 'origine')
   ('T.', 'Atticus', 'ultima')
   …
   ('equestrem', 'obtinuit', '.')
   ('equestrem', 'dignitatem', '.')
   ('obtinuit', 'dignitatem', '.')

The first parameter is the length of the output n-gram and the second parameter is how many tokens to skip.

The NLTK's ``skipgrams()`` produces a generator whose values can be turned into a list like so:

.. code-block:: python

   In [8]: list(skipgrams(unigrams, 3, 5))
   Out[8]:
   [('T.', 'Pomponis', 'Atticus'),
    ('T.', 'Pomponis', ','),
    ('T.', 'Pomponis', 'ab'),
    …
    ('equestrem', 'dignitatem', '.'),
    ('obtinuit', 'dignitatem', '.')]


Stoplist Construction
=====================

The ``Stop`` module offers an abstract class for constructing stoplists: ``BaseCorpusStoplist``.

Children class must implement ``vectorizer`` and ``tfidf_vectorizer``. Fow now, only Latin and Classical Chinese
with ``CorpusStoplist``have implemented a child class of ``BaseCorpusStoplist``.

Parameters like the size of the stoplist, the criterion on which you get the stop list with a parameter (``basis``) for weighting words within the collection using different measures. The bases currently available are: ``frequency``, ``mean`` (mean probability), ``variance`` (variance probability), ``entropy`` (entropy), and ``zou`` (a composite measure based on mean, variance, and entropy as described in [Zou 2006]).
Other parameters for both ``StringStoplist`` and ``CorpusStoplist`` include boolean preprocessing options (``lower``, ``remove_numbers``, ``remove_punctuation``) and override lists of words to add or subtract from stoplists (``include``, ``exclude``).

Syllabification
===============

CLTK provides a language-agnostic syllabifier module as part of ``phonology``. The syllabifier works by following the Sonority Sequencing Principle. The default phonetic scale (from most to least sonorous):

**low vowels > mid vowels > high vowels > flaps > laterals > nasals > fricatives > plosives**


.. code-block:: python

   In [1]: from cltk.phonology import syllabify

   In [2]: high_vowels = ['a']

   In [3]: mid_vowels = ['e']

   In [4]: low_vowels = ['i', 'u']

   In [5]: flaps = ['r']

   In [6]: nasals = ['m', 'n']

   In [7]: fricatives = ['f']

   In [8]: s = Syllabifier(high_vowels=high_vowels, mid_vowels=mid_vowels, low_vowels=low_vowels, flaps=flaps, nasals=nasals, fricatives=fricatives)

   In [9]: s.syllabify("feminarum")
   Out[9]: ['fe', 'mi', 'na', 'rum']

Additionally, you can override the default sonority hierarchy by calling ``set_hierarchy``. However, you must also re-define the
vowel list for the nuclei to be correctly identified.

.. code-block:: python

   In [10]: s = Syllabifier()

   In [11]: s.set_hierarchy([['i', 'u'], ['e'], ['a'], ['r'], ['m', 'n'], ['f']])

   In [12]: s.set_vowels(['i', 'u', 'e', 'a'])

   In [13]: s.syllabify('feminarum')
   Out[13]: ['fe', 'mi', 'na', 'rum']

For a language-dependent approach, you can call the predefined sonority dictionary by toogling the ``language`` parameter:

.. code-block:: python

   In [14]: s = Syllabifier(language='middle high german')

   In [15]: s.syllabify('lobebæren')
   Out[15]: ['lo', 'be', 'bæ', 'ren']

Text Reuse
==========
The text reuse module offers a few tools to get started with studying text reuse (i.e., allusion and intertext). The major goals of this module are to leverage conventional text reuse strategies and to create comparison methods designed specifically for the languages of the corpora included in the CLTK.

This module is under active development, so if you experience a bug or have a suggestion for something to include, please create an issue on GitHub.

Levenshtein distance calculation
--------------------------------

+.. note::
+
+   You will need to install two packages to use Levenshtein measures. Install them with `pip install fuzzywuzzy python-Levenshtein`. `python-Levenshtein` is optional but gives speed improvements.

The Levenshtein distance comparison is a commonly-used method for fuzzy string comparison.  The CLTK Levenshtein class offers a few helps for getting started with creating comparisons from document.

This simple example compares a line from Vergil's Georgics with a line from Propertius (Elegies III.13.41):

.. code-block:: python

   In [1]: from cltk.text_reuse.levenshtein import Levenshtein

   In [2]: l = Levenshtein()

   In [3]: l.ratio("dique deaeque omnes, studium quibus arua tueri,", "dique deaeque omnes, quibus est tutela per agros,")
   Out[3]: 0.71

You can also calculate the Levenshtein distance of two words, defined as the minimum number of single word edits (insertions, deletions, substitutions) required to transform a word into another.

.. code-block:: python

   In [4]: l.levenshtein_distance("deaeque", "deaeuqe")
   Out[4]: 2


Damerau-Levenshtein algorithm
-----------------------------

.. note::

   You will need to install `pyxDamerauLevenshtein <https://github.com/gfairchild/pyxDamerauLevenshtein>`_ to use these features.

The Damerau-Levenshtein algorithm is used for finding the distance metric between any two strings i.e., finite number of symbols or letters between any two strings. The Damerau-Levenshtein algorithm is an enhancement over Levenshtein algorithm in the sense that it allows for transposition operations.

This simple example compares a two Latin words to find the distance between them:

.. code-block:: python

   In [1]: from pyxdameraulevenshtein import damerau_levenshtein_distance

   In [2]: damerau_levenshtein_distance("deaeque", "deaque")
   Out[2]: 1

Alternatively, you can also use CLTK's native ``Levenshtein`` class:

.. code-block:: python

   In [3]: from cltk.text_reuse.levenshtein import Levenshtein

   In [4]: Levenshtein.damerau_levenshtein_distance("deaeque", "deaque")
   Out[4]: 1

   In [5]: Levenshtein.damerau_levenshtein_distance("deaeque", "deaeuqe")
   Out[5]: 1

Needleman-Wunsch Algorithm
--------------------------

The Needleman-Wunsch Algorithm, calculates the optimal global alignment between two strings given a scoring matrix.

There are two optional parameters: ``S`` specifying a weighted similarity square matrix, and ``alphabet`` (where ``|alphabet| = rows(S) = cols(S)``). By default, the algorithm assumes the latin alphabet and a default matrix (1 for match, -1 for substitution)

.. code-block:: python

   In [1]: from cltk.text_reuse.comparison import Needleman_Wunsch as NW

   In [2]: NW("abba", "ababa", alphabet = "ab", S = [[1, -3],[-3, 1]])
   Out[2]: ('ab-ba', 'ababa')

In this case, the similarity matrix will be:

+---+---+---+
|   | a | b |
+---+---+---+
| a | 1 |-3 |
+---+---+---+
| b |-3 | 1 |
+---+---+---+


Longest Common Substring
------------------------

Longest Common Substring takes two strings as an argument to the function and returns a substring which is common between both the
strings. The example below compares a line from Vergil's Georgics with a line from Propertius (Elegies III.13.41):

.. code-block:: python

   In [1]: from cltk.text_reuse.comparison import long_substring

   In [2]: print(long_substring("dique deaeque omnes, studium quibus arua tueri,", "dique deaeque omnes, quibus est tutela per agros,"))
   Out[2]: dique deaque omnes,


MinHash
-------
The MinHash algorithm  generates a score based on the similarity of the two strings. It takes two strings as a parameter to the  function and returns a float.

.. code-block:: python

   In [1]: from cltk.text_reuse.comparison import minhash

   In [2]: a = 'dique deaeque omnes, studium quibus arua tueri,'

   In [3]: b = 'dique deaeque omnes, quibus est tutela per agros,'

   In[3]: print(minhash(a,b))
   Out[3]:0.171631205673


Treebank label dict
===================

You can generate nested Python dict from a treebank in string format. Currently, only treebanks following the Penn notation are supported.

.. code-block:: python

   In [1]: from  cltk.tags.treebanks import parse_treebanks

   In [2]: st = "((IP-MAT-SPE (' ') (INTJ Yes) (, ,) (' ') (IP-MAT-PRN (NP-SBJ (PRO he)) (VBD seyde)) (, ,) (' ') (NP-SBJ (PRO I)) (MD shall)	(VB promyse) (NP-OB2 (PRO you)) (IP-INF (TO to)	(VB fullfylle) (NP-OB1 (PRO$ youre) (N desyre))) (. .) (' '))"

   In [3]: treebank = parse_treebanks(st)

   In [4]: treebank['IP-MAT-SPE']['INTJ']
   Out[4]: ['Yes']

   In [5]: treebank
   Out[5]: {'IP-MAT-SPE': {"'": ["'", "'", "'"], 'INTJ': ['Yes'], ',': [',', ','], 'IP-MAT-PRN': {'NP-SBJ': {'PRO': ['he']}, 'VBD': ['seyde']}, 'NP-SBJ': {'PRO': ['I']}, 'MD': ['shall'], '\t': {'VB': ['promyse'], 'NP-OB2': {'PRO': ['you']}, 'IP-INF': {'TO': ['to'], '\t': {'VB': ['fullfylle'], 'NP-OB1': {'PRO$': ['youre'], 'N': ['desyre']}}, '.': ['.'], "'": ["'"]}}}}


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



Word frequency lists
====================

The CLTK has a module which finds word frequency. The export is a ``Counter`` type of dictionary.

.. code-block:: python

   In [1]: from cltk.utils.frequency import Frequency

   In [2]: from cltk.corpus.utils.formatter import tlg_plaintext_cleanup

   In [3]: import os

   In [4]: freq = Frequency()

   In [6]: file = os.path.expanduser('~/cltk_data/greek/text/tlg/plaintext/TLG0012.TXT')

   In [7]: with open(file) as f:
   ...:     text = f.read().lower()
   ...:

   In [8]: text = tlg_plaintext_cleanup(text)

   In [9]: freq.counter_from_str(text)
   Out[9]: Counter({'δ': 6507, 'καὶ': 4799, 'δὲ': 3194, 'τε': 2645, 'μὲν': 1628, 'ἐν': 1420, 'δέ': 1267, 'ὣς': 1203, 'οἱ': 1126, 'τ': 1101, 'γὰρ': 969, 'ἀλλ': 936, 'τὸν': 904, 'ἐπὶ': 830, 'τοι': 772, 'αὐτὰρ': 761, 'δὴ': 748, 'μοι': 745, 'μιν': 645, 'γε': 632, 'ἐπεὶ': 611, 'ἄρ': 603, 'ἦ': 598, 'νῦν': 581, 'ἄρα': 576, 'κατὰ': 572, 'ἐς': 571, 'ἐκ': 554, 'ἐνὶ': 544, 'ὡς': 541, 'ὃ': 533, 'οὐ': 530, 'οἳ': 527, 'περ': 491, 'τις': 491, 'οὐδ': 482, 'καί': 481, 'οὔ': 476, 'γάρ': 435, 'κεν': 407, 'τι': 407, 'γ': 406, 'ἐγὼ': 404, 'ἐπ': 397, … })

If you have access to the TLG or PHI5 disc, and have already imported it and converted it with the CLTK, you can build your own custom lists off of that.

.. code-block:: python

   In [11]: freq.make_list_from_corpus('phi5', 200, save=False)  # or 'phi5'; both take a while to run
   Out[11]: Counter({',': 749396, 'et': 196410, 'in': 141035, 'non': 89836, 'est': 86472, ':': 76915, 'ut': 70516, ';': 69901, 'cum': 61454, 'si': 59578, 'ad': 59248, 'quod': 52896, 'qui': 46385, 'sed': 41546, '?': 40717, 'quae': 38085, 'ex': 36996, 'quam': 34431, "'": 33596, 'de': 31331, 'esse': 31066, 'aut': 30568, 'a': 29871, 'hoc': 26266, 'nec': 26027, 'etiam': 22540, 'se': 22486, 'enim': 22104, 'ab': 21336, 'quid': 21269, 'per': 20981, 'atque': 20201, 'sunt': 20025, 'sit': 19123, 'autem': 18853, 'id': 18846, 'quo': 18204, 'me': 17713, 'ne': 17265, 'ac': 17007, 'te': 16880, 'nam': 16640, 'tamen': 15560, 'eius': 15306, 'haec': 15080, 'ita': 14752, 'iam': 14532, 'mihi': 14440, 'neque': 13833, 'eo': 13125, 'quidem': 13063, 'est.': 12767, 'quoque': 12561, 'ea': 12389, 'pro': 12259, 'uel': 11824, 'quia': 11518, 'tibi': 11493, … })


Word tokenization
=================

The CLTK wraps one of the NLTK's tokenizers (``TreebankWordTokenizer``), which with the ``multilingual`` parameter works for most languages that use Latin-style whitespace and punctuation to indicate word division. There are some language-specific tokenizers, too, which do extra work to subdivide words when they are combined into one string (e.g., "armaque" in Latin). See ``WordTokenizer.available_languages`` for supported languages for such sub-string tokenization.

.. code-block:: python

   In [1]: from cltk.tokenize.word import WordTokenizer

   In [2]: tok.available_languages
   Out[2]:
   ['akkadian',
    'arabic',
    'french',
    'greek',
    'latin',
    'middle_english',
    'middle_french',
    'middle_high_german',
    'old_french',
    'old_norse',
    'sanskrit',
    'multilingual']

   In [3]: luke_ocs = "рєчє жє притъчѫ к н҄имъ глагол҄ѧ чловѣкѹ єтєрѹ богатѹ ѹгобьѕи сѧ н҄ива"

   In [4]: tok = WordTokenizer(language='multilingual')

   In [5]: tok.tokenize(luke_ocs)
   Out[5]:
   ['рєчє',
    'жє',
    'притъчѫ',
    'к',
    'н҄имъ',
    'глагол҄ѧ',
    'чловѣкѹ',
    'єтєрѹ',
    'богатѹ',
    'ѹгобьѕи',
    'сѧ',
    'н҄ива']

If this default does not work for your texts, consider the NLTK's ``RegexpTokenizer``, which splits on a regular expression patterns of your choosing. Here, for instance, on whitespace and punctuation:

.. code-block:: python

   In [6]: from nltk.tokenize import RegexpTokenizer

   In [7]: word_toker = RegexpTokenizer(r'\w+')

   In [8]: word_toker.tokenize(luke_ocs)
   Out[8]:
   ['рєчє',
    'жє',
    'притъчѫ',
    'к',
    'н',
    'имъ',
    'глагол',
    'ѧ',
    'чловѣкѹ',
    'єтєрѹ',
    'богатѹ',
    'ѹгобьѕи',
    'сѧ',
    'н',
    'ива']
