
from typing import List
import os

import cltk.inflection.utils as decl_utils
from cltk.phonology.syllabify import Syllabifier
from cltk.corpus.old_norse.syllabifier import invalid_onsets, VOWELS, CONSONANTS, SHORT_VOWELS, LONG_VOWELS, DIPHTHONGS

import numpy as np

s = Syllabifier(language="old_norse", break_geminants=True)
s.set_invalid_onsets(invalid_onsets)


def extract_common_stem(*args):
    """

    >>> extract_common_stem("armr", "arms", "armar")
    'arm'

    >>> extract_common_stem("ketill", "ketils", "katlar")
    'k'

    >>> extract_common_stem("mór", "mós", "móar")
    'mó'

    >>> extract_common_stem("söngr", "söngs", "söngvar")
    'söng'


    :param args:
    :return:
    """
    # return os.path.commonprefix(args)
    smallest = np.argmin([len(s) for s in args])
    for i, c in enumerate(args[smallest]):
        for other_word in args:
            if c != other_word[i]:
                return args[smallest][:i]
    return args[smallest]







def apply_raw_r_assimilation(last_syllable):
    """

    >>> apply_raw_r_assimilation("arm")
    'armr'
    >>> apply_raw_r_assimilation("ás")
    'áss'
    >>> apply_raw_r_assimilation("stól")
    'stóll'
    >>> apply_raw_r_assimilation("stein")
    'steinn'
    >>> apply_raw_r_assimilation("vin")
    'vinn'


    :param last_syllable:
    :return:
    """

    if len(last_syllable) > 0:
        if last_syllable[-1] == "l":
            return last_syllable + "l"
        elif last_syllable[-1] == "s":
            return last_syllable + "s"
        elif last_syllable[-1] == "n":
            return last_syllable + "n"
    return last_syllable + "r"


def add_r_ending_to_syllable(last_syllable, is_first=True):
    """

    >>> add_r_ending_to_syllable("arm", True)
    'armr'

    >>> add_r_ending_to_syllable("ás", True)
    'áss'

    >>> add_r_ending_to_syllable("stól", True)
    'stóll'

    >>> "jö"+add_r_ending_to_syllable("kul", False)
    'jökull'

    >>> add_r_ending_to_syllable("stein", True)
    'steinn'

    >>> 'mi'+add_r_ending_to_syllable('kil', False)
    'mikill'

    >>> add_r_ending_to_syllable('sæl', True)
    'sæll'

    >>> 'li'+add_r_ending_to_syllable('til', False)
    'litill'

    >>> add_r_ending_to_syllable('vænn', True)
    'vænn'

    >>> add_r_ending_to_syllable('lauss', True)
    'lauss'

    >>> add_r_ending_to_syllable("vin", True)
    'vinr'

    >>> add_r_ending_to_syllable("sel", True)
    'selr'

    >>> add_r_ending_to_syllable('fagr', True)
    'fagr'

    >>> add_r_ending_to_syllable('vitr', True)
    'vitr'

    >>> add_r_ending_to_syllable('vetr', True)
    'vetr'

    >>> add_r_ending_to_syllable('akr', True)
    'akr'

    >>> add_r_ending_to_syllable('Björn', True)
    'Björn'

    >>> add_r_ending_to_syllable('þurs', True)
    'þurs'

    >>> add_r_ending_to_syllable('karl', True)
    'karl'

    >>> add_r_ending_to_syllable('hrafn', True)
    'hrafn'

    :param last_syllable: last syllable of the word
    :param is_first: is it the first syllable of the word?
    :return:
    """
    if len(last_syllable) >= 2:
        if last_syllable[-1] in ['l', 'n', 's', 'r']:
            if last_syllable[-2] in CONSONANTS:
                # Apocope of r
                return last_syllable
            else:
                # Assimilation of r
                if len(last_syllable) >= 3 and last_syllable[-3:-1] in DIPHTHONGS:
                    return apply_raw_r_assimilation(last_syllable)
                elif last_syllable[-2] in SHORT_VOWELS and is_first:
                    # No assimilation when r is supposed to be added to a stressed syllable
                    # whose last letter is l, n or s and the penultimate letter is a short vowel
                    return last_syllable + "r"
                elif last_syllable[-2] in SHORT_VOWELS:
                    return apply_raw_r_assimilation(last_syllable)
                elif last_syllable[-2] in LONG_VOWELS:
                    return apply_raw_r_assimilation(last_syllable)
                return apply_raw_r_assimilation(last_syllable)
        else:
            return last_syllable + "r"
    else:
        return last_syllable + "r"


def add_r_ending(stem):
    """
    >>> add_r_ending("arm")
    'armr'

    >>> add_r_ending("ás")
    'áss'

    >>> add_r_ending("stól")
    'stóll'

    >>> add_r_ending("jökul")
    'jökull'

    >>> add_r_ending("stein")
    'steinn'

    >>> add_r_ending('mikil')
    'mikill'

    >>> add_r_ending('sæl')
    'sæll'

    >>> add_r_ending('litil')
    'litill'

    >>> add_r_ending('vænn')
    'vænn'

    >>> add_r_ending('lauss')
    'lauss'

    >>> add_r_ending("vin")
    'vinr'

    >>> add_r_ending("sel")
    'selr'

    >>> add_r_ending('fagr')
    'fagr'

    >>> add_r_ending('vitr')
    'vitr'

    >>> add_r_ending('vetr')
    'vetr'

    >>> add_r_ending('akr')
    'akr'

    >>> add_r_ending('Björn')
    'björn'

    >>> add_r_ending('þurs')
    'þurs'

    >>> add_r_ending('karl')
    'karl'

    >>> add_r_ending('hrafn')
    'hrafn'

    :param stem:
    :return:
    """
    s_stem = s.syllabify_SSP(stem.lower())
    n_stem = len(s_stem)
    last_syllable = decl_utils.Syllable(s_stem[-1], VOWELS, CONSONANTS)
    return "".join(s_stem[:-1]) + add_r_ending_to_syllable(last_syllable.text, n_stem == 1)
