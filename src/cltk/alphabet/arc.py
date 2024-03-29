"""The Imperial Aramaic alphabet, plus simple script to transform
a Hebrew transcription of an Imperial Aramaic text to its own Unicode block.

TODO: Add Hebrew-to-Aramaic converter
"""
from typing import Union

IMPERIAL_ARAMAIC_BLOCK: list[tuple[str, str, str]] = [
    # Imperial Aramaic block as it is provided
    # by https://www.unicode.org/charts/PDF/U10840.pdf
    # The Unicode Standard, Version 13.0
    ("10840", "IMPERIAL ARAMAIC LETTER ALEPH", "\N{IMPERIAL ARAMAIC LETTER ALEPH}"),
    ("10841", "IMPERIAL ARAMAIC LETTER BETH", "\N{IMPERIAL ARAMAIC LETTER BETH}"),
    ("10842", "IMPERIAL ARAMAIC LETTER GIMEL", "\N{IMPERIAL ARAMAIC LETTER GIMEL}"),
    ("10843", "IMPERIAL ARAMAIC LETTER DALETH", "\N{IMPERIAL ARAMAIC LETTER DALETH}"),
    ("10844", "IMPERIAL ARAMAIC LETTER HE", "\N{IMPERIAL ARAMAIC LETTER HE}"),
    ("10845", "IMPERIAL ARAMAIC LETTER WAW", "\N{IMPERIAL ARAMAIC LETTER WAW}"),
    ("10846", "IMPERIAL ARAMAIC LETTER ZAYIN", "\N{IMPERIAL ARAMAIC LETTER ZAYIN}"),
    ("10847", "IMPERIAL ARAMAIC LETTER HETH", "\N{IMPERIAL ARAMAIC LETTER HETH}"),
    ("10848", "IMPERIAL ARAMAIC LETTER TETH", "\N{IMPERIAL ARAMAIC LETTER TETH}"),
    ("10849", "IMPERIAL ARAMAIC LETTER YODH", "\N{IMPERIAL ARAMAIC LETTER YODH}"),
    ("1084A", "IMPERIAL ARAMAIC LETTER KAPH", "\N{IMPERIAL ARAMAIC LETTER KAPH}"),
    ("1084B", "IMPERIAL ARAMAIC LETTER LAMEDH", "\N{IMPERIAL ARAMAIC LETTER LAMEDH}"),
    ("1084C", "IMPERIAL ARAMAIC LETTER MEM", "\N{IMPERIAL ARAMAIC LETTER MEM}"),
    ("1084D", "IMPERIAL ARAMAIC LETTER NUN", "\N{IMPERIAL ARAMAIC LETTER NUN}"),
    ("1084E", "IMPERIAL ARAMAIC LETTER SAMEKH", "\N{IMPERIAL ARAMAIC LETTER SAMEKH}"),
    ("1084F", "IMPERIAL ARAMAIC LETTER AYIN", "\N{IMPERIAL ARAMAIC LETTER AYIN}"),
    ("10850", "IMPERIAL ARAMAIC LETTER PE", "\N{IMPERIAL ARAMAIC LETTER PE}"),
    ("10851", "IMPERIAL ARAMAIC LETTER SADHE", "\N{IMPERIAL ARAMAIC LETTER SADHE}"),
    ("10852", "IMPERIAL ARAMAIC LETTER QOPH", "\N{IMPERIAL ARAMAIC LETTER QOPH}"),
    ("10853", "IMPERIAL ARAMAIC LETTER RESH", "\N{IMPERIAL ARAMAIC LETTER RESH}"),
    ("10854", "IMPERIAL ARAMAIC LETTER SHIN", "\N{IMPERIAL ARAMAIC LETTER SHIN}"),
    ("10855", "IMPERIAL ARAMAIC LETTER TAW", "\N{IMPERIAL ARAMAIC LETTER TAW}"),
    ("10857", "IMPERIAL ARAMAIC SECTION SIGN", "\N{IMPERIAL ARAMAIC SECTION SIGN}"),
    ("10858", "IMPERIAL ARAMAIC NUMBER ONE", "\N{IMPERIAL ARAMAIC NUMBER ONE}"),
    ("10859", "IMPERIAL ARAMAIC NUMBER TWO", "\N{IMPERIAL ARAMAIC NUMBER TWO}"),
    ("1085A", "IMPERIAL ARAMAIC NUMBER THREE", "\N{IMPERIAL ARAMAIC NUMBER THREE}"),
    ("1085B", "IMPERIAL ARAMAIC NUMBER TEN", "\N{IMPERIAL ARAMAIC NUMBER TEN}"),
    ("1085C", "IMPERIAL ARAMAIC NUMBER TWENTY", "\N{IMPERIAL ARAMAIC NUMBER TWENTY}"),
    (
        "1085D",
        "IMPERIAL ARAMAIC NUMBER ONE HUNDRED",
        "\N{IMPERIAL ARAMAIC NUMBER ONE HUNDRED}",
    ),
    (
        "1085E",
        "IMPERIAL ARAMAIC NUMBER ONE THOUSAND",
        "\N{IMPERIAL ARAMAIC NUMBER ONE THOUSAND}",
    ),
    (
        "1085F",
        "IMPERIAL ARAMAIC NUMBER TEN THOUSAND",
        "\N{IMPERIAL ARAMAIC NUMBER TEN THOUSAND}",
    ),
]

