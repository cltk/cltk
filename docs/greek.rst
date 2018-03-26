Greek
*****
Greek is an independent branch of the Indo-European family of languages, native to Greece and other parts of the Eastern Mediterranean. It has the longest documented history of any living language, spanning 34 centuries of written records. Its writing system has been the Greek alphabet for the major part of its history; other systems, such as Linear B and the Cypriot syllabary, were used previously. The alphabet arose from the Phoenician script and was in turn the basis of the Latin, Cyrillic, Armenian, Coptic, Gothic and many other writing systems. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Greek_language>`_)


.. note:: For most of the following operations, you must first `import the CLTK Greek linguistic data <http://docs.cltk.org/en/latest/importing_corpora.html>`_ (named ``greek_models_cltk``).


Accentuation and diacritics
===========================

`James Tauber <https://github.com/jtauber/>`_ has created a Python 3 based `library  <https://github.com/jtauber/greek-accentuation>`_  to enable working with the accentuation of Ancient Greek words. Installing it is optional for working with CLTK.

For further information please see `the original docs <https://github.com/jtauber/greek-accentuation/blob/master/docs.rst>`_, as this is just an abridged version.

The library can be installed with ``pip``:

.. code-block:: python

    pip install greek-accentuation

Contrary to the original docs to use the functions from this module it is necessary to *explicitly* import every function you need as opposed to


**The Characters Module:**

``base`` returns a given character without diacritics. For example:

.. code-block:: python

   In[1]: from greek_accentuation.characters import base

   In[2]: base('ᾳ')
   Out[2]: 'α'

``add_diacritic`` and ``add_breathing`` add diacritics (accents, diaresis, macrons, breves) and breathing symbols to the given character. ``add_diacritic`` is stackable, for example:

.. code-block:: python

   In[1]: from greek_accentuation.characters import add_diacritic

   In[2]: add_diacritic(add_diacritic('ο', ROUGH), ACUTE)
   Out[2]: 'ὅ'

``accent`` and ``strip_accent`` return the accent of a character as an Unicode escape and the character stripped of its accent respectively. ``breathing``, ``strip_breathing``, ``length`` and ``strip_length`` work analogously, for example:

.. code-block:: python

   In[1]: from greek_accentuation.characters import length, strip_length

   In[2]: length('ῠ') == SHORT
   Out[2]: True

   In[3]: strip_length('ῡ')
   Out[3]: 'υ'

If a length diacritic becomes redundant because of a circumflex it can be stripped with ``remove_redundant_macron`` just like ``strip_length`` above.


**The Syllabify Module:**

``syllabify`` splits the given word in syllables, which are returned as a list of strings. Words without vowels are syllabified as a single syllable. The syllabification can also be displayed as a word with the syllablles separated by periods with ``display_word``.

.. code-block:: python

   In[1]: from greek_accentuation.syllabify import syllabify, display_word

   In[2]: syllabify('γυναικός')
   Out[2]: ['γυ', 'ναι', 'κός']

   In[3]: syllabify('γγγ')
   Out[3]: ['γγγ']

   In[4]: display_word(syllabify('καταλλάσσω'))
   Out[4]: 'κα.ταλ.λάσ.σω'

``is_vowel`` and ``is_diphthong`` return a boolean value to determine whether a given character is a vowel or two given characters are a diphthong.

.. code-block:: python

   In[1]: from greek_accentuation.syllabify import is_diphthong

   In[2]: is_diphthong('αι')
   Out[2]: True

``ultima``, ``antepenult`` and ``penult`` return the ultima, antepenult or penult (i.e. the last, next-to-last or third-from-last syllables) of the given word. A syllable can also be further broken down into its onset, nucleus and coda (i.e. the starting consonant, middle part and ending consonant) with the functions named accordingly. ``rime`` returns the sequence of a syllable's nucleus and coda and ``body`` returns the sequence of a syllable's onset and nucleus.


  ``onset_nucleus_coda`` returns a syllable's onset, nucleus and coda all at once as a triple.

.. code-block:: python

   In[1]: from greek_accentuation.syllabify import ultima, rime, onset_nucleus_coda

   In[2]: ultima('γυναικός')
   Out[2]: 'κός'

   In[3]: rime('κός')
   Out[3]: 'ός'

   In[4]: onset_nucleus_coda('ναι')
   Out[4]: ('ν', 'αι', '')

