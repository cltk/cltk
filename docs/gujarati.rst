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

   # Digits 

   In[1]: from cltk.corpus.gujarati.alphabet import DIGITS

   In[2]: print(DIGITS)
   Out[2]:  ['૦','૧','૨','૩','૪','૫','૬','૭','૮','૯','૧૦']
   
   # Velar consonants
   
   In[3]: from cltk.corpus.gujarati.alphabet import VELAR_CONSONANTS
   
   In[4]: print(VELAR_CONSONANTS)
   Out[4]: [ 'ક' , 'ખ' , 'ગ' , 'ઘ' , 'ઙ' ]
   
   # Palatal consonants
   
   In[5]: from cltk.corpus.gujarati.alphabet import PALATAL_CONSONANTS
   
   In[6]: print(PALATAL_CONSONANTS)
   Out[6]: ['ચ' , 'છ' , 'જ' , 'ઝ' , 'ઞ' ]
   
   # Retroflex consonants
   
   In[7]: from cltk.corpus.gujarati.alphabet import RETROFLEX_CONSONANTS
   
   In[8]: print(RETROFLEX_CONSONANTS)
   Out[8]: ['ટ' , 'ઠ' , 'ડ' , 'ઢ' , 'ણ']
   
   # Dental consonants
   
   In[9]: from cltk.corpus.gujarati.alphabet import DENTAL_CONSONANTS
   
   In[10]: print(DENTAL_CONSONANTS)
   Out[10]: ['ત' , 'થ' , 'દ' , 'ધ' , 'ન' ]
   
   # Labial consonants
   
   In[11]: from cltk.corpus.gujarati.alphabet import LABIAL_CONSONANTS
   
   In[12]: print(LABIAL_CONSONANTS)
   Out[12]: ['પ' , 'ફ' , 'બ' , 'ભ' , 'મ']
  
There are 4 sonorant consonants in Gujarati:

.. code-block:: python

   # Sonorant consonants
   
   In[1]: from cltk.corpus.gujarati.alphabet import SONORANT_CONSONANTS

   In[2]: print(SONORANT_CONSONANTS)
   Out[2]: ['ય' , 'ર' , 'લ' , 'વ']
   
There are 3 sibilants in Gujarati: 

.. code-block:: python

   # Sibilant consonants
   
   In[1]: from cltk.corpus.gujarati.alphabet import SIBILANT_CONSONANTS 
   
   In[2]: print(SIBILANT_CONSONANTS)
   Out[2]: ['શ' , 'ષ' , 'સ']
   
There is one guttural consonant also:

.. code-block:: python

   # Guttural consonant
   
   In[1]: from cltk.corpus.gujarati.alphabet import GUTTURAL_CONSONANT 
   
   In[2]: print(GUTTURAL_CONSONANTS)
   Out[2]:['હ']
   
There are also three additional consonants in Gujarati: 

.. code-block:: python

   # Additional consonants
   
   In[1]: from cltk.corpus.gujarati.alphabet import ADDITIONAL_CONSONANTS

   In[2]: print(ADDITIONAL_CONSONANTS)
   Out[2]: ['ળ' , 'ક્ષ' , 'જ્ઞ']
   
  



