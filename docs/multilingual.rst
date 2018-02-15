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

The CLTK uses languages in its organization of data, however some good corpora do not and cannot be easily broken apart. Furthermore, some, such as parallel text corpora, are inherently multilingual. Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``multilingual_``) to discover available multilingual corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('multilingual')

   In [3]: c.list_corpora
   Out[3]: ['multilingual_treebank_proiel']


Information Retrieval (regex, keyword expansion)
=============================

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

The ``Stop`` module offers two classes for constructing stoplists: ``StringStoplist`` and ``CorpusStoplist``.

``StringStoplist`` outputs a list of high frequency words from a string. The default size is 100 and can be set with the parameter ``size``.

.. code-block:: python

    In [1]: from cltk.stop.stop import StringStoplist
    
    In [2]: para = """cogitanti mihi saepe numero et memoria vetera repetenti perbeati fuisse, quinte frater, illi videri solent, qui in optima re publica, cum et honoribus et rerum gestarum gloria florerent, eum vitae cursum tenere potuerunt, ut vel in negotio sine periculo vel in otio cum dignitate esse possent; ac fuit cum mihi quoque initium requiescendi atque animum ad utriusque nostrum praeclara studia referendi fore iustum et prope ab omnibus concessum arbitrarer, si infinitus forensium rerum labor et ambitionis occupatio decursu honorum, etiam aetatis flexu constitisset. quam spem cogitationum et consiliorum meorum cum graves communium temporum tum varii nostri casus fefellerunt; nam qui locus quietis et tranquillitatis plenissimus fore videbatur, in eo maximae moles molestiarum et turbulentissimae tempestates exstiterunt; neque vero nobis cupientibus atque exoptantibus fructus oti datus est ad eas artis, quibus a pueris dediti fuimus, celebrandas inter nosque recolendas. nam prima aetate incidimus in ipsam perturbationem disciplinae veteris, et consulatu devenimus in medium rerum omnium certamen atque discrimen, et hoc tempus omne post consulatum obiecimus eis fluctibus, qui per nos a communi peste depulsi in nosmet ipsos redundarent. sed tamen in his vel asperitatibus rerum vel angustiis temporis obsequar studiis nostris et quantum mihi vel fraus inimicorum vel causae amicorum vel res publica tribuet oti, ad scribendum potissimum conferam; tibi vero, frater, neque hortanti deero neque roganti, nam neque auctoritate quisquam apud me plus valere te potest neque voluntate."""
    
    In [3]: stoplist = StringStoplist()
    
    In [4]: stops = stoplist.build_stoplist(para, size=100)
    
    In [5]: print(stops)
    Out [5]: ['a', 'ab', 'ac', 'ad', 'aetatis', 'ambitionis', 'animum', 'arbitrarer', 'atque', 'casus', 'cogitanti', 'cogitationum', 'communium', 'concessum', 'consiliorum', 'constitisset', 'cum', 'cursum', 'decursu', 'dignitate', 'eo', 'esse', 'et', 'etiam', 'eum', 'fefellerunt', 'flexu', 'florerent', 'fore', 'forensium', 'frater', 'fuisse', 'fuit', 'gestarum', 'gloria', 'graves', 'honoribus', 'honorum', 'illi', 'in', 'infinitus', 'initium', 'iustum', 'labor', 'locus', 'maximae', 'memoria', 'meorum', 'mihi', 'moles', 'molestiarum', 'nam', 'negotio', 'neque', 'nostri', 'nostrum', 'numero', 'occupatio', 'omnibus', 'optima', 'oti', 'otio', 'perbeati', 'periculo', 'plenissimus', 'possent', 'potuerunt', 'praeclara', 'prope', 'publica', 'quam', 'qui', 'quietis', 'quinte', 'quoque', 're', 'referendi', 'repetenti', 'requiescendi', 'rerum', 'saepe', 'si', 'sine', 'solent', 'spem', 'studia', 'temporum', 'tenere', 'tranquillitatis', 'tum', 'turbulentissimae', 'ut', 'utriusque', 'varii', 'vel', 'vero', 'vetera', 'videbatur', 'videri', 'vitae']

You can include the counts with the ``inc_counts`` parameter:
   
