Greek
*****
For most of the following operations, you must first `import the CLTK Greek linguistic data <http://docs.cltk.org/en/latest/importing_corpora.html>`_ (named ``greek_models_cltk``).

Converting Beta Code to Unicode
===============================
Note that incoming strings need to begin with an ``r`` and that the Beta Code must follow immediately after the initial ``"""``, as in input line 2, below.

.. code-block:: python

   In [1]: from cltk.corpus.greek.beta_to_unicode import Replacer

   In [2]: BETA_EXAMPLE = r"""O(/PWS OU)=N MH\ TAU)TO\ PA/QWMEN E)KEI/NOIS, E)PI\ TH\N DIA/GNWSIN AU)TW=N E)/RXESQAI DEI= PRW=TON. TINE\S ME\N OU)=N AU)TW=N EI)SIN A)KRIBEI=S, TINE\S DE\ OU)K A)KRIBEI=S O)/NTES METAPI/-PTOUSIN EI)S TOU\S E)PI\ SH/YEI: OU(/TW GA\R KAI\ LOU=SAI KAI\ QRE/YAI KALW=S KAI\ MH\ LOU=SAI PA/LIN, O(/TE MH\ O)RQW=S DUNHQEI/HMEN."""

   In [3]: r = Replacer()

   In [4]: r.beta_code(BETA_EXAMPLE)
   Out[4]: 'ὅπως οὖν μὴ ταὐτὸ πάθωμεν ἐκείνοις, ἐπὶ τὴν διάγνωσιν αὐτῶν ἔρχεσθαι δεῖ πρῶτον. τινὲς μὲν οὖν αὐτῶν εἰσιν ἀκριβεῖς, τινὲς δὲ οὐκ ἀκριβεῖς ὄντες μεταπίπτουσιν εἰς τοὺς ἐπὶ σήψει· οὕτω γὰρ καὶ λοῦσαι καὶ θρέψαι καλῶς καὶ μὴ λοῦσαι πάλιν, ὅτε μὴ ὀρθῶς δυνηθείημεν.'


Converting TLG texts with TLGU
======================================


The `TLGU <http://tlgu.carmen.gr/>`_ is excellent C language software for converting the TLG and PHI corpora into human-readable Unicode. The CLTK has an automated downloader and installer, as well as a wrapper which facilitates its use. When ``TLGU()`` is instantiated, it checks the local OS for a functioning version of the software. If not found it is, following the user's confirmation, downloaded and installed.

Most users will want to do a bulk conversion of the entirety of a corpus without any text markup (such as chapter or line numbers). Note that you must `import a local corpus <http://docs.cltk.org/en/latest/importing_corpora.html#importing-a-corpus>`_ before converting it.

.. code-block:: python

   In [1]: from cltk.corpus.greek.tlgu import TLGU

   In [2]: t = TLGU()

   In [3]: t.convert_corpus(corpus='tlg')  # writes to: ~/cltk_data/greek/text/tlg/plaintext/


For the PHI7, you may declare whether you want the corpus to be written to the ``greek`` or ``latin`` directories. By default, it writes to ``greek``.

.. code-block:: python

   In [5]: t.convert_corpus(corpus='phi7')  # ~/cltk_data/greek/text/phi7/plaintext/

   In [6]: t.convert_corpus(corpus='phi7', latin=True)  # ~/cltk_data/latin/text/phi7/plaintext/

The above commands take each author file and convert them into a new author file. But the software has a useful option to divide each author file into a new file for each work it contains. Thus, Homer's file, ``TLG0012.TXT``, becomes ``TLG0012.TXT-001.txt``, ``TLG0012.TXT-002.txt``, and ``TLG0012.TXT-003.txt``. To achieve this, use the following command for the ``TLG``:

.. code-block:: python

   In [7]: t.divide_works('tlg')  # ~/cltk_data/greek/text/tlg/individual_works/


You may also convert individual files, with options for how the conversion happens.

.. code-block:: python

   In [3]: t.convert('~/Downloads/corpora/TLG_E/TLG0003.TXT', '~/Documents/thucydides.txt')

   In [4]: t.convert('~/Downloads/corpora/TLG_E/TLG0003.TXT', '~/Documents/thucydides.txt', markup='full')

   In [5]: t.convert('~/Downloads/corpora/TLG_E/TLG0003.TXT', '~/Documents/thucydides.txt', break_lines=True)

   In [6]: t.convert('~/Downloads/corpora/TLG_E/TLG0003.TXT', '~/Documents/thucydides.txt', divide_works=True)


For ``convert()``, plain arguments may be sent directly to the ``TLGU``, as well, via ``extra_args``:

.. code-block:: python

   In [7]: t.convert('~/Downloads/corpora/TLG_E/TLG0003.TXT', '~/Documents/thucydides.txt', extra_args=['p', 'B'])

Concerning text normalization: Even after plaintext conversion, the TLG will still need some cleanup. The CLTK contains some helpful code for `post-TLGU cleanup <http://docs.cltk.org/en/latest/greek.html#text-cleanup>`_.

You may read about these arguments in `the TLGU manual <https://github.com/cltk/tlgu/blob/master/tlgu.1.pdf?raw=true>`_.



Lemmatization
=============

.. tip:: For ambiguous forms, which could belong to several headwords, the current lemmatizer chooses the more commonly occurring headword (`code here <https://github.com/cltk/greek_lexica_perseus/blob/master/transform_lemmata.py>`_). For any errors that you spot, please `open a ticket <https://github.com/kylepjohnson/cltk/issues>`_.

The CLTK's lemmatizer is based on a key-value store, whose code is available at the `CLTK's Latin lemma/POS repository <https://github.com/cltk/latin_pos_lemmata_cltk>`_.

The lemmatizer offers several input and output options. For text input, it can take a string or a list of tokens. Here is an example of the lemmatizer taking a string:

.. code-block:: python

   In [1]: from cltk.stem.lemma import LemmaReplacer

   In [2]: sentence = 'τὰ γὰρ πρὸ αὐτῶν καὶ τὰ ἔτι παλαίτερα σαφῶς μὲν εὑρεῖν διὰ χρόνου πλῆθος ἀδύνατα ἦν'

   In [3]: lemmatizer = LemmaReplacer('greek')

   In [4]: lemmatizer.lemmatize(sentence)
   Out[4]:
   ['τὰ',
    'γὰρ',
    'πρὸ',
    'αὐτός',
    'καὶ',
    'τὰ',
    'ἔτι',
    'παλαιός',
    'σαφής',
    'μὲν',
    'εὑρίσκω',
    'διὰ',
    'χρόνος',
    'πλῆθος',
    'ἀδύνατος',
    'εἰμί']



And here taking a list:

.. code-block:: python

   In [5]: lemmatizer.lemmatize(['χρόνου', 'πλῆθος', 'ἀδύνατα', 'ἦν'])
   Out[5]: ['χρόνος', 'πλῆθος', 'ἀδύνατος', 'εἰμί']

The lemmatizer takes several optional arguments for controlling output: ``return_lemma=True`` and ``return_string=True``. ``return_lemma`` returns the original inflection along with its headword:

.. code-block:: python

   In [6]: lemmatizer.lemmatize(['χρόνου', 'πλῆθος', 'ἀδύνατα', 'ἦν'], return_lemma=True)
   Out[6]: ['χρόνου/χρόνος', 'πλῆθος/πλῆθος', 'ἀδύνατα/ἀδύνατος', 'ἦν/εἰμί']

And ``return string`` wraps the list in ``' '.join()``:

.. code-block:: python

   In [7]: lemmatizer.lemmatize(['χρόνου', 'πλῆθος', 'ἀδύνατα', 'ἦν'], return_string=True)
   Out[7]: 'χρόνος πλῆθος ἀδύνατος εἰμί'

These two arguments can be combined, as well.


POS tagging
===========

Unigram
```````
.. code-block:: python

   In [1]: from cltk.tag.pos import POSTag

   In [2]: tagger = POSTag('greek')

   In [3]: tagger.tag_unigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')
   Out[3]:
   [('θεοὺς', 'N-P---MA-'),
    ('μὲν', 'G--------'),
    ('αἰτῶ', 'V1SPIA---'),
    ('τῶνδ', 'P-P---NG-'),
    ('᾽', None),
    ('ἀπαλλαγὴν', 'N-S---FA-'),
    ('πόνων', 'N-P---MG-'),
    ('φρουρᾶς', 'N-S---FG-'),
    ('ἐτείας', 'A-S---FG-'),
    ('μῆκος', 'N-S---NA-')]


Bigram
``````
.. code-block:: python

   In [4]: tagger.tag_bigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')
   Out[4]:
   [('θεοὺς', 'N-P---MA-'),
    ('μὲν', 'G--------'),
    ('αἰτῶ', 'V1SPIA---'),
    ('τῶνδ', 'P-P---NG-'),
    ('᾽', None),
    ('ἀπαλλαγὴν', None),
    ('πόνων', None),
    ('φρουρᾶς', None),
    ('ἐτείας', None),
    ('μῆκος', None)]


Trigram
```````
.. code-block:: python

   In [5]: tagger.tag_trigram('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')
   Out[5]:
   [('θεοὺς', 'N-P---MA-'),
    ('μὲν', 'G--------'),
    ('αἰτῶ', 'V1SPIA---'),
    ('τῶνδ', 'P-P---MG-'),
    ('᾽', None),
    ('ἀπαλλαγὴν', None),
    ('πόνων', None),
    ('φρουρᾶς', None),
    ('ἐτείας', None),
    ('μῆκος', None)]


1–2–3–gram backoff tagger
`````````````````````````
.. code-block:: python

   In [6]: tagger.tag_ngram_123_backoff('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')
   Out[6]:
   [('θεοὺς', 'N-P---MA-'),
    ('μὲν', 'G--------'),
    ('αἰτῶ', 'V1SPIA---'),
    ('τῶνδ', 'P-P---MG-'),
    ('᾽', None),
    ('ἀπαλλαγὴν', 'N-S---FA-'),
    ('πόνων', 'N-P---MG-'),
    ('φρουρᾶς', 'N-S---FG-'),
    ('ἐτείας', 'A-S---FG-'),
    ('μῆκος', 'N-S---NA-')]


TnT tagger
``````````
.. code-block:: python

   In [7]: tagger.tag_tnt('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')
   Out[7]:
   [('θεοὺς', 'N-P---MA-'),
    ('μὲν', 'G--------'),
    ('αἰτῶ', 'V1SPIA---'),
    ('τῶνδ', 'P-P---NG-'),
    ('᾽', 'Unk'),
    ('ἀπαλλαγὴν', 'N-S---FA-'),
    ('πόνων', 'N-P---MG-'),
    ('φρουρᾶς', 'N-S---FG-'),
    ('ἐτείας', 'A-S---FG-'),
    ('μῆκος', 'N-S---NA-')]


Prosody Scanning
================
There is a prosody scanner for scanning rhythms in Greek texts. It returns a list of strings or long and short marks for each sentence. Note that the last syllable of each sentence string is marked with an anceps so that specific clausulae are dileneated.

.. code-block:: python

   In [1]: from cltk.prosody.greek import Scansion

   In [2]: scanner = Scansion()

   In [3]: scanner.scan_text('νέος μὲν καὶ ἄπειρος, δικῶν ἔγωγε ἔτι. μὲν καὶ ἄπειρος.')
   Out[3]: ['˘¯¯¯˘¯¯˘¯˘¯˘˘x', '¯¯˘¯x']


Sentence Tokenization
=====================

The sentence tokenizer takes a string input into ``tokenize_sentences()`` and returns a list of strings.  For more on the tokenizer, or to make your own, see `the CLTK's Greek sentence tokenizer training set repository <https://github.com/cltk/greek_training_set_sentence>`_.

.. code-block:: python

   In [1]: from cltk.tokenize.sentence import TokenizeSentence

   In [2]: tokenizer = TokenizeSentence('greek')

   In [2]: untokenized_text = 'εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν; ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν. ἀλλ᾽ ἐγώ φημι ταῦτα μὲν φλυαρίας εἶναι· δοκεῖ δέ μοι ἄνδρας ἐλθόντας πρὸς Κῦρον οἵτινες ἐπιτήδειοι σὺν Κλεάρχῳ ἐρωτᾶν ἐκεῖνον τί βούλεται ἡμῖν χρῆσθαι· καὶ ἐὰν μὲν ἡ πρᾶξις ᾖ παραπλησία οἵᾳπερ καὶ πρόσθεν ἐχρῆτο τοῖς ξένοις, ἕπεσθαι καὶ ἡμᾶς καὶ μὴ κακίους εἶναι τῶν πρόσθεν τούτῳ συναναβάντων· ἐὰν δὲ μείζων ἡ πρᾶξις τῆς πρόσθεν φαίνηται καὶ ἐπιπονωτέρα καὶ ἐπικινδυνοτέρα, ἀξιοῦν ἢ πείσαντα ἡμᾶς ἄγειν ἢ πεισθέντα πρὸς φιλίαν ἀφιέναι· οὕτω γὰρ καὶ ἑπόμενοι ἂν φίλοι αὐτῷ καὶ πρόθυμοι ἑποίμεθα καὶ ἀπιόντες ἀσφαλῶς ἂν ἀπίοιμεν· ὅ τι δ᾽ ἂν πρὸς ταῦτα λέγῃ ἀπαγγεῖλαι δεῦρο· ἡμᾶς δ᾽ ἀκούσαντας πρὸς ταῦτα βουλεύεσθαι.'

   In [4]: tokenizer.tokenize_sentences(untokenized_text)
   Out[4]:
   ['εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ, τί κωλύει καὶ τὰ ἄκρα ἡμῖν κελεύειν Κῦρον προκαταλαβεῖν;',
    'ἐγὼ γὰρ ὀκνοίην μὲν ἂν εἰς τὰ πλοῖα ἐμβαίνειν ἃ ἡμῖν δοίη, μὴ ἡμᾶς ταῖς τριήρεσι καταδύσῃ, φοβοίμην δ᾽ ἂν τῷ ἡγεμόνι ὃν δοίη ἕπεσθαι, μὴ ἡμᾶς ἀγάγῃ ὅθεν οὐκ ἔσται ἐξελθεῖν· βουλοίμην δ᾽ ἂν ἄκοντος ἀπιὼν Κύρου λαθεῖν αὐτὸν ἀπελθών· ὃ οὐ δυνατόν ἐστιν.',
    'ἀλλ᾽ ἐγώ φημι ταῦτα μὲν φλυαρίας εἶναι· δοκεῖ δέ μοι ἄνδρας ἐλθόντας πρὸς Κῦρον οἵτινες ἐπιτήδειοι σὺν Κλεάρχῳ ἐρωτᾶν ἐκεῖνον τί βούλεται ἡμῖν χρῆσθαι· καὶ ἐὰν μὲν ἡ πρᾶξις ᾖ παραπλησία οἵᾳπερ καὶ πρόσθεν ἐχρῆτο τοῖς ξένοις, ἕπεσθαι καὶ ἡμᾶς καὶ μὴ κακίους εἶναι τῶν πρόσθεν τούτῳ συναναβάντων· ἐὰν δὲ μείζων ἡ πρᾶξις τῆς πρόσθεν φαίνηται καὶ ἐπιπονωτέρα καὶ ἐπικινδυνοτέρα, ἀξιοῦν ἢ πείσαντα ἡμᾶς ἄγειν ἢ πεισθέντα πρὸς φιλίαν ἀφιέναι· οὕτω γὰρ καὶ ἑπόμενοι ἂν φίλοι αὐτῷ καὶ πρόθυμοι ἑποίμεθα καὶ ἀπιόντες ἀσφαλῶς ἂν ἀπίοιμεν· ὅ τι δ᾽ ἂν πρὸς ταῦτα λέγῃ ἀπαγγεῖλαι δεῦρο· ἡμᾶς δ᾽ ἀκούσαντας πρὸς ταῦτα βουλεύεσθαι.']


Stopword Filtering
==================

To use the CLTK's built-in stopwords list:

.. code-block:: python

   In [1]: from nltk.tokenize.punkt import PunktLanguageVars

   In [2]: from cltk.stop.greek.stops import STOPS_LIST

   In [3]: sentence = 'Ἅρπαγος δὲ καταστρεψάμενος Ἰωνίην ἐποιέετο στρατηίην ἐπὶ Κᾶρας καὶ Καυνίους καὶ Λυκίους, ἅμα ἀγόμενος καὶ Ἴωνας καὶ Αἰολέας.'

   In [4]: p = PunktLanguageVars()

   In [5]: tokens = p.word_tokenize(sentence.lower())

   In [6]: [w for w in tokens if not w in STOPS_LIST]
   Out[6]:
   ['ἅρπαγος',
    'καταστρεψάμενος',
    'ἰωνίην',
    'ἐποιέετο',
    'στρατηίην',
    'κᾶρας',
    'καυνίους',
    'λυκίους',
    ',',
    'ἅμα',
    'ἀγόμενος',
    'ἴωνας',
    'αἰολέας.']


Text Cleanup
============

Intended for use on the TLG after processing by ``TLGU()``.

.. code-block:: python

   In [1]: from cltk.corpus.utils.formatter import tlg_plaintext_cleanup

   In [2]: import os

   In [3]: file = os.path.expanduser('~/cltk_data/greek/text/tlg/individual_works/TLG0035.TXT-001.txt')

   In [4]: with open(file) as f:
   ...:     r = f.read()
   ...:

   In [5]: r[:500]
   Out[5]: "\n{ΜΟΣΧΟΥ ΕΡΩΣ ΔΡΑΠΕΤΗΣ} \n  Ἁ Κύπρις τὸν Ἔρωτα τὸν υἱέα μακρὸν ἐβώστρει: \n‘ὅστις ἐνὶ τριόδοισι πλανώμενον εἶδεν Ἔρωτα, \nδραπετίδας ἐμός ἐστιν: ὁ μανύσας γέρας ἑξεῖ. \nμισθός τοι τὸ φίλημα τὸ Κύπριδος: ἢν δ' ἀγάγῃς νιν, \nοὐ γυμνὸν τὸ φίλημα, τὺ δ', ὦ ξένε, καὶ πλέον ἑξεῖς. \nἔστι δ' ὁ παῖς περίσαμος: ἐν εἴκοσι πᾶσι μάθοις νιν. \nχρῶτα μὲν οὐ λευκὸς πυρὶ δ' εἴκελος: ὄμματα δ' αὐτῷ \nδριμύλα καὶ φλογόεντα: κακαὶ φρένες, ἁδὺ λάλημα: \nοὐ γὰρ ἴσον νοέει καὶ φθέγγεται: ὡς μέλι φωνά, \nὡς δὲ χολὰ νόος ἐστίν: "

   In [7]: tlg_plaintext_cleanup(r, rm_punctuation=True, rm_periods=False)[:500]
   Out[7]: ' Ἁ Κύπρις τὸν Ἔρωτα τὸν υἱέα μακρὸν ἐβώστρει ὅστις ἐνὶ τριόδοισι πλανώμενον εἶδεν Ἔρωτα δραπετίδας ἐμός ἐστιν ὁ μανύσας γέρας ἑξεῖ. μισθός τοι τὸ φίλημα τὸ Κύπριδος ἢν δ ἀγάγῃς νιν οὐ γυμνὸν τὸ φίλημα τὺ δ ὦ ξένε καὶ πλέον ἑξεῖς. ἔστι δ ὁ παῖς περίσαμος ἐν εἴκοσι πᾶσι μάθοις νιν. χρῶτα μὲν οὐ λευκὸς πυρὶ δ εἴκελος ὄμματα δ αὐτῷ δριμύλα καὶ φλογόεντα κακαὶ φρένες ἁδὺ λάλημα οὐ γὰρ ἴσον νοέει καὶ φθέγγεται ὡς μέλι φωνά ὡς δὲ χολὰ νόος ἐστίν ἀνάμερος ἠπεροπευτάς οὐδὲν ἀλαθεύων δόλιον βρέφος ἄγρια π'


TLG Indices
===========

Located at ``cltk/corpus/greek/tlg_index.py`` of the source are indices for the TLG, one of just id and name (``TLG_INDEX``) and another also containing information on the authors' works (``TLG_WORKS_INDEX``).

.. code-block:: python

   In [1]: from cltk.corpus.greek.tlg_index import TLG_INDEX

   In [2]: TLG_INDEX
   Out[2]:
   {'TLG1124': 'Andronicus Rhodius Phil.',
    'TLG3094': 'Nicetas Choniates Hist., Scr. Eccl. et Rhet.',
    'TLG2565': 'Mnesimachus Hist.',
    'TLG1477': 'Manetho Hist.',
    ... }

   In [3]: from cltk.corpus.greek.tlg_index import TLG_WORKS_INDEX

   In [4]: TLG_WORKS_INDEX
   Out [4]:
   {'TLG1587': {'name': 'Philiades Eleg.', 'works': ['001']},
    'TLG0555': {'name': 'Clemens Alexandrinus Theol.',
     'works': ['001', '002', '003', '004', '005', '006', '007', '008']},
    'TLG0402': {'name': 'Alexis Comic.',
     'works': ['001', '002', '003', '004', '005', '006']},
    'TLG2304': {'name': 'Idaeus Phil.', 'works': ['001']},
    'TLG5015': {'name': 'Scholia In Aristotelem', 'works': ['001', '002', '003']},
     ...}


In addition to these indices there are several helper functions which will build filepaths for your particular computer. Not that you will need to have run ``convert_corpus(corpus='tlg')`` and ``divide_works('tlg')`` from the ``TLGU()`` class, respectively, for the following two functions.

.. code-block:: python

   In [1]: from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths

   In [2]: assemble_tlg_author_filepaths()
   Out[2]:
   ['/Users/kyle/cltk_data/greek/text/tlg/plaintext/TLG1167.TXT',
    '/Users/kyle/cltk_data/greek/text/tlg/plaintext/TLG1584.TXT',
    '/Users/kyle/cltk_data/greek/text/tlg/plaintext/TLG1196.TXT',
    '/Users/kyle/cltk_data/greek/text/tlg/plaintext/TLG1201.TXT',
    ...]

   In [3]: from cltk.corpus.utils.formatter import assemble_tlg_works_filepaths

   In [4]: assemble_tlg_works_filepaths()
   Out[4]:
   ['/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG1585.TXT-001.txt',
    '/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG0038.TXT-001.txt',
    '/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG1607.TXT-002.txt',
    '/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG0468.TXT-001.txt',
    '/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG0468.TXT-002.txt',
    '/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG4175.TXT-001.txt',
    '/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG4175.TXT-002.txt',
    '/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG4175.TXT-003.txt',
    '/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG4175.TXT-004.txt',
    '/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG4175.TXT-005.txt',
    '/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG4175.TXT-006.txt',
    '/Users/kyle/cltk_data/greek/text/tlg/individual_works/TLG4175.TXT-007.txt',
    ...]

These two functions are useful when, for example, needing to process all authors of the TLG corpus, all works of the corpus, or all works of one particular author.


.. tip::

   These index files can be greatly improved by better parsing of the TLG's ``.IDT`` index files, as well as the metadata indices which contain information about authors' genres, dates, etc.