``debreath`` returns a word with the smooth breathing removed and the rough breathing replaced with an h. ``rebreath`` reverses ``debreath``.

.. code-block:: python

   In[1]: from greek_accentuation.syllabify import debreath, rebreath

   In[2]: debreath('οἰκία')
   Out[2]: 'οικία'

   In[3]: rebreath('οικία')
   Out[3]: 'οἰκία'

   In[3]: debreath('ἑξεῖ')
   Out[3]: 'hεξεῖ'

   In[4]: rebreath('hεξεῖ')
   Out[4]: 'ἑξεῖ'


``syllable_length`` returns the length of a syllable (in the linguistic sense) and ``syllable_accent`` extracts a syllable's accent.

.. code-block:: python

   In[1]: from greek_accentuation.syllabify import syllable_length, syllable_accent

   In[2]: syllable_length('σω') == LONG
   Out[2]: True

   In[3]: syllable_accent('ναι') is None
   Out[3]: True

The accentuation class of a word such as oxytone, paroxytone, proparoxytone, perispomenon, properispomenon or barytone can be tested with the functions named accordingly.

``add_necessary_breathing`` adds smooth breathing to a word if necessary.

.. code-block:: python

   In[1]: from greek_accentuation.syllabify import add_necessary_breathing

   In[2]: add_necessary_breathing('οι')
   Out[2]: 'οἰ'

   In[3]: add_necessary_breathing('οἰ')
   Out[3]: 'οἰ'

**The Accentuation Module:**

``get_accent_type`` returns the accent type of a word as a tuple of the syllable number and accent, which is comparable to the constants provided. The accent type can also be displayed as a string with ``display_accent_type``.

.. code-block:: python

   In[1]: from greek_accentuation.accentuation import get_accent_type, display_accent_type

   In[2]: get_accent_type('ἀγαθοῦ') == PERISPOMENON
   Out[2]: True

   In[3]: display_accent_type(get_accent_type('ψυχή'))
   Out[3]: 'oxytone'

``syllable_add_accent(syllable, accent)`` adds the given accent to a syllable. It is also possible to add an accent class to a syllable, for example:

.. code-block:: python

   In[1]: from greek_accentuation.accentuation import syllable_add_accent, make_paroxytone

   In[2]: syllable_add_accent('ου', CIRCUMFLEX)
   Out[2]: 'οῦ'

   In[3]: make_paroxytone('λογος')
   Out[3]: 'λόγος'

``possible_accentuations`` returns all possible accentuations of a given syllabification according to Ancient Greek accentuation rules. To treat vowels of unmarked length as short vowels set ``default_short = True`` in the function parameters.

.. code-block:: python

   In[1]: from greek_accentuation.accentuation import possible_accentuations

   In[2]: s = syllabify('εγινωσκου')

   In[3]: for accent_class in possible_accentuations(s):

   In[4]:     print(add_accent(s, accent_class))
   Out[4]: εγινώσκου
   Out[4]: εγινωσκού
   Out[4]: εγινωσκοῦ

   In[5]: s = syllabify('κυριος')

   In[6]: for accent_class in possible_accentuations(s, default_short=True):

   In[7]:     print(add_accent(s, accent_class))
   Out[7]: κύριος
   Out[7]: κυρίος
   Out[7]: κυριός

``recessive`` finds the most recessive (i.e. as far away from the end of the word as possible) accent and returns the given word with that accent. A ``|`` can be placed to set a point past which the accent will not recede. ``on_penult`` places the accent on the penult (third-from-last syllable).

.. code-block:: python

   In[1]: from greek_accentuation.accentuation import recessive, on_penult

   In[2]: recessive('εἰσηλθον')
   Out[2]: 'εἴσηλθον'

   In[3]: recessive('εἰσ|ηλθον')
   Out[3]: 'εἰσῆλθον'

   In[4]: on_penult('φωνησαι')
   Out[4]: 'φωνῆσαι'

``persistent`` gets passed a word and a lemma (i.e. the canonical form of a set of words) and derives the accent from these two words.

