"""Old Norse phonemic rules

Old Norse words encounter many sound changes which occur mainly according to endings.
Some sound changes may be explained by disappeared or transformed endings.

The i ending lead to an i-umlaut (sound transformation) which made the previous vowel more alike the sound i.
The u ending lead to an u-umlaut (sound transformation) which made the previous vowel more alike the sound u.
The r ending is sometimes assimilated depending on the previous adjacent consonant.

These sound transformations were active at an earlier stage of "classical" Old Norse, i.e. conditions in which such
transformations occurred may be not encountered in "classical" Old Norse, nevertheless their results were still visible
in "classical" Old Norse.

Sources:
- Kleine Grammatik des Altisländischen by Robert Nedoma (in German)
- https://en.wikipedia.org/wiki/Proto-Norse_language#Proto-Norse_to_Old_Norse

"""

from cltk.phonology.syllabify import Syllabifier, Syllable
from cltk.corpus.old_norse.syllabifier import invalid_onsets, VOWELS, CONSONANTS, SHORT_VOWELS, LONG_VOWELS, \
    DIPHTHONGS, BACK_TO_FRONT_VOWELS

import numpy

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]

s = Syllabifier(language="old_norse", break_geminants=True)
s.set_invalid_onsets(invalid_onsets)


class OldNorseSyllable(Syllable):

    def apply_u_umlaut(self, is_second=False):
        if "".join(self.nucleus) == "a":
            self.nucleus = ["ö"]
        elif "".join(self.nucleus) == "ö" and is_second:
            self.nucleus = ["u"]

    def apply_i_umlaut(self):
        nucleus = "".join(self.nucleus)
        if nucleus in BACK_TO_FRONT_VOWELS:
            self.nucleus = [BACK_TO_FRONT_VOWELS[nucleus]]


def extract_common_stem(*args):
    """
    Function which extract the longest common substring in a list of strings.
    This is a very basic function because it does not deal correctly with sound shifts (like u-umlaut and i-umlaut).

    >>> extract_common_stem("armr", "arms", "armar")
    'arm'

    >>> extract_common_stem("ketill", "ketils", "katlar")
    'k'

    # the given result is 'k', but the expected result should be 'katil'

    >>> extract_common_stem("mór", "mós", "móar")
    'mó'

    >>> extract_common_stem("söngr", "söngs", "söngvar")
    'söng'


    :param args:
    :return:
    """
    l_s = [[OldNorseSyllable(syllable, VOWELS, CONSONANTS) for syllable in s.syllabify_ssp(word)] for word in args]

    nuclei = ["".join(syllables[0].nucleus) for syllables in l_s]

    # all_equal = True
    # if len(nuclei) > 1:
    #     for nucleus in nuclei:
    #         all_equal = nuclei[0] == nucleus and all_equal
    #         if not all_equal:
    #             break
    # if all_equal:
    #      return os.path.commonprefix(args)
    smallest = numpy.argmin([len(s) for s in args])
    for i, c in enumerate(args[smallest]):
        for other_word in args:
            if c != other_word[i]:
                return args[smallest][:i]
    return args[smallest]
    # else:
    #     print(nuclei)
    #     return ""


def apply_raw_r_assimilation(last_syllable: str) -> str:
    """
    -r preceded by an -s-, -l- or -n- becomes respectively en -s, -l or -n.

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


    :param last_syllable: last syllable of an Old Norse word
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


def add_r_ending_to_syllable(last_syllable: str, is_first=True) -> str:
    """
    Adds an the -r ending to the last syllable of an Old Norse word.
    In some cases, it really adds an -r. In other cases, it on doubles the last character or left the syllable
    unchanged.

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
    :return: inflected syllable
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