ARAMAIC_CHAR_TABLE: list[Union[tuple[str, str], tuple[str, str, str]]] = [
    # Equivalencies are provided based on
    # Skeleton Achaemenid Aramaic Grammar
    # http://arshama.classics.ox.ac.uk/aramaic/
    ("\N{IMPERIAL ARAMAIC LETTER ALEPH}", "א"),
    ("\N{IMPERIAL ARAMAIC LETTER BETH}", "ב"),
    ("\N{IMPERIAL ARAMAIC LETTER GIMEL}", "ג"),
    ("\N{IMPERIAL ARAMAIC LETTER DALETH}", "ד"),
    ("\N{IMPERIAL ARAMAIC LETTER HE}", "ה"),
    ("\N{IMPERIAL ARAMAIC LETTER WAW}", "ו"),
    ("\N{IMPERIAL ARAMAIC LETTER ZAYIN}", "ז"),
    ("\N{IMPERIAL ARAMAIC LETTER HETH}", "ח"),
    ("\N{IMPERIAL ARAMAIC LETTER TETH}", "ט"),
    ("\N{IMPERIAL ARAMAIC LETTER YODH}", "י"),
    ("\N{IMPERIAL ARAMAIC LETTER KAPH}", "כ", "ך"),
    ("\N{IMPERIAL ARAMAIC LETTER LAMEDH}", "ל"),
    ("\N{IMPERIAL ARAMAIC LETTER MEM}", "מ", "ם"),
    ("\N{IMPERIAL ARAMAIC LETTER NUN}", "נ", "ן"),
    ("\N{IMPERIAL ARAMAIC LETTER SAMEKH}", "ס"),
    ("\N{IMPERIAL ARAMAIC LETTER AYIN}", "ע"),
    ("\N{IMPERIAL ARAMAIC LETTER PE}", "פ", "ף"),
    ("\N{IMPERIAL ARAMAIC LETTER SADHE}", "צ", "ץ"),
    ("\N{IMPERIAL ARAMAIC LETTER QOPH}", "ק"),
    ("\N{IMPERIAL ARAMAIC LETTER RESH}", "ר"),
    ("\N{IMPERIAL ARAMAIC LETTER SHIN}", "שׁ"),
    ("\N{IMPERIAL ARAMAIC LETTER TAW}", "ת"),
    ("\N{IMPERIAL ARAMAIC SECTION SIGN}", "§"),
    ("\N{IMPERIAL ARAMAIC NUMBER ONE}", "1"),
    ("\N{IMPERIAL ARAMAIC NUMBER TWO}", "2"),
    ("\N{IMPERIAL ARAMAIC NUMBER THREE}", "3"),
    ("\N{IMPERIAL ARAMAIC NUMBER TEN}", "10"),
    ("\N{IMPERIAL ARAMAIC NUMBER TWENTY}", "20"),
    ("\N{IMPERIAL ARAMAIC NUMBER ONE HUNDRED}", "100"),
    ("\N{IMPERIAL ARAMAIC NUMBER ONE THOUSAND}", "1000"),
    ("\N{IMPERIAL ARAMAIC NUMBER TEN THOUSAND}", "10000"),
]


def _imperial_to_square_table() -> list[tuple[str, str]]:
    new_table: list[tuple[str, str]] = list()
    for _tuple in ARAMAIC_CHAR_TABLE:
        if len(_tuple) > 2:
            new_table.append((_tuple[1], _tuple[0]))
            new_table.append((_tuple[2], _tuple[0]))
        else:
            new_table.append((_tuple[1], _tuple[0]))
    return new_table


SQUARE_TO_IMPERIAL_TABLE: list[tuple[str, str]] = _imperial_to_square_table()
# SQUARE_TO_IMPERIAL = {k: v for k, v in SQUARE_TO_IMPERIAL_TABLE}
SQUARE_TO_IMPERIAL: dict[str, str] = dict(SQUARE_TO_IMPERIAL_TABLE)


def _square_to_imperial_char(_str: str) -> str:
    return SQUARE_TO_IMPERIAL[_str] if _str in SQUARE_TO_IMPERIAL else _str


def square_to_imperial(square_script: str) -> str:
    """simple script to transform a Hebrew transcription
    of an Imperial Aramaic text to its own unicode block
    """
    return "".join(map(_square_to_imperial_char, square_script))
