"""Every phonetic of every language is given similar positions in the vectors. Therefore transliterations
happen when each offset is calculated relative to the ranges of the languages specified.
Every phonetic has a dedicated phonetic vector which describes all the facets of the character, whether it is
a vowel or a consonant whe ther it has a halanta, etc.

Source: https://github.com/anoopkunchukuttan/indic_nlp_library/blob/master/src/indicnlp/script/indic_scripts.py
"""

import os
import csv

try:
    import numpy as np
except ImportError:
    print('"numpy" is not installed.')
    raise

__author__ = ['Anoop Kunchukuttan <anoop.kunchukuttan@gmail.com>']
__license__ = 'GPLv3'


# Indexes into the phonetic vector
PVIDX_BT_VOWEL = 0
PVIDX_BT_CONSONANT = 1
PVIDX_BT_NUKTA = 2
PVIDX_BT_HALANT = 3
PVIDX_BT_ANUSVAAR = 4
PVIDX_BT_MISC = 5
PVIDX_BT_S = PVIDX_BT_VOWEL
PVIDX_BT_E = PVIDX_BT_MISC + 1

PVIDX_VSTAT_DEP = 12

LC_TA = 'ta'

LANGUAGE_NAME_TO_CODE = {'hindi': 'hi', 'sanskrit': 'sa', 'punjabi': 'pa', 'gujarati': 'gu', 'oriya': 'or',
                         'tamil': 'ta', 'telegu': 'te', 'kannada': 'kn', 'malayalam': 'ml', 'sinhalese': 'si',
                         'marathi': 'mr', 'konkan': 'kk', 'nepali': 'ne', 'sindhi': 'sd', 'bengali': 'bn',
                         'assamese': 'as'}


# The phonetics of every script exist in the ranges of the dictionary mentioned below
SCRIPT_RANGES = {
    'pa': [0x0a00, 0x0a7f],
    'gu': [0x0a80, 0x0aff],
    'or': [0x0b00, 0x0b7f],
    'ta': [0x0b80, 0x0bff],
    'te': [0x0c00, 0x0c7f],
    'kn': [0x0c80, 0x0cff],
    'ml': [0x0d00, 0x0d7f],
    'si': [0x0d80, 0x0dff],
    'hi': [0x0900, 0x097f],
    'mr': [0x0900, 0x097f],
    'kk': [0x0900, 0x097f],
    'sa': [0x0900, 0x097f],
    'ne': [0x0900, 0x097f],
    'sd': [0x0900, 0x097f],
    'bn': [0x0980, 0x09ff],
    'as': [0x0980, 0x09ff],
}

COORDINATED_RANGE_START_INCLUSIVE = 0
COORDINATED_RANGE_END_INCLUSIVE = 0x6f

PV_PROP_RANGES = dict(basic_type=[0, 6], vowel_length=[6, 8], vowel_strength=[8, 11], vowel_status=[11, 13],
                      consonant_type=[13, 18], articulation_place=[18, 23], aspiration=[23, 25], voicing=[25, 27],
                      nasalization=[27, 29], vowel_horizontal=[29, 32], vowel_vertical=[32, 36],
                      vowel_roundness=[36, 38])

PHONETIC_VECTOR_START_OFFSET = 6