.. code-block:: python

    In [6]: stops = stoplist.build_stoplist(para, size=100)
    
    In [7]: print(stops)
    Out [7]: [('a', 2), ('ab', 1), ('ac', 1), ('ad', 3), ('aetatis', 1), ('ambitionis', 1), ('animum', 1), ('arbitrarer', 1), ('atque', 3), ('casus', 1), ('cogitanti', 1), ('cogitationum', 1), ('communium', 1), ('concessum', 1), ('consiliorum', 1), ('constitisset', 1), ('cum', 4), ('cursum', 1), ('decursu', 1), ('dignitate', 1), ('eo', 1), ('esse', 1), ('et', 11), ('etiam', 1), ('eum', 1), ('fefellerunt', 1), ('flexu', 1), ('florerent', 1), ('fore', 2), ('forensium', 1), ('frater', 2), ('fuisse', 1), ('fuit', 1), ('gestarum', 1), ('gloria', 1), ('graves', 1), ('honoribus', 1), ('honorum', 1), ('illi', 1), ('in', 8), ('infinitus', 1), ('initium', 1), ('iustum', 1), ('labor', 1), ('locus', 1), ('maximae', 1), ('memoria', 1), ('meorum', 1), ('mihi', 3), ('moles', 1), ('molestiarum', 1), ('nam', 3), ('negotio', 1), ('neque', 5), ('nostri', 1), ('nostrum', 1), ('numero', 1), ('occupatio', 1), ('omnibus', 1), ('optima', 1), ('oti', 2), ('otio', 1), ('perbeati', 1), ('periculo', 1), ('plenissimus', 1), ('possent', 1), ('potuerunt', 1), ('praeclara', 1), ('prope', 1), ('publica', 2), ('quam', 1), ('qui', 3), ('quietis', 1), ('quinte', 1), ('quoque', 1), ('re', 1), ('referendi', 1), ('repetenti', 1), ('requiescendi', 1), ('rerum', 4), ('saepe', 1), ('si', 1), ('sine', 1), ('solent', 1), ('spem', 1), ('studia', 1), ('temporum', 1), ('tenere', 1), ('tranquillitatis', 1), ('tum', 1), ('turbulentissimae', 1), ('ut', 1), ('utriusque', 1), ('varii', 1), ('vel', 7), ('vero', 2), ('vetera', 1), ('videbatur', 1), ('videri', 1), ('vitae', 1)]
    
``CorpusStoplist`` outputs a list of stopwords from a collection of documents based, with a parameter (``basis``) for weighting words within the collection using different measures. The bases currently available are: ``frequency``, ``mean`` (mean probability), ``variance`` (variance probability), ``entropy`` (entropy), and ``zou`` (a composite measure based on mean, variance, and entropy as described in [Zou 2006]).
   
.. code-block:: python

    In [8]: from cltk.stop.stop import CorpusStoplist
    
    In [9]: stoplist = CorpusStoplist()
    
    In [10]: para_2 = """ac mihi repetenda est veteris cuiusdam memoriae non sane satis explicata recordatio, sed, ut arbitror, apta ad id, quod requiris, ut cognoscas quae viri omnium eloquentissimi clarissimique senserint de omni ratione dicendi. vis enim, ut mihi saepe dixisti, quoniam, quae pueris aut adulescentulis nobis ex commentariolis nostris incohata ac rudia exciderunt, vix sunt hac aetate digna et hoc usu, quem ex causis, quas diximus, tot tantisque consecuti sumus, aliquid eisdem de rebus politius a nobis perfectiusque proferri; solesque non numquam hac de re a me in disputationibus nostris dissentire, quod ego eruditissimorum hominum artibus eloquentiam contineri statuam, tu autem illam ab elegantia doctrinae segregandam putes et in quodam ingeni atque exercitationis genere ponendam. ac mihi quidem saepe numero in summos homines ac summis ingeniis praeditos intuenti quaerendum esse visum est quid esset cur plures in omnibus rebus quam in dicendo admirabiles exstitissent; nam quocumque te animo et cogitatione converteris, permultos excellentis in quoque genere videbis non mediocrium artium, sed prope maximarum. quis enim est qui, si clarorum hominum scientiam rerum gestarum vel utilitate vel magnitudine metiri velit, non anteponat oratori imperatorem? quis autem dubitet quin belli duces ex hac una civitate praestantissimos paene innumerabilis, in dicendo autem excellentis vix paucos proferre possimus? iam vero consilio ac sapientia qui regere ac gubernare rem publicam possint, multi nostra, plures patrum memoria atque etiam maiorum exstiterunt, cum boni perdiu nulli, vix autem singulis aetatibus singuli tolerabiles oratores invenirentur. ac ne qui forte cum aliis studiis, quae reconditis in artibus atque in quadam varietate litterarum versentur, magis hanc dicendi rationem, quam cum imperatoris laude aut cum boni senatoris prudentia comparandam putet, convertat animum ad ea ipsa artium genera circumspiciatque, qui in eis floruerint quamque multi sint; sic facillime, quanta oratorum sit et semper fuerit paucitas, iudicabit."""
    
    In [11]: corpus = [para, para2]
    
    In [12]: stops = stoplist.build_stoplist(corpus, basis='entropy', size=10)
    
    In [13]: print(stops)
    Out [13]: ['ac', 'ad', 'atque', 'cum', 'et', 'in', 'mihi', 'qui', 'rerum', 'vel']
    
