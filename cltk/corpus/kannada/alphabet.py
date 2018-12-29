"""Kannada is a Dravidian language spoken predominantly in Karnataka state
of India. It has 49 characters but the written symbols are much more
than 49 as different characters are combined to form compound characters.

The characters can be divided into 3 categories:
    1. Swaras (Vowels) : 13 in modern Kannada and 14 in Classical
    2. Vynjanas (Consonants) : They are further divided into 2 categories:
         i) Structured Consonants : 25
        ii) Unstructured Consonants : 9 in modern Kannada and 11 in Classical
    3. Yogavaahakas (part vowel, part consonant) : 2

Corresponding to each Swaras and Yogavaahakas there is a symbol.
Thus Consonant + Vowel Symbol = Kagunita
"""


VOWELS = [
    'ಅ', 'ಆ', 'ಇ', 'ಈ', 'ಉ', 'ಊ', 'ಋ',
    'ೠ', 'ಎ', 'ಏ', 'ಐಒ', 'ಒ', 'ಓ', 'ಔ']

YOGAVAAHAKAS = ['ಅಂ', 'ಅಃ']

STRUCTURED_CONSONANTS = [
    'ಕ', 'ಖ', 'ಗ', 'ಘ', 'ಙಚ',
    'ಚ', 'ಛ', 'ಜ', 'ಝ', 'ಞ',
    'ಟ', 'ಠ', 'ಡ', 'ಢ', 'ಣ',
    'ತ', 'ಥ', 'ದ', 'ಧ', 'ನ',
    'ಪ', 'ಫ', 'ಬ', 'ಭ', 'ಮ']

UNSTRUCTURED_CONSONANTS = [
    'ಯ', 'ರ', 'ಱ', 'ಲ', 'ವ', 'ಶ',
    'ಷ', 'ಸ', 'ಹ', 'ಳ', 'ೞ']

# NUMERALS from 0 - 9

NUMERALS = [
    '೦', '೧', '೨', '೩', '೪',
    '೫', '೬', '೭', '೮', '೯']

VOWEL_SIGNS = [
    '', 'ಾ', 'ಿ', 'ೀ', 'ು',
    'ೂ', 'ೃ', 'ೆ', 'ೇ', 'ೈ',
    'ೊ', 'ೋ', 'ೌ', 'ಂ', 'ಃ']