class Syllabifier:
    """Class for syllabalizing Indian language words."""

    def __init__(self, lang_name):
        """Setup values."""

        self.lang_name = lang_name
        assert self.lang_name in LANGUAGE_NAME_TO_CODE.keys(), 'Language not available'
        self.lang = LANGUAGE_NAME_TO_CODE[lang_name]

        assert self.lang in SCRIPT_RANGES.keys()

        self.all_phonetic_data, self.tamil_phonetic_data, self.all_phonetic_vectors, self.tamil_phonetic_vectors, self.phonetic_vector_length = self.get_lang_data()

    def get_lang_data(self):
        """Define and call data for future use. Initializes and defines all
        variables which define the phonetic vectors.
        """

        csv_dir_path = get_cltk_data_dir() + '/sanskrit/model/sanskrit_models_cltk/phonetics'

        all_phonetic_csv = os.path.join(csv_dir_path, 'all_script_phonetic_data.csv')
        tamil_csv = os.path.join(csv_dir_path, 'tamil_script_phonetic_data.csv')

        # Make helper function for this
        with open(all_phonetic_csv,'r') as f:
            reader = csv.reader(f, delimiter = ',', quotechar = '"')
            next(reader, None) # Skip headers
            all_phonetic_data = [row for row in reader]

        with open(tamil_csv,'r') as f:
            reader = csv.reader(f, delimiter = ',', quotechar = '"')
            next(reader, None) # Skip headers
            # tamil_phonetic_data = [row[PHONETIC_VECTOR_START_OFFSET:] for row in reader]
            tamil_phonetic_data = [row for row in reader]

        # Handle better?
        all_phonetic_data = [[int(cell) if cell=='0' or cell=='1' else cell for cell in row] for row in all_phonetic_data]
        tamil_phonetic_data = [[int(cell) if cell=='0' or cell=='1' else cell for cell in row] for row in tamil_phonetic_data]

        all_phonetic_vectors = np.array([row[PHONETIC_VECTOR_START_OFFSET:] for row in all_phonetic_data])
        tamil_phonetic_vectors = np.array([row[PHONETIC_VECTOR_START_OFFSET:] for row in tamil_phonetic_data])

        phonetic_vector_length = all_phonetic_vectors.shape[1]

        return all_phonetic_data, tamil_phonetic_data, all_phonetic_vectors, tamil_phonetic_vectors, phonetic_vector_length

    @staticmethod
    def in_coordinated_range_offset(c_offset):
        """Applicable to Brahmi derived Indic scripts. Used to determine
        whether offset is of a  alphabetic character or not.
        """
        return COORDINATED_RANGE_START_INCLUSIVE <= c_offset <= COORDINATED_RANGE_END_INCLUSIVE

    def get_offset(self, c, lang):
        """Gets the offset; that is the relative position in the range of the
        specified language.
        """
        return ord(c) - SCRIPT_RANGES[lang][0]

    def invalid_vector(self):
        """Returns an zero array of length 38"""
        return np.array([0] * self.phonetic_vector_length)

    def get_phonetic_info(self, lang):
        """For a specified language (lang), it returns the matrix and the vecto
         containing specifications of the characters.
         """
        phonetic_data = self.all_phonetic_data if lang != LC_TA else self.tamil_phonetic_data
        phonetic_vectors = self.all_phonetic_vectors if lang != LC_TA else self.tamil_phonetic_vectors

        return phonetic_data, phonetic_vectors

    def get_phonetic_feature_vector(self, c, lang):
        """For a given character in a language, it gathers all the information related to it
          (eg: whether fricative, plosive,etc)"""

        offset = self.get_offset(c, lang)
        if not self.in_coordinated_range_offset(offset):
            return self.invalid_vector()

        phonetic_data, phonetic_vectors = self.get_phonetic_info(lang)

        # 'Valid Vector Representation' is the [5] column
        if phonetic_data[offset][5] == 0:
            return self.invalid_vector()

        return phonetic_vectors[offset]

    def get_property_vector(self, v, prop_name):
        """Returns the part of the vector corresponding to the required property"""
        return v[PV_PROP_RANGES[prop_name][0]:PV_PROP_RANGES[prop_name][1]]


    def is_consonant(self, v):
        """Checks the property of the character (of being a consonant)
        selected against its phonetic vector.
        """
        return v[PVIDX_BT_CONSONANT] == 1


    def is_misc(self,v):
        """Checks the property of the character (of being miscellenous)
        selected against its phonetic vector.
        """
        return v[PVIDX_BT_MISC] == 1

    def is_valid(self, v):
        """Checks if the character entered is valid, by checking against the
        phonetic vector. At least 1 of the 38 properties have to be
        satisfied for a valid vector.
        """
        return np.sum(v) > 0

    def is_vowel(self, v):
        """Checks the property of the character (of being a vowel) selected against its phonetic vector
            """
        return v[PVIDX_BT_VOWEL] == 1

    def is_anusvaar(self, v):
        """Checks the property of the character (of having an anusvaar)
        selected against its phonetic vector.
        """
        return v[PVIDX_BT_ANUSVAAR] == 1

    def is_plosive(self, v):
        """Checks the property of the character (of being a plosive
        character) selected against its phonetic vector.
         """
        return self.is_consonant(v) and self.get_property_vector(v, 'consonant_type')[0] == 1

    def is_nukta(self,v):
        """Checks the property of the character (of having a nukta) selected
        against its phonetic vector.
        """
        return v[PVIDX_BT_NUKTA] == 1

    def is_dependent_vowel(self, v):
        """Checks the property of the character (if it is a dependent
        vowel) selected against its phonetic vector.
        """
        return self.is_vowel(v) and v[PVIDX_VSTAT_DEP] == 1

    def orthographic_syllabify(self, word):
        """Main syllablic function."""
        p_vectors = [self.get_phonetic_feature_vector(c, self.lang) for c in word]

        syllables = []

        for i in range(len(word)):
            v = p_vectors[i]

            syllables.append(word[i])

            if i + 1 < len(word) and (not self.is_valid(p_vectors[i + 1]) or self.is_misc(p_vectors[i + 1])):
                syllables.append(u' ')

            elif not self.is_valid(v) or self.is_misc(v):
                syllables.append(u' ')

            elif self.is_vowel(v):

                anu_nonplos = (i + 2 < len(word) and
                               self.is_anusvaar(p_vectors[i + 1]) and
                               not self.is_plosive(p_vectors[i + 2])
                               )

                anu_eow = (i + 2 == len(word) and
                           self.is_anusvaar(p_vectors[i + 1]))

                if not (anu_nonplos or anu_eow):
                    syllables.append(u' ')

            elif i + 1 < len(word) and (self.is_consonant(v) or self.is_nukta(v)):
                if self.is_consonant(p_vectors[i + 1]):
                    syllables.append(u' ')
                elif self.is_vowel(p_vectors[i + 1]) and not self.is_dependent_vowel(p_vectors[i + 1]):
                    syllables.append(u' ')
                elif self.is_anusvaar(p_vectors[i + 1]):
                    anu_nonplos = (i + 2 < len(word) and not self.is_plosive(p_vectors[i + 2]))

                    anu_eow = i + 2 == len(word)

                    if not (anu_nonplos or anu_eow):
                        syllables.append(u' ')

        return u''.join(syllables).strip().split(u' ')


if __name__ == '__main__':
    syllabifier = Syllabifier('hindi')
    current = syllabifier.orthographic_syllabify('नमस्ते')
    print(current)
