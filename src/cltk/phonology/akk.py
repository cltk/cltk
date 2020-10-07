"""
Functions and classes for Akkadian phonology.
"""

from typing import List, Tuple, Union

_author__ = ["M. Willis Monroe <willismonroe@gmail.com>"]
__license__ = "MIT License. See LICENSE."


AKKADIAN = {
    "short_vowels": ["a", "e", "i", "u"],
    "macron_vowels": ["ā", "ē", "ī", "ū"],
    "circumflex_vowels": ["â", "ê", "î", "û"],
    "consonants": [
        "b",
        "d",
        "g",
        "h",
        "ḫ",
        "k",
        "l",
        "m",
        "n",
        "p",
        "q",
        "r",
        "s",
        "ṣ",
        "š",
        "t",
        "ṭ",
        "w",
        "y",
        "z",
        "ʾ",
    ],
}


def get_cv_pattern(
    word: str, pprint: bool = False
) -> Union[List[Tuple[str, int, str]], str]:
    """
    Return a patterned string representing the consonants
    and vowels of the input word.

    >>> word = 'iparras'
    >>> get_cv_pattern(word)
    [('V', 1, 'i'), ('C', 1, 'p'), ('V', 2, 'a'), ('C', 2, 'r'), ('C', 2, 'r'), ('V', 2, 'a'), ('C', 3, 's')]
    >>> get_cv_pattern(word, True)
    'V₁C₁V₂C₂C₂V₂C₃'
    """

    subscripts = {
        1: "₁",
        2: "₂",
        3: "₃",
        4: "₄",
        5: "₅",
        6: "₆",
        7: "₇",
        8: "₈",
        9: "₉",
        0: "₀",
    }

    pattern = []
    c_count = 1
    v_count = 1
    count = 0

    for char in word:
        if char in AKKADIAN["consonants"]:
            cv = "C"
        else:
            cv = "V"
            # remove length:
            if char in AKKADIAN["macron_vowels"]:
                char = AKKADIAN["short_vowels"][AKKADIAN["macron_vowels"].index(char)]
            elif char in AKKADIAN["circumflex_vowels"]:
                char = AKKADIAN["short_vowels"][
                    AKKADIAN["circumflex_vowels"].index(char)
                ]
        if char not in [x[2] for x in pattern]:
            if cv == "C":
                count = c_count
                c_count += 1
            elif cv == "V":
                count = v_count
                v_count += 1
            pattern.append((cv, count, char))
        elif char in [x[2] for x in pattern]:
            pattern.append((cv, next(x[1] for x in pattern if x[2] == char), char))
    if pprint:
        output = ""
        for item in pattern:
            output += item[0] + subscripts[item[1]]
        return output
    return pattern


def _is_consonant(char: str) -> bool:
    return char in AKKADIAN["consonants"]


def _is_vowel(char: str) -> bool:
    return (
        char
        in AKKADIAN["short_vowels"]
        + AKKADIAN["macron_vowels"]
        + AKKADIAN["circumflex_vowels"]
    )


def _is_short_vowel(char: str) -> bool:
    return char in AKKADIAN["short_vowels"]


def _is_macron_vowel(char: str) -> bool:
    return char in AKKADIAN["macron_vowels"]


def _is_circumflex_vowel(char: str) -> bool:
    return char in AKKADIAN["circumflex_vowels"]


def syllabify(word) -> List[str]:
    """
    Split Akkadian words into list of syllables
    >>> syllabify("napištašunu")
    ['na', 'piš', 'ta', 'šu', 'nu']

    >>> syllabify("epištašu")
    ['e', 'piš', 'ta', 'šu']
    """

    syllables = []

    # catch single character words
    if len(word) == 1:
        return [word]

    # If there's an initial vowel and the word is longer than 2 letters,
    # and the third syllable is a not consonant (easy way to check for VCC pattern),
    # the initial vowel is the first syllable.
    # Rule (b.ii)
    if _is_vowel(word[0]):
        if len(word) > 2 and not _is_consonant(word[2]):
            syllables.append(word[0])
            word = word[1:]

    # flip the word and count from the back:
    word = word[::-1]

    # Here we iterate over the characters backwards trying to match
    # consonant and vowel patterns in a hierarchical way.
    # Each time we find a match we store the syllable (in reverse order)
    # and move the index ahead the length of the syllable.
    syllables_reverse = []
    i = 0
    while i < len(word):
        char = word[i]

        # CV:
        if _is_vowel(char):
            if _is_vowel(word[i + 1]):
                # Next char is a vowel so cut off syllable here
                syllables_reverse.append(word[i])
                i += 1
            else:
                syllables_reverse.append(word[i + 1] + word[i])
                i += 2

        # CVC and VC:
        elif _is_consonant(char):
            if _is_vowel(word[i + 1]):
                # If there are only two characters left, that's it.
                if i + 2 >= len(word):
                    syllables_reverse.append(word[i + 1] + word[i])
                    break
                # CVC
                elif _is_consonant(word[i + 2]):
                    syllables_reverse.append(word[i + 2] + word[i + 1] + word[i])
                    i += 3
                # VC (remember it's backwards here)
                elif _is_vowel(word[i + 2]):
                    syllables_reverse.append(word[i + 1] + word[i])
                    i += 2

    return syllables + syllables_reverse[::-1]


