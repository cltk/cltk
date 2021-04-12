"""The Middle English alphabet. Sources:

- *From Old English to Standard English*, Dennis Freeborn
- `<https://web.cn.edu/kwheeler/documents/ME_Pronunciation.pdf>`_
- `<https://en.wikipedia.org/wiki/Middle_English_phonology>`_

The produced consonant sound in Middle English are categorized as
following:

- Stops: ⟨/b/, /p/, /d/, /t/, /g/, /k/⟩
- Affricatives: ⟨/ǰ/, /č/, /v/, /f/, /ð/, /θ/, /z/, /s/, /ž/, /š/, /c̹/, /x/, /h/⟩
- Nasals: ⟨/m/, /n/, /ɳ/⟩
- Later Resonants: ⟨/l/⟩
- Medial Resonants: ⟨/r/, /y/, /w/⟩

Thorn (þ) was gradually replaced by the diphthong "th", while Eth (ð), which
had already fallen out of use by the 14th century, was later replaced by "d"

Wynn (ƿ) is the predecessor of "w". Modern transliteration scripts, usually
replace it with "w" as to avoid confusion with the strikingly similar p

The vowel sounds in Middle English are divided into:

- Long Vowels: ⟨/a:/, /e/, /e̜/, /i/ , /ɔ:/, /o/ , /u/⟩
- Short Vowels: ⟨/a/, /ɛ/, /I/, /ɔ/, /U/, /ə/⟩

As established rules for ME orthography were effectively nonexistent, compiling
a definite list of diphthongs is non-trivial. The following aims to compile a
list of the most commonly-used diphthongs.

>>> from cltk.alphabet import enm
>>> enm.ALPHABET[:5]
['a', 'b', 'c', 'd', 'e']
>>> enm.CONSONANTS[:5]
['b', 'c', 'd', 'f', 'g']
"""

import re

ALPHABET = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
    "y",
    "æ",
    "ð",
    "þ",
    "ƿ",
]


CONSONANTS = [
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "l",
    "m",
    "n",
    "p",
    "r",
    "s",
    "t",
    "x",
    "ð",
    "þ",
    "ƿ",
]

VOWELS = ["a", "e", "i", "o", "u", "y", "æ"]

DIPTHONGS = [
    "ai",
    "au",
    "aw",
    "ay",
    "ei",
    "eu",
    "ew",
    "ey",
    "iu",
    "iw",
    "o",
    "oi",
    "ou",
    "ow",
    "oy",
    "uw",
]


def normalize_middle_english(
    text: str, to_lower: bool = True, alpha_conv: bool = True, punct: bool = True
) -> str:
    """Normalizes Middle English text string and returns normalized string.

    :param text: str text to be normalized
    :param to_lower: bool convert text to lower text
    :param alpha_conv: bool convert text to canonical form æ -> ae, þ -> th, ð -> th, ȝ -> y if at beginning,
     gh otherwise
    :param punct: remove punctuation

    >>> normalize_middle_english('Whan Phebus in the CraBbe had neRe hys cours ronne', to_lower = True)
    'whan phebus in the crabbe had nere hys cours ronne'
    >>> normalize_middle_english('I pray ȝow þat ȝe woll', alpha_conv = True)
    'i pray yow that ye woll'
    >>> normalize_middle_english("furst, to begynne:...", punct = True)
    'furst to begynne'
    """

    if to_lower:
        text = text.lower()
    if alpha_conv:
        text = text.replace("æ", "ae").replace("þ", "th").replace("ð", "th")
        text = re.sub(r"(?<!\w)(?=\w)ȝ", "y", text)
        text = text.replace("ȝ", "gh")
    if punct:
        text = re.sub(r"[\.\";\,\:\[\]\(\)!&?‘]", "", text)
    return text
