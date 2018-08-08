Old Norse
*********

Old Norse was a North Germanic language that was spoken by inhabitants of Scandinavia and inhabitants of their overseas settlements during about the 9th to 13th centuries. The Proto-Norse language developed into Old Norse by the 8th century, and Old Norse began to develop into the modern North Germanic languages in the mid- to late-14th century, ending the language phase known as Old Norse. These dates, however, are not absolute, since written Old Norse is found well into the 15th century. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Old_Norse>`_)


Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``old_norse_``) to discover available Old Norse corpora.

.. code-block:: python

    In[1]: from cltk.corpus.utils.importer import CorpusImporter

    In[2]: corpus_importer = CorpusImporter("old_norse")

    In[3]: corpus_importer.list_corpora

    Out[3]: ['old_norse_text_perseus', 'old_norse_models_cltk']


Stopword Filtering
==================

To use the CLTK's built-in stopwords list, We use an example from `Eiríks saga rauða
<http://www.heimskringla.no/wiki/Eir%C3%ADks_saga_rau%C3%B0a>`_:

.. code-block:: python

    In[1]: from nltk.tokenize.punkt import PunktLanguageVars

    In[2]: from cltk.stop.old_norse.stops import STOPS_LIST

    In[3]: sentence = 'Þat var einn morgin, er þeir Karlsefni sá fyrir ofan rjóðrit flekk nökkurn, sem glitraði við þeim'

    In[4]: p = PunktLanguageVars()

    In[5]: tokens = p.word_tokenize(sentence.lower())

    In[6]: [w for w in tokens if not w in STOPS_LIST]

    Out[6]: ['var',
    'einn',
    'morgin',
    ',',
    'karlsefni',
    'rjóðrit',
    'flekk',
    'nökkurn',
    ',',
    'glitraði']


Swadesh
=======
The corpus module has a class for generating a Swadesh list for Old Norse.

.. code-block:: python

    In[1]: from cltk.corpus.swadesh import Swadesh

    In[2]: swadesh = Swadesh('old_norse')

    In[3]: swadesh.words()[:10]

    Out[3]: ['ek', 'þú', 'hann', 'vér', 'þér', 'þeir', 'sjá, þessi', 'sá', 'hér', 'þar']


Word Tokenizing
===============
A very simple tokenizer is available for Old Norse. For now, it does not take into account specific Old Norse constructions like the merge of conjugated verbs with þú and with sik.
Here is a sentence extracted from *Gylfaginning* in the *Edda* by Snorri Sturluson.

.. code-block:: python

    In[1]: word_tokenizer = WordTokenizer('old_norse')

    In[2]: sentence = "Gylfi konungr var maðr vitr ok fjölkunnigr."

    In[3]: word_tokenizer.tokenize(sentence)

    Out[3]:['Gylfi', 'konungr', 'var', 'maðr', 'vitr', 'ok', 'fjölkunnigr', '.']


POS tagging
===========

You can get the POS tags of Old Norse texts using the CLTK's wrapper around the NLTK tokenizer. First, download the model by importing the ``old_norse_models_cltk`` corpus. This TnT tagger was trained from annotated data from `Icelandic Parsed Historical Corpus <http://www.linguist.is/icelandic_treebank/Download>`_ (version 0.9, license: LGPL).

TnT tagger
``````````

The following sentence is from the first verse of *Völuspá* (a poem describing destiny of Agards gods).

.. code-block:: python

    In[1]: from cltk.tag.pos import POSTag

    In[2]: tagger = POSTag('old_norse')

    In[3]: sent = 'Hlióðs bið ek allar.'

    In[4]: tagger.tag_tnt(sent)

    Out[4]: [('Hlióðs', 'Unk'),
    ('bið', 'VBPI'),
    ('ek', 'PRO-N'),
    ('allar', 'Q-A'),
    ('.', '.')]

Phonology transcription
=======================

According to phonological rules (available at `Wikipedia - Old Norse orthography <https://en.wikipedia.org/wiki/Old_Norse_orthography>`_  and *Altnordisches Elementarbuch* by Friedrich Ranke and Dietrich Hofmann), a reconstructed pronunciation of Old Norse words is implemented.