def add_r_ending(stem: str) -> str:
    """
    Adds an -r ending to an Old Norse noun.

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
    s_stem = s.syllabify_ssp(stem.lower())
    n_stem = len(s_stem)
    last_syllable = Syllable(s_stem[-1], VOWELS, CONSONANTS)
    return "".join(s_stem[:-1]) + add_r_ending_to_syllable(last_syllable.text, n_stem == 1)


def has_u_umlaut(word: str) -> bool:
    """
    Does the word have an u-umlaut?

    >>> has_u_umlaut("höfn")
    True

    >>> has_u_umlaut("börnum")
    True

    >>> has_u_umlaut("barn")
    False

    :param word: Old Norse word
    :return: has an u-umlaut occurred?
    """
    word_syl = s.syllabify_ssp(word)
    s_word_syl = [Syllable(syl, VOWELS, CONSONANTS) for syl in word_syl]

    if len(s_word_syl) == 1 and s_word_syl[-1].nucleus[0] in ["ö", "ǫ"]:
        return True
    elif len(s_word_syl) >= 2 and s_word_syl[-1].nucleus[0] == "u":
        return s_word_syl[-2].nucleus[0] in ["ö", "ǫ"]
    return False


def apply_i_umlaut(stem: str):
    """
    Changes the vowel of the last syllable of the given stem according to an i-umlaut.

    >>> apply_i_umlaut("mæl")
    'mæl'
    >>> apply_i_umlaut("lagð")
    'legð'
    >>> apply_i_umlaut("vak")
    'vek'
    >>> apply_i_umlaut("haf")
    'hef'
    >>> apply_i_umlaut("buð")
    'byð'
    >>> apply_i_umlaut("bár")
    'bær'
    >>> apply_i_umlaut("réð")
    'réð'
    >>> apply_i_umlaut("fór")
    'fœr'

    :param stem:
    :return:
    """
    assert len(stem) > 0
    s_stem = s.syllabify_ssp(stem.lower())
    last_syllable = OldNorseSyllable(s_stem[-1], VOWELS, CONSONANTS)
    last_syllable.apply_i_umlaut()
    return "".join(s_stem[:-1]) + str(last_syllable)


def apply_u_umlaut(stem: str):
    """
    Changes the vowel of the last syllable of the given stem if the vowel is affected by an u-umlaut.
    >>> apply_u_umlaut("far")
    'för'
    >>> apply_u_umlaut("ör")
    'ör'
    >>> apply_u_umlaut("axl")
    'öxl'
    >>> apply_u_umlaut("hafn")
    'höfn'

    :param stem:
    :return:
    """
    assert len(stem) > 0
    s_stem = s.syllabify_ssp(stem.lower())
    if len(s_stem) == 1:
        last_syllable = OldNorseSyllable(s_stem[-1], VOWELS, CONSONANTS)
        last_syllable.apply_u_umlaut()
        return "".join(s_stem[:-1]) + str(last_syllable)

    else:
        penultimate_syllable = OldNorseSyllable(s_stem[-2], VOWELS, CONSONANTS)
        last_syllable = OldNorseSyllable(s_stem[-1], VOWELS, CONSONANTS)
        penultimate_syllable.apply_u_umlaut()
        last_syllable.apply_u_umlaut(True)
        last_syllable.apply_u_umlaut(True)
        return "".join(s_stem[:-2]) + str(penultimate_syllable) + str(last_syllable)


def ns_has_i_umlaut(ns: str, gs: str, np: str):
    """
    Checks if the nominative singular has an i-umlaut
    # >>> ns_has_i_umlaut("ketill", "ketils", "katlar")
    # True

    >>> ns_has_i_umlaut("armr", "arms", "armar")
    False

    >>> ns_has_i_umlaut("mór", "mós", "móar")
    False

    >>> ns_has_i_umlaut("hirðir", "hirðis", "hirðar")
    False

    >>> ns_has_i_umlaut("söngr", "söngs", "söngvar")
    False

    >>> ns_has_i_umlaut("gestr", "gests", "gestir")
    False

    >>> ns_has_i_umlaut("staðr", "staðar", "staðir")
    False

    :param ns:
    :param gs:
    :param np:
    :return:
    """

    ns_syl = s.syllabify_ssp(ns)
    gs_syl = s.syllabify_ssp(gs)
    np_syl = s.syllabify_ssp(np)
    s_ns_syl = [Syllable(syl, VOWELS, CONSONANTS) for syl in ns_syl]
    s_gs_syl = [Syllable(syl, VOWELS, CONSONANTS) for syl in gs_syl]
    s_np_syl = [Syllable(syl, VOWELS, CONSONANTS) for syl in np_syl]
    if len(gs_syl) >= 2 and s_gs_syl[-1].nucleus[0] == "i":
        if len(ns_syl) >= 2:
            vowel = s_ns_syl[-2].nucleus[0]
        else:
            vowel = s_ns_syl[-1].nucleus[0]
        return vowel in BACK_TO_FRONT_VOWELS and s_gs_syl[-2].nucleus[0] == BACK_TO_FRONT_VOWELS[vowel]

    if len(np_syl) >= 2 and s_np_syl[-1].nucleus[0] == "i":
        if len(ns_syl) >= 2:
            vowel = s_ns_syl[-2].nucleus[0]
        else:
            vowel = s_ns_syl[-1].nucleus[0]
        return vowel in BACK_TO_FRONT_VOWELS and s_np_syl[-2].nucleus[0] in BACK_TO_FRONT_VOWELS[vowel]

    return False