.. code-block:: python

   In[1]: from greek_accentuation.accentuation import persistent

   In[2]: persistent('ἀνθρωπου', 'ἄνθρωπος')
   Out[2]: 'ἀνθρώπου'



**Expand iota subscript:**

The CLTK offers one transformation that can be useful in certain types of processing: Expanding the iota subsctipt from a unicode point and placing beside, to the right, of the character.

.. code-block:: python

   In [1]: from cltk.corpus.greek.alphabet import expand_iota_subscript

   In [2]: s = 'εἰ δὲ καὶ τῷ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῷ'

   In [3]: expand_iota_subscript(s)
   Out[3]: 'εἰ δὲ καὶ τῶΙ ἡγεμόνι πιστεύσομεν ὃν ἂν Κῦρος διδῶΙ'

   In [4]: expand_iota_subscript(s, lowercase=True)
   Out[4]: 'εἰ δὲ καὶ τῶι ἡγεμόνι πιστεύσομεν ὃν ἂν κῦρος διδῶι'




Alphabet
========

The Greek vowels and consonants in upper and lower case are placed in `cltk/corpus/greek/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/greek/alphabet.py>`_.

Greek vowels can occur without any breathing or accent, have rough or smooth breathing, different accents, diareses, macrons, breves and combinations thereof and Greek consonants have none of these features, except *ρ*, which can have rough or smooth breathing.

In `alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/greek/alphabet.py>`_ the vowels and consonants are grouped by upper or lower case, accent, breathing, a diaresis and possible combinations thereof.
These groupings are stored in lists or, in case of a single letter like ρ, as strings with descriptive names structured like ``CASE_SPECIFIERS``, e.g. ``LOWER_DIARESIS_CIRCUMFLEX``.

For example to use upper case vowels with rough breathing and an acute accent:

.. code-block:: python

   In[1]: from cltk.corpus.greek.alphabet import UPPER_ROUGH_ACUTE
   In[2]: print(UPPER_ROUGH_ACUTE)
   Out[2]: ['Ἅ', 'Ἕ', 'Ἥ', 'Ἵ', 'Ὅ', 'Ὕ', 'Ὥ', 'ᾍ', 'ᾝ', 'ᾭ']


Accents indicate the pitch of vowels. An *acute accent* or *ὀξεῖα (oxeîa)* indicates a rising pitch on a long vowel or a high pitch on a short vowel, a *grave accent* or *βαρεῖα (bareîa)* indicates a normal or low pitch and a *circumflex* or *περισπωμένη (perispōménē)* indicates high or falling pitch within one syllable.

Breathings, which are used not only on vowels, but also on *ρ*, indicate the presence or absence of a voiceless glottal fricative - rough breathing indicetes a voiceless glottal fricative before a vowel, like in *αἵρεσις (haíresis)* and smooth breathing indicates none.

Diareses are placed on *ι* and *υ* to indicate two vowels not being a diphthong and macrons and breves are placed on *α, ι*, and *υ* to indicate the length of these vowels.

For more information on Greek diacritics see the corresponding `wikipedia page <https://en.wikipedia.org/wiki/Greek_diacritics#Description>`_.

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

Once these files are created, see `TLG Indices <http://docs.cltk.org/en/latest/greek.html#tlg-indices>`_ below for accessing these newly created files.

See also `Text Cleanup <http://docs.cltk.org/en/latest/greek.html#text-cleanup>` for removing extraneous non-textual characters from these files.



Information Retrieval
=====================

See `Multilingual Information Retrieval <http://docs.cltk.org/en/latest/multilingual.html#information-retrieval>`_ for Greek–specific search options.


Lemmatization
=============

.. tip:: For ambiguous forms, which could belong to several headwords, the current lemmatizer chooses the more commonly occurring headword (`code here <https://github.com/cltk/greek_lexica_perseus/blob/master/transform_lemmata.py>`_). For any errors that you spot, please `open a ticket <https://github.com/cltk/cltk/issues>`_.

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

The lemmatizer takes several optional arguments for controlling output: ``return_raw=True`` and ``return_string=True``. ``return_raw`` returns the original inflection along with its headword:

.. code-block:: python

   In [6]: lemmatizer.lemmatize(['χρόνου', 'πλῆθος', 'ἀδύνατα', 'ἦν'], return_raw=True)
   Out[6]: ['χρόνου/χρόνος', 'πλῆθος/πλῆθος', 'ἀδύνατα/ἀδύνατος', 'ἦν/εἰμί']

