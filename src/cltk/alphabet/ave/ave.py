"""The Avestan alphabet. Sources:

- `<https://www.unicode.org/charts/PDF/U10B00.pdf>`_

"""

__author__ = [
        "Caio Geraldes <caio.geraldes@usp.br>"]


VOWELS = [
    "\U00010B00", # 𐬀  AVESTAN LETTER A
    "\U00010B01", # 𐬁  AVESTAN LETTER AA
    "\U00010B02", # 𐬂  AVESTAN LETTER AO
    "\U00010B03", # 𐬃  AVESTAN LETTER AAO
    "\U00010B04", # 𐬄  AVESTAN LETTER AN
    "\U00010B05", # 𐬅  AVESTAN LETTER AAN
    "\U00010B06", # 𐬆  AVESTAN LETTER AE
    "\U00010B07", # 𐬇  AVESTAN LETTER AEE
    "\U00010B08", # 𐬈  AVESTAN LETTER E
    "\U00010B09", # 𐬉  AVESTAN LETTER EE
    "\U00010B0A", # 𐬊  AVESTAN LETTER O
    "\U00010B0B", # 𐬋  AVESTAN LETTER OO
    "\U00010B0C", # 𐬌  AVESTAN LETTER I
    "\U00010B0D", # 𐬍  AVESTAN LETTER II
    "\U00010B0E", # 𐬎  AVESTAN LETTER U
    "\U00010B0F"  # 𐬏  AVESTAN LETTER UU
]

CONSONANTS = [
    "\U00010B10", # 𐬐 AVESTAN LETTER KE
    "\U00010B11", # 𐬑 AVESTAN LETTER XE
    "\U00010B12", # 𐬒 AVESTAN LETTER XYE
    "\U00010B13", # 𐬓 AVESTAN LETTER XVE
    "\U00010B14", # 𐬔 AVESTAN LETTER GE
    "\U00010B15", # 𐬕 AVESTAN LETTER GGE
    "\U00010B16", # 𐬖 AVESTAN LETTER GHE
    "\U00010B17", # 𐬗 AVESTAN LETTER CE
    "\U00010B18", # 𐬘 AVESTAN LETTER JE
    "\U00010B19", # 𐬙 AVESTAN LETTER TE
    "\U00010B1A", # 𐬚 AVESTAN LETTER THE
    "\U00010B1B", # 𐬛 AVESTAN LETTER DE
    "\U00010B1C", # 𐬜 AVESTAN LETTER DHE
    "\U00010B1D", # 𐬝 AVESTAN LETTER TTE
    "\U00010B1E", # 𐬞 AVESTAN LETTER PE
    "\U00010B1F", # 𐬟 AVESTAN LETTER FE
    "\U00010B20", # 𐬠 AVESTAN LETTER BE
    "\U00010B21", # 𐬡 AVESTAN LETTER BHE
    "\U00010B22", # 𐬢 AVESTAN LETTER NGE
    "\U00010B23", # 𐬣 AVESTAN LETTER NGYE
    "\U00010B24", # 𐬤 AVESTAN LETTER NGVE
    "\U00010B25", # 𐬥 AVESTAN LETTER NE
    "\U00010B26", # 𐬦 AVESTAN LETTER NYE
    "\U00010B27", # 𐬧 AVESTAN LETTER NNE
    "\U00010B28", # 𐬨 AVESTAN LETTER ME
    "\U00010B29", # 𐬩 AVESTAN LETTER HME
    "\U00010B2A", # 𐬪 AVESTAN LETTER YYE
    "\U00010B2B", # 𐬫 AVESTAN LETTER YE
    "\U00010B2C", # 𐬬 AVESTAN LETTER VE
    "\U00010B2D", # 𐬭 AVESTAN LETTER RE
    "\U00010B2E", # 𐬮 AVESTAN LETTER LE
    "\U00010B2F", # 𐬯 AVESTAN LETTER SE
    "\U00010B30", # 𐬰 AVESTAN LETTER ZE
    "\U00010B31", # 𐬱 AVESTAN LETTER SHE
    "\U00010B32", # 𐬲 AVESTAN LETTER ZHE
    "\U00010B33", # 𐬳 AVESTAN LETTER SHYE
    "\U00010B34", # 𐬴 AVESTAN LETTER SSHE
    "\U00010B35"  # 𐬵 AVESTAN LETTER HE
]

PUNCTUATION = [
    "\U00010B39", # 𐬹 AVESTAN ABBREVIATION MARK
    "\U00010B3A", # 𐬺 TINY TWO DOTS OVER ONE DOT PUNCTUATION
    "\U00010B3B", # 𐬻 SMALL TWO DOTS OVER ONE DOT PUNCTUATION
    "\U00010B3C", # 𐬼 LARGE TWO DOTS OVER ONE DOT PUNCTUATION
    "\U00010B3D", # 𐬽 LARGE ONE DOT OVER TWO DOTS PUNCTUATION
    "\U00010B3E", # 𐬾 LARGE TWO RINGS OVER ONE RING PUNCTUATION
    "\U00010B3F"  # 𐬿 LARGE ONE RING OVER TWO RINGS PUNCTUATION
]

if __name__ == "__main__":
    for letter in PUNCTUATION:
        print(letter)