def find_stress(word: str) -> List[str]:
    """
    Find the stressed syllable in a word.
    The general logic follows Huehnergard 3rd edition (pgs. 3-4):
    (a) Light: ending in a short vowel: e.g., -a, -ba
    (b) Heavy: ending in a long vowel marked with a macron, or in a
    short vowel plus a consonant: e.g., -ā, -bā, -ak, -bak
    (c) Ultraheavy: ending in a long vowel marked with a circumflex,
    in any long vowel plus a consonant: e.g., -â, -bâ, -āk, -bāk, -âk, -bâk.
    (a) If the last syllable is ultraheavy, it bears the stress.
    (b) Otherwise, stress falls on the last non-final heavy or ultraheavy syllable.
    (c) Words that contain no non-final heavy or ultraheavy syllables have the
    stress fall on the first syllable.

    >>> find_stress("napištašunu")
    ['na', '[piš]', 'ta', 'šu', 'nu']

    """

    word = syllabify(word)

    syllables_stress = []

    for i, syllable in enumerate(word):
        # Enumerate over the syllables and mark them for length
        # We check each type of length by looking at the length of the
        # syllable and verifying rules based on character length.

        # Ultraheavy:
        # -â, -bâ, -āk, -bāk, -âk, -bâk.
        if len(syllable) == 1:
            if _is_circumflex_vowel(syllable):
                syllables_stress.append((syllable, "Ultraheavy"))
                continue
        elif len(syllable) == 2:
            if _is_consonant(syllable[0]) and _is_circumflex_vowel(syllable[1]):
                syllables_stress.append((syllable, "Ultraheavy"))
                continue
            if (
                _is_macron_vowel(syllable[0]) or _is_circumflex_vowel(syllable[0])
            ) and _is_consonant(syllable[1]):
                syllables_stress.append((syllable, "Ultraheavy"))
                continue
        elif len(syllable) == 3:
            if _is_macron_vowel(syllable[1]) or _is_circumflex_vowel(syllable[1]):
                syllables_stress.append((syllable, "Ultraheavy"))
                continue

        # Heavy:
        # -ā, -bā, -ak, -bak
        if len(syllable) == 1:
            if _is_macron_vowel(syllable):
                syllables_stress.append((syllable, "Heavy"))
                continue
        elif len(syllable) == 2:
            if _is_consonant(syllable[0]) and _is_macron_vowel(syllable[1]):
                syllables_stress.append((syllable, "Heavy"))
                continue
            if _is_short_vowel(syllable[0]) and _is_consonant(syllable[1]):
                syllables_stress.append((syllable, "Heavy"))
                continue
        elif len(syllable) == 3:
            if _is_short_vowel(syllable[1]):
                syllables_stress.append((syllable, "Heavy"))
                continue

        # Light:
        # -a, -ba
        if len(syllable) == 1:
            if _is_short_vowel(syllable):
                syllables_stress.append((syllable, "Light"))
                continue
        elif len(syllable) == 2:
            if _is_consonant(syllable[0]) and _is_short_vowel(syllable[1]):
                syllables_stress.append((syllable, "Light"))
                continue

    # It's easier to find stress backwards
    syllables_stress = syllables_stress[::-1]

    syllables = []
    found_stress = 0
    for i, syllable in enumerate(syllables_stress):
        # If we've found the stressed syllable just append the next syllable
        if found_stress:
            syllables.append(syllable[0])
            continue

        # Rule (a)
        elif syllable[1] == "Ultraheavy" and i == 0:
            syllables.append("[{}]".format(syllable[0]))
            found_stress = 1
            continue

        # Rule (b)
        elif syllable[1] in ["Ultraheavy", "Heavy"] and i > 0:
            syllables.append("[{}]".format(syllable[0]))
            found_stress = 1
            continue

        # Final 'Heavy' syllable, gets no stress
        elif syllable[1] == "Heavy" and i == 0:
            syllables.append(syllable[0])
            continue

        # Light syllable gets no stress
        elif syllable[1] == "Light":
            syllables.append(syllable[0])
            continue

    # Reverse the list again
    syllables = syllables[::-1]

    # If we still haven't found stress then rule (c) applies
    # Rule (c)
    if not found_stress:
        syllables[0] = "[{}]".format(syllables[0])

    return syllables


class AkkadianSyllabifier:
    def __init__(self):
        pass

    def syllabify(self, word):
        if type(word) == tuple and len(word) == 2:
            return syllabify(word[0])
        else:
            return syllabify(word)

    def __repr__(self):
        return f"<AkkadianSyllabifier>"

    def __call__(self, word):
        return self.syllabify(word)