And ``return string`` wraps the list in ``' '.join()``:

.. code-block:: python

   In [7]: lemmatizer.lemmatize(['χρόνου', 'πλῆθος', 'ἀδύνατα', 'ἦν'], return_string=True)
   Out[7]: 'χρόνος πλῆθος ἀδύνατος εἰμί'

These two arguments can be combined, as well.



Named Entity Recognition
========================

.. tip::

   NER is new functionality. Please report any errors you observe.

There is available a simple interface to `a list of Greek proper nouns <https://github.com/cltk/greek_proper_names_cltk>`_. By default ``tag_ner()`` takes a string input and returns a list of tuples. However it can also take pre-tokenized forms and return a string.

.. code-block:: python

   In [1]: from cltk.tag import ner

   In [2]: text_str = 'τὰ Σίλαριν Σιννᾶν Κάππαρος Πρωτογενείας Διονυσιάδες τὴν'

   In [3]: ner.tag_ner('greek', input_text=text_str, output_type=list)
   Out[3]:
   [('τὰ',),
    ('Σίλαριν', 'Entity'),
    ('Σιννᾶν', 'Entity'),
    ('Κάππαρος', 'Entity'),
    ('Πρωτογενείας', 'Entity'),
    ('Διονυσιάδες', 'Entity'),
    ('τὴν',)]


Normalization
=============

Normalizing polytonic Greek is a problem that has been mostly solved, however when working with legacy applications issues still arise. We recommend normalizing Greek vowels in order to ensure string matching.

One type of normalization issue comes from tonos accents (intended for Modern Greek) being used instead of the oxia accents (for Ancient Greek). Here is an example of two characters appearing identical but being in fact dissimilar:


.. code-block:: python

   In [1]: from cltk.corpus.utils.formatter import tonos_oxia_converter

   In [2]: char_tonos = "ά"  # with tonos, for Modern Greek

   In [3]: char_oxia = "ά"  # with oxia, for Ancient Greek

   In [4]: char_tonos == char_oxia
   Out[4]: False

   In [5]: ord(char_tonos)
   Out[5]: 940

   In [6]: ord(char_oxia)
   Out[6]: 8049

   In [7]: char_oxia == tonos_oxia_converter(char_tonos)
   Out[7]: True


If for any reason you want to go from oxia to tonos, just add the ``reverse=True`` parameter:

.. code-block:: python

   In [8]: char_tonos == tonos_oxia_converter(char_oxia, reverse=True)
   Out[8]: True


Another approach to normalization is to use the Python language's builtin ``normalize()``. The CLTK provides a wrapper \
for this, as a convenience. Here's an example its use in "compatibility" mode (``NFKC``):

.. code-block:: python

   In [1]: from cltk.corpus.utils.formatter import cltk_normalize

   In [2]: tonos = "ά"

   In [3]: oxia = "ά"

   In [4]: tonos == oxia
   Out[4]: False

   In [5]: tonos == cltk_normalize(oxia)
   Out[5]: True


One can turn off compatability with:

.. code-block:: python

   In [6]: tonos == cltk_normalize(oxia, compatibility=False)
   Out[6]: True

For more on ``normalize()`` see the `Python Unicode docs <https://docs.python.org/3.5/library/unicodedata.html#unicodedata.normalize>`_.


POS tagging
===========

These taggers were built with the assistance of the NLTK. The backoff tagger is Bayseian and the TnT is HMM. To obtain the models, first import the ``greek_models_cltk`` corpus.

1–2–3–gram backoff tagger
`````````````````````````
.. code-block:: python

   In [1]: from cltk.tag.pos import POSTag

   In [2]: tagger = POSTag('greek')

   In [3]: tagger.tag_ngram_123_backoff('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')
   Out[3]:
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

   In [4]: tagger.tag_tnt('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')
   Out[4]:
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


CRF tagger
``````````

.. warning:: This tagger's accuracy has not yet been tested.

We use the NLTK's CRF tagger. For information on it, see `the NLTK docs <http://www.nltk.org/_modules/nltk/tag/crf.html>`_.

