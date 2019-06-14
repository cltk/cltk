"""Data module for the Punjabi languages alphabet and related characters.

There are two scripts used in Punjabi: Gurmukhi (having its origins in the Brahmi) and Shahmukhi (which a Perso-Arabic script).
"""

__author__ = ['Nimit Bhardwaj <nimitbhardwaj@gmail.com>', 'Talha Javed Mukhtar <tjaved.bscs15seecs@seecs.edu.pk>']
__license__ = 'MIT License. See LICENSE.'


# 0 through 9
DIGITS_GURMUKHI = ['੦', '੧', '੨', '੩', '੪', '੫', '੬', '੭', '੮', '੯']
DIGITS_SHAHMUKHI = ['۰', '۱', '۲', '۳', '٤', '۵', '٦', '۷', '۸', '۹']

# independent vowels
# These are the base of the dependent vowels
# They give the sounds: aaa, e, ee, u, uuu, ea, eaa, o, ou
INDEPENDENT_VOWELS_GURMUKHI = ['ਆ', 'ਇ', 'ਈ', 'ਉ', 'ਊ', 'ਏ', 'ਐ', 'ਓ', 'ਔ']
INDEPENDENT_VOWELS_SHAHMUKHI = ['ا', 'و', 'ی', 'ے']

# dependent vowels
# these are added after or on the consonants
DEPENDENT_VOWELS_GURMUKHI = ['ਾ', 'ਿ', 'ੀ', 'ੁ', 'ੂ', 'ੇ', 'ੈ', 'ੋ', 'ੌ']
# In the shahmukhi script, the following dependent vowels perform the action of diacritics
DEPENDENT_VOWELS_SHAHMUKHI = ['َ', 'ِ', 'ُ']

# consonants
# except first 3 consonants in first row, all other are used in normal writing
CONSONANTS_GURMUKHI = ['ੳ', 'ਅ', 'ੲ', 'ਸ', 'ਹ',
                        'ਕ', 'ਖ', 'ਗ', 'ਘ', 'ਙ',
                        'ਚ', 'ਛ', 'ਜ', 'ਝ', 'ਞ',
                        'ਟ', 'ਠ', 'ਡ', 'ਢ', 'ਣ',
                        'ਤ', 'ਥ', 'ਦ', 'ਧ', 'ਨ',
                        'ਪ', 'ਫ', 'ਬ', 'ਭ', 'ਮ',
                        'ਯ', 'ਰ', 'ਲ', 'ਵ', 'ੜ']
CONSONANTS_SHAHMUKHI = ['ء', 'ب', 'پ', 'ت', 'ٹ',
                        'ث', 'ج', 'چ', 'ح', 'خ',
                        'د', 'ڈ', 'ذ', 'ر', 'ڑ',
                        'ز', 'ژ', 'س', 'ش', 'ص',
                        'ض', 'ط', 'ظ', 'ع', 'غ',
                        'ف', 'ق', 'ک', 'گ', 'ل',
                        'م', 'ن', 'ه', 'ھ']

# consonants
# As shown under only a dot is added to some of the consonants, this dot is
# known as the bindi in hindi or punjabi, they change the sound of the
# consonant like , ਜ is for 'j' sound, while ਜ਼ is for 'z' sound
BINDI_CONSONANTS_GURMUKHI = ['ਖ਼', 'ਗ਼', 'ਜ਼', 'ਫ਼', 'ਲ਼', 'ਸ਼']

# other symbols
OTHER_SYMBOLS_GURMUKHI = ['ੱ', 'ਂ', 'ਃ', 'ੰ', 'ੑ', 'ੴ', 'ਁ']
OTHER_SYMBOLS_SHAHMUKHI = ['ﺁ', 'ۀ', 'ﻻ']
