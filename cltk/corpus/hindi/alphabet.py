
"""HINDI is an Indic language which uses DEVNAGRI scriptderiving from Brahmi script.
script is also used to write other languages, including
Hindi is directly derived from sanskrit and is common language of medivieal texts from north India. The vowels
themselves can be divided into dependent and independent vowels"""



# The digits in hindi from index 0 to 9.

DIGITS = ['०','१','२','३','४','५','६','७','८','९']

VOWELS = ['अ','आ','इ','ई','उ','ऊ','ऋ','ए','ऐ','ओ','औ']

DEPENDENT_VOWELS = ['◌া','ি','◌ী','◌ু','◌ূ','◌ৃ','ে','ৈ','ো','ৌ']
#following are the general consonants
CONSONANTS = ['क','ख','ग','घ','ङ','च','छ','ज','झ','ञ','ट','ठ','ड','ढ','ण','त','थ','द', 'ध', 'न', 'प','फ','ब','भ','म']

#following are modified constants
Modified_constants = ['क़', 'ग़', 'ख़', 'ज़', 'ड़', 'ढ़', 'फ़']


#the Semivowels are also in the script of hindi
SEMIVOWELS = ['य ','र ','ल' ,'व']    

#There are three sibilants:
SIBILANTS = ['श','ष','स']

FRICATIVE = ['ह']

# Anusvara is used for final velar nasal sound, Visarga adds voiceless breath after vowel and Candrabindu is used to nasalize vowels 

MODIFIERS = ['◌্','◌ঁ','◌ং','◌ঃ']