.. code-block:: python

   In [5]: tagger.tag_crf('θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος')
   Out[5]:
   [('θεοὺς', 'N-P---MA-'),
    ('μὲν', 'G--------'),
    ('αἰτῶ', 'V1SPIA---'),
    ('τῶνδ', 'P-P---NG-'),
    ('᾽', 'A-S---FA-'),
    ('ἀπαλλαγὴν', 'N-S---FA-'),
    ('πόνων', 'N-P---MG-'),
    ('φρουρᾶς', 'A-S---FG-'),
    ('ἐτείας', 'N-S---FG-'),
    ('μῆκος', 'N-S---NA-')]


Prosody Scanning
================
There is a prosody scanner for scanning rhythms in Greek texts. It returns a list of strings or long and short marks for each sentence. Note that the last syllable of each sentence string is marked with an anceps so that specific clausulae are dileneated.

.. code-block:: python

   In [1]: from cltk.prosody.greek.scanner import Scansion

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


Swadesh
=======
The corpus module has a class for generating a Swadesh list for Greek.

.. code-block:: python

   In [1]: from cltk.corpus.swadesh import Swadesh

   In [2]: swadesh = Swadesh('gr')

   In [3]: swadesh.words()[:10]
   Out[3]: ['ἐγώ', 'σύ', 'αὐτός, οὗ, ὅς, ὁ, οὗτος', 'ἡμεῖς', 'ὑμεῖς', 'αὐτοί', 'ὅδε', 'ἐκεῖνος', 'ἔνθα, ἐνθάδε, ἐνταῦθα', 'ἐκεῖ']
   

TEI XML
=======

There are several rudimentary corpus converters for the "First 1K Years of Greek" project (download the corpus ``'greek_text_first1kgreek'``). Both write files to `` ~/cltk_data/greek/text/greek_text_first1kgreek_plaintext``.

This one is built upon the ``MyCapytain`` library (``pip install lxml MyCapytain``), which has the ability for very precise chunking of TEI xml. The following function only preserves numbers:

.. code-block:: python

   In [1]: from cltk.corpus.greek.tei import onekgreek_tei_xml_to_text_capitains

   In [2]: onekgreek_tei_xml_to_text_capitains()



For the following, install the ``BeautifulSoup`` library (``pip install bs4``). Note that this will just dump all text not contained within a node's bracket (including sometimes metadata).

.. code-block:: python

   In [1]: from cltk.corpus.greek.tei import onekgreek_tei_xml_to_text

   In [2]: onekgreek_tei_xml_to_text()


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

The TLG comes with some old, difficult-to-parse index files which have been made available as Python dictionaries (at ``/Users/kyle/cltk/cltk/corpus/greek/tlg``). Below are some functions to make accessing these easy. The outputs are variously a ``dict`` of an index or ``set`` if the function returns unique author ids.

.. tip::

   Python sets are like lists, but contain only unique values. Multiple sets can be conveniently combined (`see docs here <https://docs.python.org/3.5/library/stdtypes.html?highlight=set#set>`_).

