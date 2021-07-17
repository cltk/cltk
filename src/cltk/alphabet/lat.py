"""Alphabet and text normalization for Latin.

- *Principles of Text Cleaning gleaned from*
- http://udallasclassics.org/wp-content/uploads/maurer_files/APPARATUSABBREVIATIONS.pdf

Guidelines:
- [...] Square brackets, or in recent editions wavy brackets ʺ{...}ʺ, enclose words etc. that an editor thinks should be deleted (see ʺdel.ʺ) or marked as out of place (see ʺsecl.ʺ).
- [...] Square brackets in a papyrus text, or in an inscription, enclose places where words have been lost through physical damage.
- If this happens in mid-line, editors use ʺ[...]ʺ.
- If only the end of the line is missing, they use a single bracket ʺ[...ʺ
- If the lineʹs beginning is missing, they use ʺ...]ʺ
- Within the brackets, often each dot represents one missing letter.
- [[...]] Double brackets enclose letters or words deleted by the medieval copyist himself.
- (...) Round brackets are used to supplement words abbreviated by the original copyist; e.g. in an inscription: ʺtrib(unus) mil(itum) leg(ionis) IIIʺ
- <...> diamond ( = elbow = angular) brackets enclose words etc. that an editor has added (see ʺsuppl.ʺ)
- †  An obelus (pl. obeli) means that the word(s etc.) is very plainly corrrupt, but the editor cannot see how to emend.
- If only one word is corrupt, there is only one obelus, which precedes the word; if two or more words are corrupt, two obeli enclose them. (Such at least is the rule--but that rule is often broken, especially in older editions, which sometimes dagger several words using only one obelus.) To dagger words in this way is to ʺobelizeʺ them.

"""
__author__ = [
    "Todd Cook <todd.g.cook@gmail.com>",
    "Kyle P. Johnson <kyle@kyle-p-johnson.com>",
]
__license__ = "MIT License"

import re
from typing import Dict

from cltk.alphabet.text_normalization import (
    cltk_normalize,
    remove_odd_punct,
    split_leading_punct,
    split_trailing_punct,
)

BRACE_STRIP = re.compile(r"{[^}]+}")
NUMERALS = re.compile(r"[0-9]+")
LATIN_PUNCT = re.compile(r"[\\/':;,!\?\._『@#\$%^&\*]+")
QUOTES = re.compile(r'["”“]+')
# we will extact content between brackets, it is editorial
ANGLE_BRACKETS = re.compile(r"([a-zA-Z]+)?<[a-zA-Z\s]+>([,\?\.a-zA-Z]+)?")
SQUARE_BRACKETS = re.compile(r"\[[^\]]+\]")
OBELIZED_WORDS = re.compile(r"†[^†]+†")
OBELIZED_WORD = re.compile(r"†[^\s]+\s")
OBELIZED_PLUS_WORDS = re.compile(r"[\+][^\+]+[\+]")
OBELIZED_PLUS_WORD = re.compile(r"[\+][^\s]+\s")
HYPHENATED = re.compile(r"\s[^-]+-[^-]+\s")


class JVReplacer:  # pylint: disable=too-few-public-methods
    """Replace J/V with I/U.
    Latin alphabet does not distinguish between J/j and I/i and V/v and U/u;
    Yet, many texts bear the influence of later editors and the predilections of other languages.

    In practical terms, the JV substitution is recommended on all Latin text preprocessing; it
    helps to collapse the search space.

    >>> replacer = JVReplacer()
    >>> replacer.replace("Julius Caesar")
    'Iulius Caesar'

    >>> replacer.replace("In vino veritas.")
    'In uino ueritas.'

    """

    def __init__(self):
        """Initialization for JVReplacer, reads replacement pattern tuple."""
        patterns = [(r"j", "i"), (r"v", "u"), (r"J", "I"), (r"V", "U")]
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text):
        """Do j/v replacement"""
        for (pattern, repl) in self.patterns:
            text = re.subn(pattern, repl, text)[0]
        return text


JV_REPLACER = JVReplacer()


