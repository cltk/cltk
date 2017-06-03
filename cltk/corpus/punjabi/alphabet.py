"""Data module for the Punjabi languages alphabet and related characters."""

__author__ = ['Nimit Bhardwaj <nimitbhardwaj@gmail.com>', 'Talha Javed Mukhtar <tjaved.bscs15seecs@seecs.edu.pk']
__license__ = 'MIT License. See LICENSE.'


#The Functions Needed for making the data of alphabets is here

#The Digits are given under, the given list starts from 0 to 9, that is
#the index of the list tell the digit in punjabi
DIGITS_GURUMUKHI = ['੦', '੧', '੨', '੩', '੪', '੫', '੬', '੭', '੮', '੯']
DIGITS_SHAHMUKHI = ['۰', '۱', '۲', '۳', '٤', '۵', '٦', '۷', '۸', '۹']

#Below are the independent vowels of the punjabi language in gurumukhi script.
#They give the sound aaa, e, ee, u, uuu, ea, eaa, o, ou
#These vowels are the base of the dependent vowels
INDEPENDENT_VOWELS_GURUMUKHI = ['ਆ', 'ਇ', 'ਈ', 'ਉ', 'ਊ', 'ਏ', 'ਐ', 'ਓ', 'ਔ']
#There are four independent vowels in the shahmukhi script, which can also be joined with consonants
INDEPENDENT_VOWELS_SHAHMUKHI = ['ا', 'و', 'ی', 'ے']


#The given are the dependent vowels, these are added after or on the consonants
DEPENDENT_VOWELS_GURUMUKHI = ['ਾ', 'ਿ', 'ੀ', 'ੁ', 'ੂ', 'ੇ', 'ੈ', 'ੋ', 'ੌ']
#In the shahmukhi script, the following dependent vowels perform the action of diacritics
DEPENDENT_VOWELS_SHAHMUKHI = ['َ', 'ِ', 'ُ']


#Below are the consonants of the punjabi language in gurumukhi script.
#except first 3 consonants in first row, all other are used in normal writting
CONSONANTS_GURUMUKHI = ['ੳ', 'ਅ', 'ੲ', 'ਸ', 'ਹ',\
              			'ਕ', 'ਖ', 'ਗ', 'ਘ', 'ਙ',\
              			'ਚ', 'ਛ', 'ਜ', 'ਝ', 'ਞ',\
		              	'ਟ', 'ਠ', 'ਡ', 'ਢ', 'ਣ',\
		              	'ਤ', 'ਥ', 'ਦ', 'ਧ', 'ਨ',\
		              	'ਪ', 'ਫ', 'ਬ', 'ਭ', 'ਮ',\
		              	'ਯ', 'ਰ', 'ਲ', 'ਵ', 'ੜ']
#The following are the consonants in shahmukhi script
CONSONANTS_SHAHMUKHI = ['ء', 'ب', 'پ', 'ت', 'ٹ',\
						'ث', 'ج', 'چ', 'ح', 'خ',\
						'د', 'ڈ', 'ذ', 'ر', 'ڑ',\
					    'ز', 'ژ', 'س', 'ش', 'ص',\
						'ض', 'ط', 'ظ', 'ع', 'غ',\
						'ف', 'ق', 'ک', 'گ', 'ل',\
						'م', 'ن', 'ه', 'ھ']


#In gurumukhi script, only a dot is added to some of the consonants, this dot is
#known as the bindi in hindi or punjabi, they change the sound of the
#consonant like , ਜ is for 'j' sound, while ਜ਼ is for 'z' sound
BINDI_CONSONANTS_GURUMUKHI = ['ਖ਼', 'ਗ਼', 'ਜ਼', 'ਫ਼', 'ਲ਼', 'ਸ਼']

#Here are some other symbols that are used in punjabi

OTHER_SYMBOLS_GURUMUKHI = ['ੱ', 'ਂ', 'ਃ', 'ੰ', 'ੑ', 'ੴ', 'ਁ']
#Now here is the explanation of these symbols, symbol at index 0 is addak, it halfens the
#sound, at 2 is bindi on the alphabet, it gives a nasal sound, then symbol at
#index 4 gives a ha sound, then at index 4 is tippi does almost same function as bindi above
#, then is halant cuts the natural vowel sound, then is Ek Omkar, meaning God is One.

OTHER_SYMBOLS_SHAHMUKHI = ['ﺁ', 'ۀ', 'ﻻ']

#Here is a note that all the alphabets can be made by adding the consonant with the dependent vowel sound or with some other symbols
