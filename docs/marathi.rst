Marathi
*******
Marathi is an Indian language spoken predominantly by the Marathi people of Maharashtra. Marathi has some of the oldest literature of all modern Indo-Aryan languages, dating from about 900 AD. Early Marathi literature written during the Yadava (850-1312 CE) was mostly religious and philosophical in nature. Dnyaneshwar (1275–1296) was the first Marathi literary figure who had wide readership and profound influence. His major works are Amrutanubhav and Bhavarth Deepika (popularly known as Dnyaneshwari), a 9000-couplet long commentary on the Bhagavad Gita. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Marathi_language>`_)


Corpora
=======
Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``Marathi_``) to discover available Marathi corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('Marathi')

   In [3]: c.list_corpora
   Out[3]:
   ['Marathi_text_wikisource']


Tokenizer
=========

.. code-block:: python

   In [1]: from cltk.tokenize.sentence import TokenizeSentence

   In [2]: tokenizer = TokenizeSentence('marathi')

   In [3]: sentence = "आतां विश्वात्मके देवे, येणे वाग्यज्ञे तोषावे, तोषोनि मज द्यावे, पसायदान हे"

   In [4]: tokenized_sentence = tokenizer.tokenize(sentence)

   In [5]: print(tokenized_sentence)
   ['आतां', 'विश्वात्मके', 'देवे', ',', 'येणे', 'वाग्यज्ञे', 'तोषावे', ',', 'तोषोनि', 'मज', 'द्यावे', ',', 'पसायदान', 'हे']


Stopwords
=========
Stop words of classical marathi calculated from "dnyaneshwari" and "Haripath".

.. code-block:: python

    In [1]: from cltk.stop.marathi.stops import STOP_LIST

    In [2]: print(STOP_LIST[1])
    "तरी"


Alphabet
=========

The alphabets of Marathi language are placed in cltk/corpus/Marathi/alphabet.py.

.. code-block:: python

   In [1]: from cltk.corpus.marathi.alphabet import DIGITS

   In [2]: print(DIGITS)
   ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९']


There are 13 vowels in Marathi. All vowels have their independent form and a matra form, which are used for modifying consonants: ``VOWELS = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ', 'ओ', 'औ', 'अॅ', 'ऑ']``.

The International Alphabet of Sanskrit Transliteration (I.A.S.T.) is a transliteration scheme that allows the lossless \
romanization of Indic scripts as employed by Sanskrit and related Indic languages. \
IAST makes it possible for the reader to read the Indic text unambiguously, exactly as if it were in the original Indic script. The vowels would be represented thus: ``IAST_REPRESENTATION_VOWELS = ['a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'e', 'ai', 'o', 'au', 'ae', 'ao']``.

.. code-block:: python

   In [1]: from cltk.corpus.marathi.alphabet import VOWELS

   In [2]: VOWELS

   Out[2]: ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ', 'ओ', 'औ', 'अॅ', 'ऑ']

   In [3]: from cltk.corpus.marathi.alphabet import IAST_REPRESENTATION_VOWELS

   In [4]: IAST_REPRESENTATION_VOWELS

   out[4]: ['a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'e', 'ai', 'o', 'au', 'ae', 'ao']


Similarly we can import others vowels and consonants. There are 25 regular consonants (consonants that stop air from moving out of the mouth) in Marathi, and they are organized into groups ("vargas") of five. The vargas are ordered according to where the tongue is in the mouth. Each successive varga refers to a successively forward position of the tongue. The vargas are ordered and named thus (with an example of a corresponding consonant):

1. Velar: A velar consonant is a consonant that is pronounced with the back part of the tongue against the soft palate, also known as the velum, which is the back part of the roof of the mouth (e.g., ``k``).

2. Palatal: A palatal consonant is a consonant that is pronounced with the body (the middle part) of the tongue against the hard palate (which is the middle part of the roof of the mouth) (e.g., ``j``).

3. Retroflex: A retroflex consonant is a coronal consonant where the tongue has a flat, concave, or even curled shape, and is articulated between the alveolar ridge and the hard palate (e.g., English ``t``).

4. Dental: A dental consonant is a consonant articulated with the tongue against the upper teeth (e.g., Spanish ``t``).

5. Labial: Labials or labial consonants are articulated or made with the lips (e.g., ``p``).

.. code-block:: python

   VELAR_CONSONANTS = ['क', 'ख', 'ग', 'घ', 'ङ']

   PALATAL_CONSONANTS = ['च', 'छ', 'ज', 'झ', 'ञ']

   RETROFLEX_CONSONANTS = ['ट','ठ', 'ड', 'ढ', 'ण']

   DENTAL_CONSONANTS = ['त', 'थ', 'द', 'ध', 'न']

   LABIAL_CONSONANTS = ['प', 'फ', 'ब', 'भ', 'म']

   IAST_VELAR_CONSONANTS = ['k', 'kh', 'g', 'gh', 'ṅ']

   IAST_PALATAL_CONSONANTS = ['c', 'ch', 'j', 'jh', 'ñ']

   IAST_RETROFLEX_CONSONANTS = ['ṭ', 'ṭh', 'ḍ', 'ḍh', 'ṇ']

   IAST_DENTAL_CONSONANTS = ['t', 'th', 'd', 'dh', 'n']

   IAST_LABIAL_CONSONANTS = ['p', 'ph', 'b', 'bh', 'm']

There are four semi vowels in Marathi:

.. code-block:: python

   SEMI_VOWELS = ['य', 'र', 'ल', 'व']

   IAST_SEMI_VOWELS = ['y', 'r', 'l', 'w']

There are three sibilants in Marathi:

.. code-block:: python

   SIBILANTS = ['श', 'ष', 'स']

   IAST_SIBILANTS = ['ś', 'ṣ', 's']

There is one fricative consonant in Marathi:

.. code-block:: python

   FRIACTIVE_CONSONANTS = ['ह']

   IAST_FRIACTIVE_CONSONANTS = ['h']

There are three additional consonants:

.. code-block:: python

   ADDITIONAL_CONSONANTS = ['ळ', 'क्ष', 'ज्ञ']

   IAST_ADDITIONAL_CONSONANTS = ['La', 'kSha', 'dnya']
