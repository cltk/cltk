"""
Functions and classes for Akkadian morphology.
"""


__author__ = ["M. Willis Monroe <willismonroe@gmail.com>"]
__license__ = "MIT License. See LICENSE."

from typing import Dict, List, Tuple

from cltk.phonology.akk import AKKADIAN, get_cv_pattern, syllabify
from cltk.stem.akk import ENDINGS, stem


def get_bound_form(noun: str, gender: str) -> str:
    """
    Return bound form of nound, given its gender.

    >>> get_bound_form("awīlum", "m")
    'awīl'
    """

    syllables = syllabify(noun)
    stemmed_noun = stem(noun, gender)
    cv_pattern = get_cv_pattern(stemmed_noun)

    # Based on Huehnergard Appendix 6.C.1: base in -VC
    if [letter[0] for letter in cv_pattern[-2:]] == ["V", "C"] or stemmed_noun in [
        "nakr"
    ]:
        # a. 2-syllable
        if len(syllables) > 2:
            # awīlum > awīl, nakrum > naker
            if stemmed_noun in ["nakr"]:
                return "naker"
            else:
                return stemmed_noun
        # b. 1-syllable
        elif len(syllables) > 1:
            # bēlum > bēl
            return stemmed_noun
        # c. abum, aḫum
        if stemmed_noun in ["ab", "aḫ"]:
            return stemmed_noun + "i"

    # Appendix 6.C.2: base in -C₁C₁
    if cv_pattern[-1][:2] == cv_pattern[-2][:2]:
        # a. 1-syllable
        if 3 > len(syllables) > 1:
            return stemmed_noun + "i"
        # b. 2-syllable, -tt
        if len(syllables) > 2 and cv_pattern[-1][2] + cv_pattern[-2][2] == "tt":
            return stemmed_noun + "i"
        # c. 2-syllable, other
        if len(syllables) > 2:
            return stemmed_noun[:-1]

    # Appendix 6.C.3: base in -C₁C₂, C₂ ≠ t, i.e. pVrs
    if (
        cv_pattern[-1][0] == cv_pattern[-2][0]
        and cv_pattern[-1][1] != cv_pattern[-2][1]
    ):
        return stemmed_noun[:-1] + stemmed_noun[1] + stemmed_noun[-1]

    # Appendix 6.C.4: base in -Ct (fem.)
    if cv_pattern[-1][2] == "t" and cv_pattern[-2][0] == "C":
        if len(syllables) > 2:
            return stemmed_noun + "i"
        # Need to deal with fem. Ptcpl. māḫirtum -> māḫirat
        if len(syllables) > 1:
            # These are case by case
            if stemmed_noun in ["qīšt"]:
                return stemmed_noun + "i"
            if stemmed_noun in ["mārt"]:
                return stemmed_noun[:-1] + stemmed_noun[1] + stemmed_noun[-1]
                # Appendix 6.C.5: base in -V
                # Weak nouns...


def decline_noun(
    noun: str, gender: str, mimation: bool = True
) -> List[Tuple[str, Dict[str, str]]]:
    """
    Return a list of all possible Akkadiandeclined forms given any form
     of a noun and its gender.

     >>> decline_noun('iltum', 'f')
     [('iltum', {'case': 'nominative', 'number': 'singular'}), \
('iltam', {'case': 'accusative', 'number': 'singular'}), \
('iltim', {'case': 'genitive', 'number': 'singular'}), \
('iltān', {'case': 'nominative', 'number': 'dual'}), \
('iltīn', {'case': 'oblique', 'number': 'dual'}), \
('ilātum', {'case': 'nominative', 'number': 'plural'}), \
('ilātim', {'case': 'oblique', 'number': 'plural'})]
    """

    stemmed_noun = stem(noun, gender)
    declension = []

    for case in ENDINGS[gender]["singular"]:
        if gender == "m":
            form = stemmed_noun + ENDINGS[gender]["singular"][case]
        else:
            form = stemmed_noun + ENDINGS[gender]["singular"][case][1:]
        declension.append((form, {"case": case, "number": "singular"}))

    for case in ENDINGS[gender]["dual"]:
        if gender == "m":
            form = stemmed_noun + ENDINGS[gender]["dual"][case]
        else:
            form = stemmed_noun + ENDINGS[gender]["dual"][case][1:]
        declension.append((form, {"case": case, "number": "dual"}))

    for case in ENDINGS[gender]["plural"]:
        if gender == "m":
            form = stemmed_noun + ENDINGS[gender]["plural"][case]
        else:
            if stemmed_noun[-3] in AKKADIAN["macron_vowels"]:
                theme_vowel = stemmed_noun[-3]
            else:
                theme_vowel = "ā"
            ending = [x for x in ENDINGS[gender]["plural"][case] if x[0] == theme_vowel]
            if stemmed_noun[-2] in AKKADIAN["short_vowels"]:
                form = stemmed_noun[:-2] + ending[0]
            elif (
                stemmed_noun[-1] in AKKADIAN["consonants"]
                and stemmed_noun[-2] in AKKADIAN["macron_vowels"]
            ):
                form = stemmed_noun + ending[0]
            else:
                form = stemmed_noun[:-1] + ending[0]
        declension.append((form, {"case": case, "number": "plural"}))

    return declension