.. code-block:: python

    In[1]: from cltk.phonology.old_norse import transcription as ont

    In[2]: sentence = "Gylfi konungr var maðr vitr ok fjölkunnigr"

    In[3]: tr = ut.Transcriber(ont.DIPHTHONGS_IPA, ont.DIPHTHONGS_IPA_class, ont.IPA_class, ont.old_norse_rules)

    In[4]: tr.main(sentence)

    Out[4]: "[gylvi kɔnungr var maðr vitr ɔk fjœlkunːiɣr]"

Runes
=====
The oldest runic inscriptions found are from 200 AC. They have always denoted Germanic languages. Until the 8th century, the elder *futhark* alphabet was used. It was compouned with 24 characters: ᚠ, ᚢ, ᚦ, ᚨ, ᚱ, ᚲ, ᚷ, ᚹ, ᚺ, ᚾ, ᛁ, ᛃ, ᛇ, ᛈ, ᛉ, ᛊ, ᛏ, ᛒ, ᛖ, ᛗ, ᛚ, ᛜ, ᛟ, ᛞ. The word *Futhark* comes from the 6 first characters of the alphabet: ᚠ (f), ᚢ (u), ᚦ (th), ᚨ (a), ᚱ (r), ᚲ (k). Later, this alphabet was reduced to 16 runes, the *younger futhark* ᚠ, ᚢ, ᚦ, ᚭ, ᚱ, ᚴ, ᚼ, ᚾ, ᛁ, ᛅ, ᛋ, ᛏ, ᛒ, ᛖ, ᛘ, ᛚ, ᛦ, with more ambiguity on sounds. Shapes of runes may vary according to which matter they are carved on, that is why there is a variant of the *younger futhark* like this: ᚠ, ᚢ, ᚦ, ᚭ, ᚱ, ᚴ, ᚽ, ᚿ, ᛁ, ᛅ, ᛌ, ᛐ, ᛓ, ᛖ, ᛙ, ᛚ, ᛧ.

.. code-block:: python

    In[1]: from cltk.corpus.old_norse import runes

    In[2]: " ".join(Rune.display_runes(ELDER_FUTHARK))

    Out[2]: ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ ᚹ ᚺ ᚾ ᛁ ᛃ ᛇ ᛈ ᛉ ᛊ ᛏ ᛒ ᛖ ᛗ ᛚ ᛜ ᛟ ᛞ

    In[3]: little_jelling_stone = "᛬ᚴᚢᚱᛘᛦ᛬ᚴᚢᚾᚢᚴᛦ᛬ᚴ(ᛅᚱ)ᚦᛁ᛬ᚴᚢᛒᛚ᛬ᚦᚢᛋᛁ᛬ᛅ(ᚠᛏ)᛬ᚦᚢᚱᚢᛁ᛬ᚴᚢᚾᚢ᛬ᛋᛁᚾᛅ᛬ᛏᛅᚾᛘᛅᚱᚴᛅᛦ᛬ᛒᚢᛏ᛬"

    In[4]: Transcriber.transcribe(little_jelling_stone, YOUNGER_FUTHARK)

    Out[4]: "᛫kurmR᛫kunukR᛫k(ar)þi᛫kubl᛫þusi᛫a(ft)᛫þurui᛫kunu᛫sina᛫tanmarkaR᛫but᛫"

Syllabification
===============

For a language-dependent approach, you can call the predefined sonority dictionary by toogling the ``language`` parameter:

.. code-block:: python

    In[1]: s = Syllabifier(language='old_norse')

    In[2]: s.syllabify("danmarkar")

    Out[2]: ['dan', 'mar', 'kar']


Old Norse prosody
=================

* Fornyrðislag

