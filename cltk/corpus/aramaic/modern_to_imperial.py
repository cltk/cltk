# simple script to transform a hebrew transcription of an imperial aramaic
# text to its own unicode block

IMPERIAL_ARAMAIC_BLOCK = [
    # Imperial Aramaic block as it is provided
    # by https://www.unicode.org/charts/PDF/U10840.pdf
    # The Unicode Standard, Version 13.0
    ("10840", "", "IMPERIAL ARAMAIC LETTER ALEPH"),
    ("10841", "", "IMPERIAL ARAMAIC LETTER BETH"),
    ("10842", "", "IMPERIAL ARAMAIC LETTER GIMEL"),
    ("10843", "", "IMPERIAL ARAMAIC LETTER DALETH"),
    ("10844", "", "IMPERIAL ARAMAIC LETTER HE"),
    ("10845", "", "IMPERIAL ARAMAIC LETTER WAW"),
    ("10846", "", "IMPERIAL ARAMAIC LETTER ZAYIN"),
    ("10847", "", "IMPERIAL ARAMAIC LETTER HETH"),
    ("10848", "", "IMPERIAL ARAMAIC LETTER TETH"),
    ("10849", "", "IMPERIAL ARAMAIC LETTER YODH"),
    ("1084A", "", "IMPERIAL ARAMAIC LETTER KAPH"),
    ("1084B", "", "IMPERIAL ARAMAIC LETTER LAMEDH"),
    ("1084C", "", "IMPERIAL ARAMAIC LETTER MEM"),
    ("1084D", "", "IMPERIAL ARAMAIC LETTER NUN"),
    ("1084E", "", "IMPERIAL ARAMAIC LETTER SAMEKH"),
    ("1084F", "", "IMPERIAL ARAMAIC LETTER AYIN"),
    ("10850", "", "IMPERIAL ARAMAIC LETTER PE"),
    ("10851", "", "IMPERIAL ARAMAIC LETTER SADHE"),
    ("10852", "", "IMPERIAL ARAMAIC LETTER QOPH"),
    ("10853", "", "IMPERIAL ARAMAIC LETTER RESH"),
    ("10854", "", "IMPERIAL ARAMAIC LETTER SHIN"),
    ("10855", "", "IMPERIAL ARAMAIC LETTER TAW"),
    ("10857", "", "IMPERIAL ARAMAIC SECTION SIGN"),
    ("10858", "", "IMPERIAL ARAMAIC NUMBER ONE"),
    ("10859", "", "IMPERIAL ARAMAIC NUMBER TWO"),
    ("1085A", "", "IMPERIAL ARAMAIC NUMBER THREE"),
    ("1085B", "", "IMPERIAL ARAMAIC NUMBER TEN"),
    ("1085C", "", "IMPERIAL ARAMAIC NUMBER TWENTY"),
    ("1085D", "", "IMPERIAL ARAMAIC NUMBER ONE HUNDRED"),
    ("1085E", "", "IMPERIAL ARAMAIC NUMBER ONE THOUSAND"),
    ("1085F", "", "IMPERIAL ARAMAIC NUMBER TEN THOUSAND"),
]

TABLE = [
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


def imperial_to_square_table():
    new_table = []
    for el in TABLE:
        if len(el) > 2:
            new_table.append((el[1], el[0]))
            new_table.append((el[2], el[0]))
        else:
            new_table.append((el[1], el[0]))
    return new_table


SQUARE_TO_IMPERIAL_TABLE = imperial_to_square_table()
SQUARE_TO_IMPERIAL = {k: v for k, v in SQUARE_TO_IMPERIAL_TABLE}


def square_to_imperial_char(s: str) -> str:
    return SQUARE_TO_IMPERIAL[s] if s in SQUARE_TO_IMPERIAL else s


def square_to_imperial(square_script: str) -> str:
    return "".join(map(square_to_imperial_char, square_script))
