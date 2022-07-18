"""Converts legacy encodings into Unicode.

TODO: Rm regex dependency
TODO: Add tests
"""

# pylint: disable=anomalous-backslash-in-string

import regex
from unicodedata import normalize

BETA_REPLACE = [
    (r"S|\*[sS]", "Σ"),
    (r"B|\*[bB]", "Β"),
    (r"G|\*[gG]", "Γ"),
    (r"D|\*[dD]", "Δ"),
    (r"Z|\*[zZ]", "Ζ"),
    (r"Q|\*[qQ]", "Θ"),
    (r"K|\*[kK]", "Κ"),
    (r"L|\*[lL]", "Λ"),
    (r"M|\*[mM]", "Μ"),
    (r"N|\*[nN]", "Ν"),
    (r"C|\*[cC]", "Ξ"),
    (r"P|\*[pP]", "Π"),
    (r"R|\*[rR]", "Ρ"),
    (r"T|\*[tT]", "Τ"),
    (r"Y|\*[yY]", "Ψ"),
    (r"X|\*[xX]", "Χ"),
    (r"F|\*[fF]", "Φ"),
    (r"A|\*[aA]", "Α"),
    (r"E|\*[eE]", "Ε"),
    (r"H|\*[hH]", "Η"),
    (r"I|\*[iI]", "Ι"),
    (r"O|\*[oO]", "Ο"),
    (r"U|\*[uU]", "Υ"),
    (r"W|\*[wW]", "Ω"),
    (r"s([ ,.;])", r"ς\1"),
    (r"s\Z", r"ς"),
    (r"s", "σ"),
    (r"b", "β"),
    (r"g", "γ"),
    (r"d", "δ"),
    (r"z", "ζ"),
    (r"q", "θ"),
    (r"k", "κ"),
    (r"l", "λ"),
    (r"m", "μ"),
    (r"n", "ν"),
    (r"c", "ξ"),
    (r"p", "π"),
    (r"t", "τ"),
    (r"y", "ψ"),
    (r"x", "χ"),
    (r"f", "φ"),
    (r"r", "ρ"),
    (r"a", "α"),
    (r"e", "ε"),
    (r"h", "η"),
    (r"i", "ι"),
    (r"o", "ο"),
    (r"u", "υ"),
    (r"w", "ω"),
    (r"σ3", "\u03f2"),
    (r"Σ3", "\u03f9"),
    # fixed σ
    (r"σ2", "σ"),
    # koppa
    (r"\*#2", "\u03de"),
    (r"#2", "\u03df"),
    # koppa (archaic)
    (r"\*#3", "\u03d8"),
    (r"#3", "\u03d9"),
    # sampi
    (r"\*#4", "\u03e0"),
    (r"#4", "\u03e1"),
    # Diacritics
    # breathings
    (r"\)", "\u0313"),
    (r"\(", "\u0314"),
    (r"\+", "\u0308"),
    # accents
    (r"\\", "\u0300"),
    (r"\/", "\u0301"),
    (r"=", "\u0342"),
    # subscript iota
    (r"\|", "\u0345"),
    # dot below
    (r"\?", "\u0323"),
    # breve
    (r"%27", "\u0306"),
    # longa / macron
    (r"%26", "\u0304"),
    # Punctuation
    # middle dot
    (r":", "\u00b7"),
    (r"'", "\u02bc"),
]

BETA_REORDER = [
    # Brings breathings and diairesis first, then accents, then subscript iota
    (r"([\\/=])(\|)?([()+])?", r"\3\1\2"),
    # Makes sure the upper case marking is followed by the letter and only then
    # the diacritics markers come
    (r"\A(\*)?([()+])?([\\/=])?(\|)?(\w)", r"\1\5\2\3\4"),
]


class BetaCodeReplacer:
    """Replace Beta Code with Unicode.

    >>> from cltk.alphabet.grc.beta_to_unicode import BetaCodeReplacer
    >>> beta_code_replace = BetaCodeReplacer()
    >>> beta_code_str = "O(/PWS OU)=N MH\ TAU)TO\ "
    >>> beta_code_replace.replace_beta_code(beta_code_str)
    'ὅπως οὖν μὴ ταὐτὸ '
    >>> beta_code_str = "PROU+POTETAGME/NWN"
    >>> beta_code_replace.replace_beta_code(beta_code_str)
    'προϋποτεταγμένων'
    """

    def __init__(self, pattern=None, reorder_pattern=None):
        if pattern is None:
            pattern = BETA_REPLACE
        if reorder_pattern is None:
            reorder_pattern = BETA_REORDER
        self.pattern = [
            (regex.compile(beta_regex, flags=regex.VERSION1), repl)
            for (beta_regex, repl) in pattern
        ]
        self.reorder_pattern = [
            (regex.compile(beta_regex, flags=regex.VERSION1), repl)
            for (beta_regex, repl) in reorder_pattern
        ]

    def replace_beta_code(self, text: str) -> str:
        """Replace method. Note: regex.subn() returns a tuple (new_string,
        number_of_subs_made).

        >>> from cltk.alphabet.grc.beta_to_unicode import BetaCodeReplacer
        >>> beta_code_replace = BetaCodeReplacer()
        >>> beta_code_str = r"*XALDAI+KH\\N"  # extra slash in ``\\N`` only here for doctest
        >>> beta_code_replace.replace_beta_code(beta_code_str)
        'Χαλδαϊκὴν'
        >>> beta_code_str = "proi+sxome/nwn"
        >>> beta_code_replace.replace_beta_code(beta_code_str)
        'προϊσχομένων'
        """

        # Accounts for cases in which the whole string is upper case, leaving only
        # the uppers marked by asterisks
        if text.isupper():
            text = regex.sub(r"(?<!\*)([A-Z]+)", lambda pat: pat.group(1).lower(), text)
        text = text.replace("-", "")
        for (pattern, repl) in self.reorder_pattern:
            text = pattern.subn(repl, text)[0]
        for (pattern, repl) in self.pattern:
            text = pattern.subn(repl, text)[0]
        return normalize("NFC", text)
