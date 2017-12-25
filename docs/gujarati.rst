Gujarati
******

Gujarati is an Indo-Aryan language native to the Indian state of Gujarat. It
is part of the greater Indo-European language family. Gujarati is descended from Old
Gujarati (circa 1100–1500 AD). In India, it is the official language in the state of
Gujarat, as well as an official language in the union territories of Daman and Diu and
Dadra and Nagar Haveli.Gujarati is spoken by 4.5% of the Indian population, which amounts
to 46 million speakers in India.Altogether, there are about 50 million speakers of Gujarati
worldwide.(Source: `Wikipedia <https://en.wikipedia.org/wiki/Gujarati_language>`_) 

Alphabet
=========

The Gujarati alphabets are placed in `cltk/corpus/gujarati/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/gujarati/alphabet.py>`_.

There are 13 vowels in Gujarati. Like Hindi and other similar languages, vowels in Gujarati
have an independent form and a matra form used to modify consonants in word formation.

``VOWELS = [ 'અ' , 'આ' , 'ઇ' , 'ઈ' , 'ઉ' , 'ઊ' , 'ઋ' , 'એ' , 'ઐ' , 'ઓ' , 'ઔ' , 'અં' , 'અઃ'  ]``

The International Alphabet of Sanskrit Transliteration (I.A.S.T.) is a transliteration scheme that
allows the lossless romanization of Indic scripts as employed by Sanskrit and related Indic languages.
IAST makes it possible for the reader to read the Indic text unambiguously, exactly as if it were
in the original Indic script.

``IAST_VOWELS_REPRESENTATION = ['a', 'ā', 'i', 'ī', 'u', 'ū','ṛ','e','ai','o','au','ṁ','ḥ']``

There are 33 consonants. They are grouped in accordance with the traditional Sanskrit scheme of 
arrangement.

1. Velar: A velar consonant is a consonant that is pronounced with the back part of the tongue against
the soft palate, also known as the velum, which is the back part of the roof of the mouth (e.g., ``k``).

2. Palatal: A palatal consonant is a consonant that is pronounced with the body (the middle part) of the
tongue against the hard palate (which is the middle part of the roof of the mouth) (e.g., ``j``).

3. Retroflex: A retroflex consonant is a coronal consonant where the tongue has a flat, concave, or even
curled shape, and is articulated between the alveolar ridge and the hard palate (e.g., English ``t``).

4. Dental: A dental consonant is a consonant articulated with the tongue against the 
upper teeth (e.g., Spanish ``t``).

5. Labial: Labials or labial consonants are articulated or made with the lips (e.g., ``p``).

.. code-block:: python

   VELAR_CONSONANTS = [ 'ક' , 'ખ' , 'ગ' , 'ઘ' , 'ઙ' ]

   PALATAL_CONSONANTS = ['ચ' , 'છ' , 'જ' , 'ઝ' , 'ઞ' ]

   RETROFLEX_CONSONANTS = ['ટ' , 'ઠ' , 'ડ' , 'ઢ' , 'ણ']

   DENTAL_CONSONANTS = ['ત' , 'થ' , 'દ' , 'ધ' , 'ન' ]

   LABIAL_CONSONANTS = ['પ' , 'ફ' , 'બ' , 'ભ' , 'મ']
   
   IAST_VELAR_CONSONANTS = ['k', 'kh', 'g', 'gh', 'ṅ']
   
   IAST_PALATAL_CONSONANTS = ['ch', 'chh', 'j', 'jh', 'ñ']
   
   IAST_RETROFLEX_CONSOnANTS = ['ṭ', 'ṭh', 'ḍ', 'ḍh', 'ṇ']
   
   IAST_DENTAL_CONSONANTS = ['t', 'th', 'd', 'dh', 'n']
   
   IAST_LABIAL_CONSONANTS = ['p', 'ph', 'b', 'bh', 'm']
   
There are 4 sonorant consonants in Gujarati:

.. code-block:: python

   SONORANT_CONSONANTS = ['ય' , 'ર' , 'લ' , 'વ']
   
   IAST_SONORANT_CONSONANTS = ['y', 'r', 'l', 'v']
   
There are 3 sibilants in Gujarati: 

.. code-block:: python

   SIBILANT_CONSONANTS = ['શ' , 'ષ' , 'સ']
   
   IAST_SIBILANT_CONSONANTS = ['ś', 'ṣ', 's']
   
There is one guttural consonant also:

.. code-block:: python

   GUTTURAL_CONSONANT = ['હ']
   
   IAST_GUTTURAL_CONSONANT = ['h']
   
There are also three additional consonants in Gujarati: 

.. code-block:: python

   ADDITIONAL_CONSONANTS = ['ળ' , 'ક્ષ' , 'જ્ઞ']
   
   IAST_ADDITIONAL_CONSONANTS = ['ḷ' , 'kṣ' , 'gñ']




