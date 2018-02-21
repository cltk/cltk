Hindi
********

Hindi is a standardised and Sanskritised register of the Hindustani language. Like other Indo-Aryan languages, Hindi is considered to be a direct descendant of an early form of Sanskrit, through Sauraseni Prakrit and Śauraseni Apabhraṃśa. It has been influenced by Dravidian languages, Turkic languages, Persian, Arabic, Portuguese and English. Hindi emerged as Apabhramsha, a degenerated form of Prakrit, in the 7th century A.D. By the 10th century A.D., it became stable. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Hindi>`_)


Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``hindi_``) to discover available Hindi corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('hindi')

   In [3]: c.list_corpora
   Out[3]:
   ['hindi_text_ltrc']


Stopword Filtering
==================

To use the CLTK's built-in stopwords list:

.. code-block:: python

   In [1]: from cltk.stop.classical_hindi.stops import STOPS_LIST

   In [2]: print(STOPS_LIST[:5])
   Out[2]: ["हें", "है", "हैं", "हि", "ही"]


Swadesh
=======

The corpus module has a class for generating a Swadesh list for classical hindi.

.. code-block:: python

   In [1]: from cltk.corpus.swadesh import Swadesh

   In [2]: swadesh = Swadesh('hi')

   In [3]: swadesh.words()[:10]
   Out[3]: ['मैं', 'तू', 'वह', 'हम', 'तुम', 'वे', 'यह', 'वह', 'यहाँ', 'वहाँ' ]


Tokenizer
=========

This tool can break a sentence into its constituent words. It simply splits the text into tokens of words and punctuations.

.. code-block:: python

   In [1]: from cltk.tokenize.sentence import TokenizeSentence

   In [2]: import os

   In [3]: root = os.path.expanduser('~')

   In [4]: hindi_corpus = os.path.join(root,'cltk_data/hindi/text/hindi_text_ltrc')

   In [5]: hindi_text_path = os.path.join(hindi_corpus, 'miscellaneous/gandhi/main.txt')

   In [6]: hindi_text = open(hindi_text_path,'r').read()

   In [7]: tokenizer = TokenizeSentence('hindi')

   In [8]: hindi_text_tokenize = tokenizer.tokenize(hindi_text)

   In [9]: print(hindi_text_tokenize[0:100])
   ['10्र', 'प्रति', 'ा', 'वापस', 'नहीं', 'ली', 'जातीएक', 'बार', 'कस्तुरबा', 'गांधी', 'बहुत', 'बीमार', 'हो', 'गईं', '।', 'जलर्', 'चिकित्सा', 'से', 'उन्हें', 'कोई', 'लाभ', 'नहीं', 'हुआ', '।', 'दूसरे', 'उपचार', 'किये', 'गये', '।', 'उनमे', 'भी', 'सफलता', 'नहीं', 'मिली', '।', 'अंत', 'में', 'गांधीजी', 'ने', 'उन्हें', 'नमक', 'और', 'दाल', 'छोडने', 'की', 'सलाह', 'दी', '।', 'परन्तु', 'इसके', 'लिए', 'बा', 'तैयार', 'नहीं', 'हुईं', '।', 'गांधीजी', 'ने', 'बहुत', 'समझाया', '.', 'पोथियों', 'से', 'प्रमाण', 'पढकर', 'सुनाये', '.', 'लेकर', 'सब', 'व्यर्थ', '।', 'बा', 'बोलीं', '.', '"', 'कोई', 'आपसे', 'कहे', 'कि', 'दाल', 'और', 'नमक', 'छोड', 'दो', 'तो', 'आप', 'भी', 'नहीं', 'छोडेंगे', '।', '"', 'गांधीजी', 'ने', 'तुरन्त', 'प्रसÙ', 'होकर', 'कहा', '.', '"', 'तुम']

