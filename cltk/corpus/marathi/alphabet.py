"""Data module for the Marathi languages alphabet and related characters.

Marathi is written in Devnagari script
"""

__author__ = ['Mahesh Bhosale <bhosalems24@gmail.com>']
__license__ = ['MIT License. See LICENSE.']


#DIGITS
#0 to 9
DIGITS = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९']

#VOWELS
#There are 13 vowels in Marathi,
#All vowels have their indepenedent form and a matra form, which are used for modifying consonents

VOWELS = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ', 'ओ', 'औ', 'अॅ', 'ऑ']

#Using the International Alphabet of Sanskrit Transliteration (IAST), these vowels would be represented thus:
IAST_REPRESENTATION_VOWELS = ['a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'e', 'ai', 'o', 'au', 'ae', 'ao']

#CONSONENTS
#There are 25 regular consonants (consonants that stop air from moving out of the mouth) in Marathi, and they
# are organized into groups (vargas) of five. The vargas are ordered according to where the tongue is in the mouth.
# Each successive varga refers to a successively forward position of the tongue. The vargas are ordered and named thus
# (with an example of a corresponding consonant):
# 1.Velar (e.g. k)
# 2.Palatal (e.g. j)
# 3.Retroflex (e.g. English t)
# 4.Dental (e.g. Spanish t)
# 5.Labial (e.g. p)

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

#SEMI_VOWELS
#There are four semi vowels in marathi

SEMI_VOWELS = ['य', 'र', 'ल', 'व']
IAST_SEMI_VOWELS = ['y', 'r', 'l', 'w']

#SIBILANTS
#There are three sibilants in marathi

SIBILANTS = ['श', 'ष', 'स']
IAST_SIBILANTS = ['ś', 'ṣ', 's']

#FRIACTICE_CONSTANT
#There is one fricative consonant in marathi

FRIACTIVE_CONSONANTS = ['ह']
IAST_FRIACTIVE_CONSONANTS = ['h']

#ADDITIONAL_CONSTANTS
#There are three additional consonants:

ADDITIONAL_CONSONANTS = ['ळ', 'क्ष', 'ज्ञ']
IAST_ADDITIONAL_CONSONANTS = ['La', 'kSha', 'dnya']