.. code-block:: python

    In[1]: text1 = "Hljóðs bið ek allar\nhelgar kindir,\nmeiri ok minni\nmögu Heimdallar;\nviltu at ek, Valföðr,\nvel fyr telja\nforn spjöll fira,\nþau er fremst of man."

    In[2]: VerseManager.is_fornyrdhislag(text1)

    Out[2]: True

    In[3]: fo = Fornyrdhislag()

    In[4]: fo.from_short_lines_text(text1)

    In[5]: fo.short_lines

    Out[5]: ['Hljóðs bið ek allar', 'helgar kindir,', 'meiri ok minni', 'mögu Heimdallar;', 'viltu at ek, Valföðr,', 'vel fyr telja', 'forn spjöll fira,', 'þau er fremst of man.']

    In[6]: fo.long_lines

    Out[6]: [['Hljóðs bið ek allar', 'helgar kindir,'], ['meiri ok minni', 'mögu Heimdallar;'], ['viltu at ek, Valföðr,', 'vel fyr telja'], ['forn spjöll fira,', 'þau er fremst of man.']]

    In[7]: fo.syllabify()

    In[8]: fo.syllabified_text

    Out[8]: [[[[['hljóðs'], ['bið'], ['ek'], ['al', 'lar']]], [[['hel', 'gar'], ['kin', 'dir']]]], [[[['meir', 'i'], ['ok'], ['min', 'ni']]], [[['mög', 'u'], ['heim', 'dal', 'lar']]]], [[[['vil', 'tu'], ['at'], ['ek'], ['val', 'föðr']]], [[['vel'], ['fyr'], ['tel', 'ja']]]], [[[['forn'], ['spjöll'], ['fir', 'a']]], [[['þau'], ['er'], ['fremst'], ['of'], ['man']]]]]

    In[9]: fo.to_phonetics()

    In[10]: fo.transcribed_text

    Out[10]: [['[dɐyr feː]', '[dɐyja frɛːndr]'], ['[dɐyr sjalvr it sama]', '[ɛk vɛit ɛinː]'], ['[at aldrɛi dɐyr]', '[doːmr um dɒuðan hvɛrn]']]


* Ljóðaháttr

.. code-block:: python

    In[1]: text2 = "Deyr fé,\ndeyja frændr,\ndeyr sjalfr it sama,\nek veit einn,\nat aldrei deyr:\ndómr um dauðan hvern."

    In[2]: VerseManager.is_ljoodhhaattr(text2)

    Out[2]: True

    In[3]: lj = Ljoodhhaatr()

    In[4]: lj.from_short_lines_text(text2)

    In[5]: lj.short_lines

    Out[5]: ['Deyr fé,', 'deyja frændr,', 'deyr sjalfr it sama,', 'ek veit einn,', 'at aldrei deyr:', 'dómr um dauðan hvern.']

    In[6]: lj.long_lines

    Out[6]: [['Deyr fé,', 'deyja frændr,'], ['deyr sjalfr it sama,'], ['ek veit einn,', 'at aldrei deyr:'], ['dómr um dauðan hvern.']]

    In[7]: lj.syllabify()

    In[8]: lj.syllabified_text

    Out[8]: [[[[['deyr'], ['fé']]], [[['deyj', 'a'], ['frændr']]]], [[[['deyr'], ['sjalfr'], ['it'], ['sam', 'a']]]], [[[['ek'], ['veit'], ['einn']]], [[['at'], ['al', 'drei'], ['deyr']]]], [[[['dómr'], ['um'], ['dau', 'ðan'], ['hvern']]]]]

* Dróttkvætt

* Hrynhenda


Old Norse pronouns declension
=============================

Old Norse, like other ancient Germanic languages, is highly inflected. With the **declension module**, you can get a declined form of a pronoun already stored.

.. code-block:: python

    In[1]: from cltk.declension.old_norse import utils as decl_utils

    In[2]: pro_demonstrative_pronouns_this = Pronoun("demonstrative pronouns this")

    In[3]: demonstrative_pronouns_this = [[["þessi", "þenna", "þessum", "þessa"], ["þessir", "þessa", "þessum", "þessa"]], [["þessi", "þessa", "þessi", "þessar"], ["þessar", "þessar", "þessum", "þessa"]], [["þetta", "þetta", "þessu", "þessa"], ["þessi", "þessi", "þessum", "þessa"]]]

    In[4]: pro_demonstrative_pronouns_this.set_declension(demonstrative_pronouns_this)

    In[5]: pro_demonstrative_pronouns_this.get_declined(decl_utils.Case.accusative, decl_utils.Number.singular, decl_utils.Gender.feminine)

    Out[5]: 'þessa'

