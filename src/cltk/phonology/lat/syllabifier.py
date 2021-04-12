"""Split Latin words into a list of syllables, based on a set of Latin
language syllable specifications and the original work of Father Matthew
Spencer in C# and Javascript. Original documentation from Fr. Spencer
is preserved where applicable.
"""

import re
from typing import List

__author__ = ["Luke Hollis <lukehollis@gmail.com>"]
__license__ = "MIT License. See LICENSE."

# nota bene: ui is only a diphthong in the exceptional
# cases below (according to Wheelock's Latin)
LATIN = {
    "diphthongs": ["ae", "au", "ei", "eu", "oe"],
    "exceptions": {
        "huius": ["hui", "us"],
        "cuius": ["cui", "us"],
        "huic": ["huic"],
        "cui": ["cui"],
        "hui": ["hui"],
    },
    # y is treated as a vowel; not native to Latin but useful
    # for words borrowed from Greek
    "vowels": [
        "a",
        "e",
        "i",
        "o",
        "u",
        "á",
        "é",
        "í",
        "ó",
        "ú",
        "ā",
        "ē",
        "ī",
        "ō",
        "ū",
        "æ",
        "œ",
        "ǽ",  # no accented œ in unicode?
        "y",
    ],
    "mute_consonants_and_f": ["b", "c", "d", "g", "p", "t", "f"],
    "liquid_consonants": ["l", "r"],
    "prefixes": [
        "a",
        "ab",
        "abs",
        "ad",
        "ac",
        "amb",
        "ambi",
        "ante",
        "circum",
        "co",
        "con",
        "com",
        "contra",
        "counter",
        "de",
        "dis",
        "di",
        "dif",
        "e",
        "ex",
        "ef",
        "extra",
        "extro",
        "in",
        "en",
        "infra",
        "inter",
        "intro",
        "juxta",
        "ne",
        "non",
        "ob",
        "per",
        "post",
        "prae",
        "pre",
        "preter",
        "pro",
        "quasi",
        "re",
        "red",
        "retro",
        "se",
        "sed",
        "sin",
        "sine",
        "sub",
        "subter",
        "super",
        "sur",
        "supra",
        "trans",
        "tra",
        "tran",
        "ultra",
        "outr",
    ],
    "single_syllable_prefixes": ["in", "ex", "ob"],
}


def _is_consonant(char: str) -> bool:
    """Checks if char is in the list of vowels in the language"""
    return char not in LATIN["vowels"]


def _is_vowel(char: str) -> bool:
    """Checks if char is in the list of vowels in the language"""
    return char in LATIN["vowels"]


def _is_diphthong(char_1: str, char_2: str) -> bool:
    """Checks if two sequential characters compose a diphthong"""
    return char_1 + char_2 in LATIN["diphthongs"]


def _is_mute_consonant_or_f(char: str) -> bool:
    """Checks if char is in the mute_consonants_and_f list"""
    return char in LATIN["mute_consonants_and_f"]


def _is_liquid_consonant(char: str) -> bool:
    """Checks if char is in the mute_consonants_and_f list"""
    return char in LATIN["liquid_consonants"]


def syllabify(word: str) -> List[str]:
    """
    Splits input Latin word into a list of syllables

    >>> syllabify('sidere')
    ['si', 'de', 're']
    """

    prefixes = LATIN["single_syllable_prefixes"]
    prefixes.sort(key=len, reverse=True)

    # Check if word is in exception dictionary
    if word in LATIN["exceptions"]:
        syllables = LATIN["exceptions"][word]

    # Else, break down syllables for word
    else:
        syllables = []

        # Remove prefixes
        for prefix in prefixes:
            if word.startswith(prefix):
                syllables.append(prefix)
                word = re.sub("^%s" % prefix, "", word)
                break

        # Initialize syllable to build by iterating through over characters
        syllable = ""

        # Get word length for determining character position in word
        word_len = len(word)

        # Iterate over characters to build syllables
        for i, char in enumerate(word):

            # Build syllable
            syllable = syllable + char
            syllable_complete = False

            # Checks to process syllable logic
            char_is_vowel = _is_vowel(char)
            has_next_char = i < word_len - 1
            has_prev_char = i > 0

            # If it's the end of the word, the syllable is complete
            if not has_next_char:
                syllable_complete = True

            else:
                next_char = word[i + 1]
                if has_prev_char:
                    prev_char = word[i - 1]

                # 'i' is a special case for a vowel. when i is at the
                # beginning of the word (Iesu) or i is between
                # vowels (alleluia), then the i is treated as a
                # consonant (y) Note: what about compounds like 'adiungere'
                if char == "i" and has_next_char and _is_vowel(next_char):
                    if i == 0:
                        char_is_vowel = False
                    elif _is_vowel(prev_char):
                        char_is_vowel = False

                # Determine if the syllable is complete
                if char_is_vowel:

                    if (  # If the next character's a vowel
                        _is_vowel(
                            next_char
                        )  # And it doesn't compose a dipthong with the current character
                        and not _is_diphthong(
                            char, next_char
                        )  # And the current character isn't preceded by a q, unless followed by a u
                        and not (
                            has_prev_char
                            and prev_char == "q"
                            and char == "u"
                            and next_char != "u"
                        )
                    ) or (
                        # If the next character's a consonant
                        # but not a double consonant,
                        # unless it's a mute consonant followed
                        # by a liquid consonant
                        i < word_len - 2
                        and (
                            (
                                (
                                    has_prev_char
                                    and prev_char != "q"
                                    and char == "u"
                                    and _is_vowel(word[i + 2])
                                )
                                or (
                                    not has_prev_char
                                    and char == "u"
                                    and _is_vowel(word[i + 2])
                                )
                            )
                            or (
                                char != "u"
                                and _is_vowel(word[i + 2])
                                and not _is_diphthong(char, next_char)
                            )
                            or (
                                _is_mute_consonant_or_f(next_char)
                                and _is_liquid_consonant(word[i + 2])
                            )
                        )
                    ):
                        syllable_complete = True

                # Otherwise, it's a consonant
                else:

                    if (  # If the next character's also a consonant (but it's not the last in the word)
                        (
                            not _is_vowel(next_char) and i < word_len - 2
                        )  # If the char's not a mute consonant followed by a liquid consonant
                        and not (
                            _is_mute_consonant_or_f(char)
                            and _is_liquid_consonant(next_char)
                        )  # If the char's not a c, p, or t followed by an h
                        and not (
                            (
                                has_prev_char
                                and not _is_vowel(prev_char)
                                and char in ["c", "p", "t"]
                                and next_char == "h"
                            )
                            or (
                                not has_prev_char
                                and char in ["c", "p", "t"]
                                and next_char == "h"
                            )
                        )  # And it's not the only letter in the syllable
                        and not len(syllable) == 1
                    ):
                        syllable_complete = True

            # If it's a complete syllable, append it to syllables list and reset syllable
            if syllable_complete:
                syllables.append(syllable)
                syllable = ""

    return syllables