.. code-block:: python

   In [1]: from cltk.corpus.greek.tlg.parse_tlg_indices import get_female_authors

   In [2]: from cltk.corpus.greek.tlg.parse_tlg_indices import get_epithet_index

   In [3]: from cltk.corpus.greek.tlg.parse_tlg_indices import get_epithets

   In [4]: from cltk.corpus.greek.tlg.parse_tlg_indices import select_authors_by_epithet

   In [5]: from cltk.corpus.greek.tlg.parse_tlg_indices import get_epithet_of_author

   In [6]: from cltk.corpus.greek.tlg.parse_tlg_indices import get_geo_index

   In [7]: from cltk.corpus.greek.tlg.parse_tlg_indices import get_geographies

   In [8]: from cltk.corpus.greek.tlg.parse_tlg_indices import select_authors_by_geo

   In [9]: from cltk.corpus.greek.tlg.parse_tlg_indices import get_geo_of_author

   In [10]: from cltk.corpus.greek.tlg.parse_tlg_indices import get_lists

   In [11]: from cltk.corpus.greek.tlg.parse_tlg_indices import get_id_author

   In [12]: from cltk.corpus.greek.tlg.parse_tlg_indices import select_id_by_name

   In [13]: get_female_authors()
   Out[13]:
   {'0009',
    '0051',
    '0054',
    …}

   In [14]: get_epithet_index()
   Out[14]:
   {'Lexicographi': {'3136', '4040', '4085', '9003'},
    'Lyrici/-ae': {'0009',
     '0033',
     '0199',
     …}}

   In [15]: get_epithets()
   Out[15]:
   ['Alchemistae',
    'Apologetici',
    'Astrologici',
    …]

   In [16]: select_authors_by_epithet('Tactici')
   Out[16]: {'0058', '0546', '0556', '0648', '3075', '3181'}

   In [17]: get_epithet_of_author('0016')
   Out[17]: 'Historici/-ae'

   In [18]: get_geo_index()
   Out[18]:
   {'Alchemistae': {'1016',
     '2019',
     '2140',
     '2181',
     …}}

   In [19]: get_geographies()
   Out[19]:
   ['Abdera',
    'Adramytteum',
    'Aegae',
    …]

   In [20]: select_authors_by_geo('Thmuis')
   Out[20]: {'2966'}

   In [21]: get_geo_of_author('0216')
   Out[21]: 'Aetolia'

   In [22]: get_lists()
   Out[22]:
   {'Lists pertaining to all works in Canon (by TLG number)': {'LIST3CLA.BIN': 'Literary classifications of works',
     'LIST3CLX.BIN': 'Literary classifications of works (with x-refs)',
     'LIST3DAT.BIN': 'Chronological classifications of authors',
      …}}

   In [23]: get_id_author()
   Out[23]:
   {'1139': 'Anonymi Historici (FGrH)',
    '4037': 'Anonymi Paradoxographi',
    '0616': 'Polyaenus Rhet.',
    …}

   In [28]: select_id_by_name('hom')
   Out[28]:
   [('0012', 'Homerus Epic., Homer'),
    ('1252', 'Certamen Homeri Et Hesiodi'),
    ('1805', 'Vitae Homeri'),
    ('5026', 'Scholia In Homerum'),
    ('1375', 'Evangelium Thomae'),
    ('2038', 'Acta Thomae'),
    ('0013', 'Hymni Homerici, Homeric Hymns'),
    ('0253', '[Homerus] [Epic.]'),
    ('1802', 'Homerica'),
    ('1220', 'Batrachomyomachia'),
    ('9023', 'Thomas Magister Philol.')]


In addition to these indices there are several helper functions which will build filepaths for your particular computer. Note that you will need to have run ``convert_corpus(corpus='tlg')`` and ``divide_works('tlg')`` from the ``TLGU()`` class, respectively, for the following two functions.

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



Transliteration
===============

The CLTK provides `IPA phonetic transliteration <https://en.wikipedia.org/wiki/International_Phonetic_Alphabet>`_ for \
the Greek language. Currently, the only available dialect is Attic as reconstructed by Philomen Probert \
(taken from `A Companion to the Ancient Greek Language <https://books.google.com/books?id=oa42E3DP3icC&printsec=frontcover#v=onepage&q&f=false>`_, \
85-103). Example:

.. code-block:: python

   In [1]: from cltk.phonology.greek.transcription import Transcriber

   In [2]: transcriber = Transcriber(dialect="Attic", reconstruction="Probert")

   In [3]: transcriber.transcribe("Διόθεν καὶ δισκήπτρου τιμῆς ὀχυρὸν ζεῦγος Ἀτρειδᾶν στόλον Ἀργείων")
   Out[3]: '[di.ó.tʰen kɑj dis.kɛ́ːp.trọː ti.mɛ̂ːs o.kʰy.ron zdêw.gos ɑ.trẹː.dɑ̂n stó.lon ɑr.gẹ́ː.ɔːn]'


Word Tokenization
=================

.. code-block:: python

   In [1]: from cltk.tokenize.word import WordTokenizer

   In [2]: word_tokenizer = WordTokenizer('greek')

   In [3]: text = 'Θουκυδίδης Ἀθηναῖος ξυνέγραψε τὸν πόλεμον τῶν Πελοποννησίων καὶ Ἀθηναίων,'

   In [4]: word_tokenizer.tokenize(text)
   Out[4]: ['Θουκυδίδης', 'Ἀθηναῖος', 'ξυνέγραψε', 'τὸν', 'πόλεμον', 'τῶν', 'Πελοποννησίων', 'καὶ', 'Ἀθηναίων', ',']
   