Other parameters for both ``StringStoplist`` and ``CorpusStoplist`` include boolean preprocessing options (``lower``, ``remove_numbers``, ``remove_punctuation``) and override lists of words to add or subtract from stoplists (``include``, ``exclude``).
   
.. code-block:: python

    In [14]: stops = stoplist.build_stoplist(corpus, size=10, basis='frequency', exclude=['ad'])
    
    In [15]: print(stops)
    Out [15]: ['ac', 'atque', 'cum', 'et', 'in', 'mihi', 'neque', 'qui', 'vel']
    
    In [16]: stops = stoplist.build_stoplist(corpus, size=10, basis='frequency', include=['est'])
    
    In [17]: print(stops)
    Out [17]: ['ac', 'ad', 'atque', 'cum', 'est', 'et', 'in', 'mihi', 'neque', 'qui', 'vel']


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


Damerau-Levenshtein algorithm
-----------------------------

.. note::

   You will need to install `pyxDamerauLevenshtein <https://github.com/gfairchild/pyxDamerauLevenshtein>`_ to use these features.
   
The Damerau-Levenshtein algorithm is used for finding the distance metric between any two strings i.e., finite number of symbols or letters between any two strings. The Damerau-Levenshtein algorithm is an enhancement over Levenshtein algorithm in the sense that it allows for transposition operations.

This simple example compares a two Latin words to find the distance between them:

.. code-block:: python

   In [1]: from from pyxdameraulevenshtein import damerau_levenshtein_distance

   In [2]: damerau_levenshtein_distance("deaeque", "deaque")
   Out[2]: 1
   

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

The NLTK offers several methods for word tokenization. The ``PunktLanguageVars`` is its latest tokenizer.

.. code-block:: python

   In [1]: from nltk.tokenize.punkt import PunktLanguageVars

   In [2]: s = """Anna soror, quae me suspensam insomnia terrent! Quis novus hic nostris successit sedibus hospes."""

   In [3]: p = PunktLanguageVars()

   In [4]: p.word_tokenize(s)
   Out[4]:
   ['Anna',
    'soror',
    ',',
    'quae',
    'me',
    'suspensam',
    'insomnia',
    'terrent',
    '!',
    'Quis',
    'novus',
    'hic',
    'nostris',
    'successit',
    'sedibus',
    'hospes.']

This tokenizer works well, though has the particular feature that periods are fixed to the word preceding it. Notice the final token ``hospes.`` in the above. To get around this limitation, the CLTK offers ``nltk_tokenize_words()``, which is a simple wrapper for ``PunktLanguageVars.word_tokenize()``. It identifies final periods and turns them into their own item.

.. code-block:: python

   In [5]: from cltk.tokenize.word import nltk_tokenize_words

   In [6]: nltk_tokenize_words(s)
   Out[6]:
   ['Anna',
    'soror',
    ',',
    'quae',
    'me',
    'suspensam',
    'insomnia',
    'terrent',
    '!',
    'Quis',
    'novus',
    'hic',
    'nostris',
    'successit',
    'sedibus',
    'hospes',
    '.']

If, however, you want the default output of ``PunktLanguageVars.word_tokenize()``, use the argument ``attached_period=True``, as in ``nltk_tokenize_words(s, attached_period=True)``.

If ``PunktLanguageVars`` doesn't suit your tokenization needs, consider another tokenizer from the NLTK, which breaks on any other regular expression pattern you choose. Here, for instance, on whitespace word breaks:

.. code-block:: python

   In [7]: from nltk.tokenize import RegexpTokenizer

   In [8]: word_breaks = RegexpTokenizer(r'\w+')

   In [8]: tokens = word_breaks.tokenize(cleaned)

   In [9]: tokens[:10]
   Out[9]: ['Arma',
    'uirumque',
    'cano',
    'Troiae',
    'qui',
    'primus',
    'ab',
    'oris',
    'Italiam',
    'fato']