class LigatureReplacer:  # pylint: disable=too-few-public-methods
    """Replace 'œæ' with AE, 'Œ Æ' with OE.
    Classical Latin wrote the o and e separately (as has today again become the general practice),
    but the ligature was used by medieval and early modern writings, in part because the
    diphthongal sound had, by Late Latin, merged into the sound [e].
    See: https://en.wikipedia.org/wiki/%C5%92
    Æ (minuscule: æ) is a grapheme named æsc or ash, formed from the letters a and e, originally
    a ligature representing the Latin diphthong ae. It has been promoted to the full status of a
    letter in the alphabets of some languages, including Danish, Norwegian, Icelandic, and Faroese.
    See: https://en.wikipedia.org/wiki/%C3%86

    >>> replacer = LigatureReplacer()
    >>> replacer.replace("mæd")
    'maed'

    >>> replacer.replace("prœil")
    'proeil'

    """

    def __init__(self):
        """Initialization for LigatureReplacer, reads replacement pattern tuple."""
        patterns = [(r"œ", "oe"), (r"æ", "ae"), (r"Œ", "OE"), (r"Æ", "AE")]
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text):
        """Do character replacement."""
        for (pattern, repl) in self.patterns:
            text = re.subn(pattern, repl, text)[0]
        return text


LIGATURE_REPLACER = LigatureReplacer()


def dehyphenate(text: str) -> str:
    """
    Remove hyphens from text; used on texts that have an line breaks with hyphens
    that may creep into the text. Caution using this elsewhere.
    :param text:
    :return:

    >>> dehyphenate('quid re-tundo hier')
    'quid retundo hier'
    """

    idx_to_omit = []
    for item in HYPHENATED.finditer(text):
        idx_to_omit.insert(0, item.span())
    for start, end in idx_to_omit:
        text = text[:start] + text[start:end].replace("-", "") + text[end:]
    return text


def swallow(text: str, pattern_matcher: re.Pattern) -> str:
    """
    Utility function internal to this module

    :param text: text to clean
    :param pattern_matcher: pattern to match
    :return: the text without the matched pattern; spaces are not substituted
    """
    idx_to_omit = []
    for item in pattern_matcher.finditer(text):
        idx_to_omit.insert(0, item.span())
    for start, end in idx_to_omit:
        text = text[:start] + text[end:]
    return text.strip()


def swallow_braces(text: str) -> str:
    """
    Remove Text within braces, and drop the braces.

    :param text: Text with braces
    :return: Text with the braces and any text inside removed

    >>> swallow_braces("{PRO P. QVINCTIO ORATIO} Quae res in civitate {etc}... ")
    'Quae res in civitate ...'

    """
    return swallow(text, BRACE_STRIP)


def drop_latin_punctuation(text: str) -> str:
    """
    Drop all Latin punctuation except the hyphen and obelization markers, replacing the punctuation
    with a space.
    Please collapsing hyphenated words and removing obelization marks separately beforehand.

    The hyphen is important in Latin tokenization as the enclitic particle `-ne`
    is different than the interjection `ne`.

    :param text: Text to clean
    :return: cleaned text

    >>> drop_latin_punctuation('quid est ueritas?')
    'quid est ueritas '

    >>> drop_latin_punctuation("vides -ne , quod , planus est ")
    'vides -ne   quod   planus est '

    >>> drop_latin_punctuation("here is some trash, punct \/':;,!\?\._『@#\$%^&\*okay").replace("  ", " ")
    'here is some trash punct okay'

    """
    text = NUMERALS.sub(" ", text)
    text = LATIN_PUNCT.sub(" ", text)
    text = QUOTES.sub(" ", text)
    return text


def remove_accents(text: str) -> str:  # pylint: disable=too-many-statements
    """
    Remove accents; note: AE replacement and macron replacement should happen elsewhere, if desired.
    :param text: text with undesired accents
    :return: clean text

    >>> remove_accents('suspensám')
    'suspensam'

    >>> remove_accents('quăm')
    'quam'

    >>> remove_accents('aegérrume')
    'aegerrume'

    >>> remove_accents('ĭndignu')
    'indignu'

    >>> remove_accents('îs')
    'is'

    >>> remove_accents('óccidentem')
    'occidentem'

    >>> remove_accents('frúges')
    'fruges'

    """
    replacements = (
        (r"á", "a"),
        (r"Á", "A"),
        (r"á", "a"),
        (r"Á", "A"),
        (r"ă", "a"),
        (r"Ă", "A"),
        (r"à", "a"),
        (r"À", "A"),
        (r"â", "a"),
        (r"Â", "A"),
        (r"ä", "a"),
        (r"Ä", "A"),
        (r"é", "e"),
        (r"è", "e"),
        (r"È", "E"),
        (r"é", "e"),
        (r"É", "E"),
        (r"ê", "e"),
        (r"Ê", "E"),
        (r"ë", "e"),
        (r"Ë", "E"),
        (r"ĭ", "i"),
        (r"î", "i"),
        (r"í", "i"),
        (r"í", "i"),
        (r"î", "i"),
        (r"Î", "I"),
        (r"ï", "i"),
        (r"Ï", "I"),
        (r"ó", "o"),
        (r"ô", "o"),
        (r"Ô", "O"),
        (r"ö", "o"),
        (r"Ö", "O"),
        (r"û", "u"),
        (r"Û", "U"),
        (r"ù", "u"),
        (r"Ù", "U"),
        (r"ü", "u"),
        (r"Ü", "U"),
        (r"ú", "u"),
        (r"ÿ", "y"),
        (r"Ÿ", "Y"),
        (r"ç", "c"),
        (r"Ç", "C"),
        (r"ë", "e"),
        (r"Ë", "E"),
        (r"Ȳ", "Y"),
        (r"ȳ", "y"),
    )
    for target, tranformation in replacements:
        text = text.replace(target, tranformation)
    return text


