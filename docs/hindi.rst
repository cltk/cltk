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
   
   
Alphabet
========

HINDI is an Indic language which uses **Devanagari** script derived from Brahmi script. The Devanagari script is used for over 120 languages, making it one of the most used and `adopted writing systems <https://en.wikipedia.org/wiki/List_of_writing_systems_by_adoption>`_ in the world.

Devanagari script has forty-seven primary characters, of which fourteen are vowels and thirty-three are consonants.
The script has no distinction similar to the capital and small letters of the Latin alphabet. Generally the orthography of the script reflects the pronunciation of the language.

.. code-block:: python

   In [1]: from cltk.corpus.hindi.alphabet import *
   #Listing Numerals used in Hindi.
   In [11]: DIGITS
   Out[11]: ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९']

   #Listing primary vowels.
   In [12]: VOWELS
   Out[12]: ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ', 'ओ', 'औ']

   #Listing dependent vowels (मात्रा).
   In [13]: DEPENDENT_VOWELS
   Out[13]: ['ऺ','ऻ' ,'़' ,'ऽ' ,'ा' ,'ि', 'ी','ु' ,'ू' ,'.ृ' ,'ॄ','ॅ', 'ॆ', 'े','ै' ,'ॉ' ,' ॊ', 'ो' 
            ,'ौ' ,'्' ,'ॏ']
   
   #Listing of primary consonants.
   In [14]: CONSONANTS
   Out[14]: ['क','ख','ग','घ','ङ','च','छ','ज','झ','ञ','ट','ठ','ड','ढ','ण','त','थ','द', 'ध', 
            'न', 'प','फ','ब','भ','म']
 
   
   #Listing of modified consonants.
   In [15]: MODIFIED_CONSONANTS
   Out[15]: ['क़', 'ग़', 'ख़', 'ज़', 'ड़', 'ढ़', 'फ़', 'य़', 'ऱ', 'ळ', 'ऴ']
   
   #Listing of semivowels.
   In [16]: SEMIVOWELS
   Out[16]: ['य ', 'र ', 'ल', 'व']
   
   #Listing of sibilants and fricative
   In [17]: SIBILANTS
   Out[17]: ['श', 'ष', 'स']

   In [18]: FRICATIVE
   Out[18]: ['ह']

   #Listing of modifiers
   # Anusvara is used for final velar nasal sound, Visarga adds voiceless breath after vowel and Candrabindu is used to nasalize vowels.
   In [19]: MODIFIERS
   Out[19]: ['◌্', '◌ঁ', '◌ং', '◌ঃ']

   #Listing of sign.
   # About Om:- Om is part of the iconography found in ancient and medieval era manuscripts, temples, monasteries and spiritual retreats in Hinduism, Buddhism, and Jainism.The symbol has a spiritual meaning in all Indian dharmas, but the meaning and connotations of Om vary between the diverse schools within and across the various traditions.
   In [20]: SIGNS
   Out[20]: ['ॐ']


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

