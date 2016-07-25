"""Data module for the Punjabi languages alphabet and related characters."""

__author__ = 'Nimit Bhardwaj <nimitbhardwaj@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

#The Functions Needed for making the data of alphabets is here

#The Digits are given under, the given list starts from 0 to 9, that is
#the index of the list tell the digit in punjabi

DIGITS = ['੦', '੧', '੨', '੩', '੪', '੫', '੬', '੭', '੮', '੯']

#Below are the independent vowels of the punjabi language.
#They give the sound aaa, e, ee, u, uuu, ea, eaa, o, ou
#These vowels are the base of the dependent vowels
INDEPENDENT_VOWELS = ['ਆ', 'ਇ', 'ਈ', 'ਉ', 'ਊ', 'ਏ', 'ਐ', 'ਓ', 'ਔ']

#The given are the dependent vowels, these are added after or on the consonants

DEPENDENT_VOWELS = ['ਾ', 'ਿ', 'ੀ', 'ੁ', 'ੂ', 'ੇ', 'ੈ', 'ੋ', 'ੌ']


#Below are the consonants of the punjabi language.
#except first 3 consonants in first row, all other are used in normal writting

CONSONANTS = ['ੳ', 'ਅ', 'ੲ', 'ਸ', 'ਹ',\
              'ਕ', 'ਖ', 'ਗ', 'ਘ', 'ਙ',\
              'ਚ', 'ਛ', 'ਜ', 'ਝ', 'ਞ',\
              'ਟ', 'ਠ', 'ਡ', 'ਢ', 'ਣ',\
              'ਤ', 'ਥ', 'ਦ', 'ਧ', 'ਨ',\
              'ਪ', 'ਫ', 'ਬ', 'ਭ', 'ਮ',\
              'ਯ', 'ਰ', 'ਲ', 'ਵ', 'ੜ']
#As shown under only a dot is added to some of the consonants, this dot is
#known as the bindi in hindi or punjabi, they change the sound of the
#consonant like , ਜ is for 'j' sound, while ਜ਼ is for 'z' sound
BINDI_CONSONANTS = ['ਖ਼', 'ਗ਼', 'ਜ਼', 'ਫ਼', 'ਲ਼', 'ਸ਼']

#Here are some other symbols that are used in punjabi

OTHER_SYMBOLS = ['ੱ', 'ਂ', 'ਃ', 'ੰ', 'ੑ', 'ੴ', 'ਁ']
#Now here is the explanation of these symbols, symbol at index 0 is addak, it halfens the
#sound, at 2 is bindi on the alphabet, it gives a nasal sound, then symbol at
#index 4 gives a ha sound, then at index 4 is tippi does almost same function as bindi above
#, then is halant cuts the natural vowel sound, then is Ek Omkar, meaning God is One.


#Here is a note that all the alphabets can be made by adding the consonant with the dependent vowel sound or with some other symbols