def remove_macrons(text: str) -> str:
    """
    Remove macrons above vowels
    :param text: text with macronized vowels
    :return: clean text

    >>> remove_macrons("canō")
    'cano'

    >>> remove_macrons("Īuliī")
    'Iulii'

    """
    text = text.replace(r"ā", "a")
    text = text.replace(r"Ā", "A")
    text = text.replace(r"ē", "e")
    text = text.replace(r"Ē", "E")
    text = text.replace(r"ī", "i")
    text = text.replace(r"Ī", "I")
    text = text.replace(r"ō", "o")
    text = text.replace(r"Ō", "O")
    text = text.replace(r"ū", "u")
    text = text.replace(r"Ū", "U")
    return text


def swallow_angle_brackets(text: str) -> str:
    """
    Disappear text in and surrounding an angle bracket
    >>> text = " <O> mea dext<e>ra illa CICERO RUFO Quo<quo>. modo proficiscendum <in> tuis.  deesse HS <c> quae    metu <exagitatus>, furore   <es>set consilium  "
    >>> swallow_angle_brackets(text)
    'mea  illa CICERO RUFO  modo proficiscendum  tuis.  deesse HS  quae    metu  furore    consilium'

    """
    text = swallow(text, ANGLE_BRACKETS)
    # There are occasionally some unmatched ANGLE_BRACKETS
    text = text.replace("<", " ")
    text = text.replace(">", " ")
    return text


def disappear_angle_brackets(text: str) -> str:
    """
    Remove all angle brackets, keeping the surrounding text; no spaces are inserted
    :param text: text with angle bracket
    :return: text without angle brackets
    """
    text = text.replace("<", "")
    text = text.replace(">", "")
    return text


def swallow_square_brackets(text: str) -> str:
    """
    Swallow text inside angle brackets, without substituting a space.
    :param text: text to clean
    :return: text without square brackets and text inside removed

    >>> swallow_square_brackets("qui aliquod institui[t] exemplum")
    'qui aliquod institui exemplum'

    >>> swallow_square_brackets("posthac tamen cum haec [tamen] quaeremus,")
    'posthac tamen cum haec  quaeremus,'

    """
    return swallow(text, SQUARE_BRACKETS)


def swallow_obelized_words(text: str) -> str:
    """
    Swallow obelized words; handles enclosed and words flagged on the left.
    Considers plus signs and daggers as obelization markers
    :param text: Text with obelized words
    :return: clean text

    >>> swallow_obelized_words("tu Fauonium †asinium† dicas")
    'tu Fauonium  dicas'

    >>> swallow_obelized_words("tu Fauonium †asinium dicas")
    'tu Fauonium dicas'

    >>> swallow_obelized_words("meam +similitudinem+")
    'meam'

    >>> swallow_obelized_words("mea +ratio non habet" )
    'mea non habet'

    """
    text = swallow(text, OBELIZED_WORDS)
    text = swallow(text, OBELIZED_WORD)
    text = swallow(text, OBELIZED_PLUS_WORDS)
    return swallow(text, OBELIZED_PLUS_WORD)


def disappear_round_brackets(text: str) -> str:
    """
    Remove round brackets and keep the text intact
    :param text: Text with round brackets.
    :return: Clean text.

    >>> disappear_round_brackets("trib(unus) mil(itum) leg(ionis) III")
    'tribunus militum legionis III'
    """
    text = text.replace("(", "")
    return text.replace(")", "")