Word2Vec
========

.. note::

   The Word2Vec models have not been fully vetted and are offered in the spirit of a beta. The CLTK's API for it \
   will be revised.

.. note::

   You will need to install `Gensim <https://radimrehurek.com/gensim/install.html>`_ to use these features.

Word2Vec is a `Vector space model <https://en.wikipedia.org/wiki/Vector_space_model>`_ especially powerful for comparing \
words in relation to each other. For instance, it is commonly used to discover words which appear in \
similar contexts (something akin to synonyms; think of them as lexical clusters).

The CLTK repository contains pre-trained Word2Vec models for Greek (import as ``greek_word2vec_cltk``), one lemmatized and the other not. They were trained on \
the TLG corpus. To train your own, see the README at `the Greek Word2Vec repository <https://github.com/cltk/greek_word2vec_cltk>`_.

One of the most common uses of Word2Vec is as a keyword expander. Keyword expansion is the taking of a query term, \
finding synonyms, and searching for those, too. Here's an example of its use:

.. code-block:: python

   In [1]: from cltk.ir.query import search_corpus

   In [2]: In [6]: for x in search_corpus('πνεῦμα', 'tlg', context='sentence', case_insensitive=True, expand_keyword=True, threshold=0.5):
       print(x)
      ...:
   The following similar terms will be added to the 'πνεῦμα' query: '['γεννώμενον', 'ἔντερον', 'βάπτισμα', 'εὐαγγέλιον', 'δέρμα', 'ἐπιῤῥέον', 'ἔμβρυον', 'ϲῶμα', 'σῶμα', 'συγγενὲς']'.
   ('Lucius Annaeus Cornutus Phil.', "μυθολογεῖται δ' ὅτι διασπασθεὶς ὑπὸ τῶν Τιτά-\nνων συνετέθη πάλιν ὑπὸ τῆς Ῥέας, αἰνιττομένων τῶν \nπαραδόντων τὸν μῦθον ὅτι οἱ γεωργοί, θρέμματα γῆς \nὄντες, συνέχεαν τοὺς βότρυς καὶ τοῦ ἐν αὐτοῖς Διονύσου \nτὰ μέρη ἐχώρισαν ἀπ' ἀλλήλων, ἃ δὴ πάλιν ἡ εἰς ταὐτὸ \nσύρρυσις τοῦ γλεύκους συνήγαγε καὶ ἓν *σῶμα* ἐξ αὐτῶν \nἀπετέλεσε.")
   ('Metopus Phil.', '\nκαὶ ταὶ νόσοι δὲ γίνονται τῶ σώματος <τῷ> θερμότερον ἢ κρυμωδέσ-\nτερον γίνεσθαι τὸ *σῶμα*.')
   …


``threshold`` is the closeness of the query term to its neighboring words. Note that when ``expand_keyword=True``, the \
search term will be stripped of any regular expression syntax.

The keyword expander leverages ``get_sims()`` (which in turn leverages functionality of the Gensim package) to find similar terms. \
Some examples of it in action:

.. code-block:: python

   In [3]: from cltk.vector.word2vec import get_sims

   In [4]: get_sims('βασιλεύς', 'greek', lemmatized=False, threshold=0.5)
   "word 'βασιλεύς' not in vocabulary"
   The following terms in the Word2Vec model you may be looking for: '['βασκαίνων', 'βασκανίας', 'βασιλάκιος', 'βασιλίδων', 'βασανισθέντα', 'βασιλήϊον', 'βασιλευόμενα', 'βασανιστηρίων', … ]'.

   In [36]: get_sims('τυραννος', 'greek', lemmatized=True, threshold=0.7)
   "word 'τυραννος' not in vocabulary"
   The following terms in the Word2Vec model you may be looking for: '['τυραννίσιν', 'τυρόριζαν', 'τυρεύοντες', 'τυρρηνοὶ', 'τυραννεύοντα', 'τυροὶ', 'τυραννικά', 'τυρσηνίαν', 'τυρώ', 'τυρσηνίας', … ]'.

To add and subtract vectors, you need to load the models yourself with Gensim.