def swallow_editorial(text: str) -> str:
    """
    Swallow common editorial morks
    :param text: Text with editorial marks
    :return: Clean text.

    >>> swallow_editorial("{PRO P. QVINCTIO ORATIO} Quae res in civitate trib(unus) mil(itum) leg(ionis) III tu Fauonium †asinium† dicas meam +similitudinem+  mea +ratio non habet ...     ")
    '{PRO P. QVINCTIO ORATIO} Quae res in civitate tribunus militum legionis III tu Fauonium  dicas meam   mea non habet ...'

    """
    text = disappear_round_brackets(text)
    text = swallow_angle_brackets(text)
    text = swallow_square_brackets(text)
    text = swallow_obelized_words(text)
    return text


def accept_editorial(text: str) -> str:
    """
    Accept common editorial suggestions
    :param text: Text with editorial suggestions
    :return: clean text

    >>> accept_editorial("{PRO P. QVINCTIO ORATIO} Quae res in civitate trib(unus) mil(itum) leg(ionis) III tu Fauonium †asinium† dicas meam +similitudinem+  mea +ratio non habet ...     ")
    'Quae res in civitate tribunus militum legionis III tu Fauonium  dicas meam   mea non habet  '

    """
    text = swallow_braces(text)
    text = disappear_round_brackets(text)
    text = swallow_obelized_words(text)
    text = text.replace("[", "")
    text = text.replace("]", "")
    text = text.replace("<", "")
    text = text.replace(">", "")
    text = text.replace("...", " ")
    return text


def truecase(word: str, case_counter: Dict[str, int]):
    """
    Truecase a word using a Truecase dictionary

    :param word: a word
    :param case_counter: A counter; a dictionary of words/tokens and their relative frequency counts
    :return: the truecased word

    >>> case_counts ={"caesar": 1, "Caesar": 99}
    >>> truecase('CAESAR', case_counts)
    'Caesar'

    """
    lcount = case_counter.get(word.lower(), 0)
    ucount = case_counter.get(word.upper(), 0)
    tcount = case_counter.get(word.title(), 0)
    if lcount == 0 and ucount == 0 and tcount == 0:
        return word  #: we don't have enough information to change the case
    if tcount > ucount and tcount > lcount:
        return word.title()
    if lcount > tcount and lcount > ucount:
        return word.lower()
    if ucount > tcount and ucount > lcount:
        return word.upper()
    return word


def normalize_lat(
    text: str,
    drop_accents: bool = False,
    drop_macrons: bool = False,
    jv_replacement: bool = False,
    ligature_replacement: bool = False,
) -> str:
    """The function for all default Latin normalization.

    >>> text = "canō Īuliī suspensám quăm aegérrume ĭndignu îs óccidentem frúges Julius Caesar. In vino veritas. mæd prœil"
    >>> normalize_lat(text)
    'canō Īuliī suspensám quăm aegérrume ĭndignu îs óccidentem frúges Julius Caesar. In vino veritas. mæd prœil'

    >>> normalize_lat(text, drop_accents=True)
    'canō Īuliī suspensam quăm aegerrume ĭndignu is óccidentem frúges Julius Caesar. In vino veritas. mæd prœil'

    >>> normalize_lat(text, drop_accents=True, drop_macrons=True)
    'cano Iulii suspensam quăm aegerrume ĭndignu is óccidentem frúges Julius Caesar. In vino veritas. mæd prœil'

    >>> normalize_lat(text, drop_accents=True, drop_macrons=True, jv_replacement=True)
    'cano Iulii suspensam quăm aegerrume ĭndignu is óccidentem frúges Iulius Caesar. In uino ueritas. mæd prœil'

    >>> normalize_lat(text, drop_accents=True, drop_macrons=True, jv_replacement=True, ligature_replacement=True)
    'cano Iulii suspensam quăm aegerrume ĭndignu is óccidentem frúges Iulius Caesar. In uino ueritas. maed proeil'

    """
    text_cltk_normalized: str = cltk_normalize(text=text)
    # text_cltk_normalized = split_trailing_punct(text=text_cltk_normalized)
    # text_cltk_normalized = split_leading_punct(text=text_cltk_normalized)
    text_cltk_normalized = remove_odd_punct(text=text_cltk_normalized)
    if drop_macrons:
        text_cltk_normalized = remove_macrons(text_cltk_normalized)
    if drop_accents:
        text_cltk_normalized = remove_accents(text_cltk_normalized)
    if jv_replacement:
        text_cltk_normalized = JV_REPLACER.replace(text_cltk_normalized)
    if ligature_replacement:
        text_cltk_normalized = LIGATURE_REPLACER.replace(text_cltk_normalized)
    return text_cltk_normalized
