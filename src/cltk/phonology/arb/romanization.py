"""Arabic transliteration, Roman <-> Arabic Unicode. This implementation is based on the following resources:

1. http://languagelog.ldc.upenn.edu/myl/ldc/morph/buckwalter.html.
2. https://github.com/Alfanous-team/alfanous/blob/master/src/alfanous/Romanization.py
3. https://en.wikipedia.org/wiki/ArabTeX
"""

__author__ = ["Lakhdar Benzahia <lakhdar.benzahia@gmail.com>"]
__license__ = "MIT License. See LICENSE."
__reviewers__ = [
    "Taha Zerrouki taha.zerrouki@gmail.com",
    "Kyle P. Johnson <kyle@kyle-p-johnson.com>",
]


BUCKWALTER_TO_UNICODE = {
    "'": "\u0621",  # hamza-on-the-line
    "|": "\u0622",  # madda
    ">": "\u0623",  # hamza-on-'alif
    "&": "\u0624",  # hamza-on-waaw
    "<": "\u0625",  # hamza-under-'alif
    "}": "\u0626",  # hamza-on-yaa'
    "A": "\u0627",  # bare 'alif
    "b": "\u0628",  # baa'
    "p": "\u0629",  # taa' marbuuTa
    "t": "\u062A",  # taa'
    "v": "\u062B",  # thaa'
    "j": "\u062C",  # jiim
    "H": "\u062D",  # Haa'
    "x": "\u062E",  # khaa'
    "d": "\u062F",  # daal
    "*": "\u0630",  # dhaal
    "r": "\u0631",  # raa'
    "z": "\u0632",  # zaay
    "s": "\u0633",  # siin
    "$": "\u0634",  # shiin
    "S": "\u0635",  # Saad
    "D": "\u0636",  # Daad
    "T": "\u0637",  # Taa'
    "Z": "\u0638",  # Zaa' (DHaa')
    "E": "\u0639",  # cayn
    "g": "\u063A",  # ghayn
    "_": "\u0640",  # taTwiil
    "f": "\u0641",  # faa'
    "q": "\u0642",  # qaaf
    "k": "\u0643",  # kaaf
    "l": "\u0644",  # laam
    "m": "\u0645",  # miim
    "n": "\u0646",  # nuun
    "h": "\u0647",  # haa'
    "w": "\u0648",  # waaw
    "Y": "\u0649",  # 'alif maqSuura
    "y": "\u064A",  # yaa'
    "F": "\u064B",  # fatHatayn
    "N": "\u064C",  # Dammatayn
    "K": "\u064D",  # kasratayn
    "a": "\u064E",  # fatHa
    "u": "\u064F",  # Damma
    "i": "\u0650",  # kasra
    "~": "\u0651",  # shaddah
    "o": "\u0652",  # sukuun
    "`": "\u0670",  # dagger 'alif
    "{": "\u0671",  # waSla
    # extended here
    "^": "\u0653",  # Maddah
    "#": "\u0654",  # HamzaAbove
    ":": "\u06DC",  # SmallHighSeen
    "@": "\u06DF",  # SmallHighRoundedZero
    '"': "\u06E0",  # SmallHighUprightRectangularZero
    "[": "\u06E2",  # SmallHighMeemIsolatedForm
    ";": "\u06E3",  # SmallLowSeen
    ",": "\u06E5",  # SmallWaw
    ".": "\u06E6",  # SmallYa
    "!": "\u06E8",  # SmallHighNoon
    "-": "\u06EA",  # EmptyCentreLowStop
    "+": "\u06EB",  # EmptyCentreHighStop
    "%": "\u06EC",  # RoundedHighStopWithFilledCentre
    "]": "\u06ED",  #
}

ISO2332_TO_UNICODE = {
    "ˌ": "\u0621",  # hamza-on-the-line
    # "|": "\u0622", # madda
    "ˈ": "\u0623",  # hamza-on-'alif
    "ˈ": "\u0624",  # hamza-on-waaw
    # "<": "\u0625", # hamza-under-'alif
    "ˈ": "\u0626",  # hamza-on-yaa'
    "ʾ": "\u0627",  # bare 'alif
    "b": "\u0628",  # baa'
    "ẗ": "\u0629",  # taa' marbuuTa
    "t": "\u062A",  # taa'
    "ṯ": "\u062B",  # thaa'
    "ǧ": "\u062C",  # jiim
    "ḥ": "\u062D",  # Haa'
    "ẖ": "\u062E",  # khaa'
    "d": "\u062F",  # daal
    "ḏ": "\u0630",  # dhaal
    "r": "\u0631",  # raa'
    "z": "\u0632",  # zaay
    "s": "\u0633",  # siin
    "š": "\u0634",  # shiin
    "ṣ": "\u0635",  # Saad
    "ḍ": "\u0636",  # Daad
    "ṭ": "\u0637",  # Taa'
    "ẓ": "\u0638",  # Zaa' (DHaa')
    "ʿ": "\u0639",  # cayn
    "ġ": "\u063A",  # ghayn
    # "_": "\u0640", # taTwiil
    "f": "\u0641",  # faa'
    "q": "\u0642",  # qaaf
    "k": "\u0643",  # kaaf
    "l": "\u0644",  # laam
    "m": "\u0645",  # miim
    "n": "\u0646",  # nuun
    "h": "\u0647",  # haa'
    "w": "\u0648",  # waaw
    "ỳ": "\u0649",  # 'alif maqSuura
    "y": "\u064A",  # yaa'
    "á": "\u064B",  # fatHatayn
    "ú": "\u064C",  # Dammatayn
    "í": "\u064D",  # kasratayn
    "a": "\u064E",  # fatHa
    "u": "\u064F",  # Damma
    "i": "\u0650",  # kasra
    # "~": "\u0651", # shaddah
    "°": "\u0652",  # sukuun
    # "`": "\u0670", # dagger 'alif
    # "{": "\u0671", # waSla
    ##extended here
    # "^": "\u0653", # Maddah
    # "#": "\u0654", # HamzaAbove
    # ":": "\u06DC", # SmallHighSeen
    # "@": "\u06DF", # SmallHighRoundedZero
    # "\": "\u06E0", # SmallHighUprightRectangularZero
    # "[": "\u06E2", # SmallHighMeemIsolatedForm
    # ";": "\u06E3", # SmallLowSeen
    # ",": "\u06E5", # SmallWaw
    # ".": "\u06E6", # SmallYa
    # "!": "\u06E8", # SmallHighNoon
    # "-": "\u06EA", # EmptyCentreLowStop
    # "+": "\u06EB", # EmptyCentreHighStop
    # "%": "\u06EC", # RoundedHighStopWithFilledCentre
    # "]": "\u06ED"          #
}

ARABTEX_TO_UNICODE = {
    "'": "\u0621",  # hamza-on-the-line
    # "|": "\u0622", # madda
    "a'": "\u0623",  # hamza-on-'alif
    "U'": "\u0624",  # hamza-on-waaw
    # "<": "\u0625", # hamza-under-'alif
    "'y": "\u0626",  # hamza-on-yaa'
    "A": "\u0627",  # bare 'alif
    "b": "\u0628",  # baa'
    "T": "\u0629",  # taa' marbuuTa
    "t": "\u062A",  # taa'
    "_t": "\u062B",  # thaa'
    "j": "\u062C",  # jiim
    ".h": "\u062D",  # Haa'
    "x": "\u062E",  # khaa'
    "d": "\u062F",  # daal
    "_d": "\u0630",  # dhaal
    "r": "\u0631",  # raa'
    "z": "\u0632",  # zaay
    "s": "\u0633",  # siin
    "^s": "\u0634",  # shiin
    ".s": "\u0635",  # Saad
    ".d": "\u0636",  # Daad
    ".t": "\u0637",  # Taa'
    ".z": "\u0638",  # Zaa' (DHaa')
    "`": "\u0639",  # cayn
    ".g": "\u063A",  # ghayn
    # "_": "\u0640", # taTwiil # Missing
    "f": "\u0641",  # faa'
    "q": "\u0642",  # qaaf
    "k": "\u0643",  # kaaf
    "l": "\u0644",  # laam
    "m": "\u0645",  # miim
    "n": "\u0646",  # nuun
    "h": "\u0647",  # haa'
    "w": "\u0648",  # waaw
    "I*": "\u0649",  # 'alif maqSuura
    "y": "\u064A",  # yaa'
    "aN": "\u064B",  # fatHatayn
    "uN": "\u064C",  # Dammatayn
    "iN": "\u064D",  # kasratayn
    "a": "\u064E",  # fatHa
    "u": "\u064F",  # Damma
    "i": "\u0650",  # kasra
    "xx": "\u0651",  # shaddah
    # "": "\u0652", # sukuun    Missing
    # "": "\u0670", # dagger 'alif Missing
    # "": "\u0671", # waSla Missing
    # extended here
    # "": "\u0653", # Maddah Missing
    # "": "\u0654", # HamzaAbove Missing
    # "": "\u06DC", # SmallHighSeen Missing
    # "": "\u06DF", # SmallHighRoundedZero Missing
    # """: "\u06E0", # SmallHighUprightRectangularZero Missing
    # "": "\u06E2", # SmallHighMeemIsolatedForm Missing
    # "": "\u06E3", # SmallLowSeen Missing
    # "": "\u06E5", # SmallWaw Missing
    # "": "\u06E6", # SmallYa Missing
    # "": "\u06E8", # SmallHighNoon Missing
    # "": "\u06EA", # EmptyCentreLowStop Missing
    # "": "\u06EB", # EmptyCentreHighStop Missing
    # "": "\u06EC", # RoundedHighStopWithFilledCentre Missing
    # "": "\u06ED"  # Missing
}

ASMO449_TO_UNICODE = {
    "A": "\u0621",  # hamza-on-the-line
    "B": "\u0622",  # madda
    "C": "\u0623",  # hamza-on-'alif
    "D": "\u0624",  # hamza-on-waaw
    "E": "\u0625",  # hamza-under-'alif
    "F": "\u0626",  # hamza-on-yaa'
    "G": "\u0627",  # bare 'alif
    "H": "\u0628",  # baa'
    "I": "\u0629",  # taa' marbuuTa
    "J": "\u062A",  # taa'
    "K": "\u062B",  # thaa'
    "L": "\u062C",  # jiim
    "M": "\u062D",  # Haa'
    "N": "\u062E",  # khaa'
    "O": "\u062F",  # daal
    "P": "\u0630",  # dhaal
    "Q": "\u0631",  # raa'
    "R": "\u0632",  # zaay
    "S": "\u0633",  # siin
    "T": "\u0634",  # shiin
    "U": "\u0635",  # Saad
    "V": "\u0636",  # Daad
    "W": "\u0637",  # Taa'
    "X": "\u0638",  # Zaa' (DHaa')
    "Y": "\u0639",  # cayn
    "Z": "\u063A",  # ghayn
    "0x60": "\u0640",  # taTwiil
    "a": "\u0641",  # faa'
    "b": "\u0642",  # qaaf
    "c": "\u0643",  # kaaf
    "d": "\u0644",  # laam
    "e": "\u0645",  # miim
    "f": "\u0646",  # nuun
    "g": "\u0647",  # haa'
    "h": "\u0648",  # waaw
    "i": "\u0649",  # 'alif maqSuura
    "j": "\u064A",  # yaa'
    "k": "\u064B",  # fatHatayn
    "l": "\u064C",  # Dammatayn
    "m": "\u064D",  # kasratayn
    "n": "\u064E",  # fatHa
    "o": "\u064F",  # Damma
    "p": "\u0650",  # kasra
    "q": "\u0651",  # shaddah
    "r": "\u0652",  # sukuun
    # "": "\u0670", # dagger 'alif missing
    # "": "\u0671", # waSla missing
    # extended here
    # "": "\u0653", # Maddah  missing
    # "": "\u0654", # HamzaAbove missing
    # "": "\u06DC", # SmallHighSeen missing
    # "": "\u06DF", # SmallHighRoundedZero missing
    # """: "\u06E0", # SmallHighUprightRectangularZero  missing
    # "": "\u06E2", # SmallHighMeemIsolatedForm  missing
    # "": "\u06E3", # SmallLowSeen missing
    # "": "\u06E5", # SmallWaw missing
    # "": "\u06E6", # SmallYa  missing
    # "": "\u06E8", # SmallHighNoon  missing
    # "": "\u06EA", # EmptyCentreLowStop missing
    # "": "\u06EB", # EmptyCentreHighStop missing
    # "": "\u06EC", # RoundedHighStopWithFilledCentre missing
    # "": "\u06ED"  # missing
}

ISO88596_TO_UNICODE = {
    "C1": "\u0621",  # hamza-on-the-line
    "C2": "\u0622",  # madda
    "C3": "\u0623",  # hamza-on-'alif
    "C4": "\u0624",  # hamza-on-waaw
    "C5": "\u0625",  # hamza-under-'alif
    "C6": "\u0626",  # hamza-on-yaa'
    "C7": "\u0627",  # bare 'alif
    "C8": "\u0628",  # baa'
    "C9": "\u0629",  # taa' marbuuTa
    "CA": "\u062A",  # taa'
    "CB": "\u062B",  # thaa'
    "CC": "\u062C",  # jiim
    "CD": "\u062D",  # Haa'
    "CE": "\u062E",  # khaa'
    "CF": "\u062F",  # daal
    "D0": "\u0630",  # dhaal
    "D1": "\u0631",  # raa'
    "D2": "\u0632",  # zaay
    "D3": "\u0633",  # siin
    "D4": "\u0634",  # shiin
    "D5": "\u0635",  # Saad
    "D6": "\u0636",  # Daad
    "D7": "\u0637",  # Taa'
    "D8": "\u0638",  # Zaa' (DHaa')
    "D9": "\u0639",  # cayn
    "DA": "\u063A",  # ghayn
    "E0": "\u0640",  # taTwiil missing
    "E1": "\u0641",  # faa'
    "E2": "\u0642",  # qaaf
    "E3": "\u0643",  # kaaf
    "E4": "\u0644",  # laam
    "E5": "\u0645",  # miim
    "E6": "\u0646",  # nuun
    "E7": "\u0647",  # haa'
    "E8": "\u0648",  # waaw
    "E9": "\u0649",  # 'alif maqSuura
    "EA": "\u064A",  # yaa'
    "EB": "\u064B",  # fatHatayn
    "EC": "\u064C",  # Dammatayn
    "ED": "\u064D",  # kasratayn
    "EE": "\u064E",  # fatHa
    "EF": "\u064F",  # Damma
    "F0": "\u0650",  # kasra
    "F1": "\u0651",  # shaddah
    "F2": "\u0652",  # sukuun
    # "": "\u0670", # dagger 'alif missing
    # "": "\u0671", # waSla missing
    # extended here
    # "": "\u0653", # Maddah  missing
    # "": "\u0654", # HamzaAbove missing
    # "": "\u06DC", # SmallHighSeen missing
    # "": "\u06DF", # SmallHighRoundedZero missing
    # """: "\u06E0", # SmallHighUprightRectangularZero  missing
    # "": "\u06E2", # SmallHighMeemIsolatedForm  missing
    # "": "\u06E3", # SmallLowSeen missing
    # "": "\u06E5", # SmallWaw missing
    # "": "\u06E6", # SmallYa  missing
    # "": "\u06E8", # SmallHighNoon  missing
    # "": "\u06EA", # EmptyCentreLowStop missing
    # "": "\u06EB", # EmptyCentreHighStop missing
    # "": "\u06EC", # RoundedHighStopWithFilledCentre missing
    # "": "\u06ED"  # missing
}

ROMANIZATION_SYSTEMS_MAPPINGS = {
    "buckwalter": BUCKWALTER_TO_UNICODE,
    "iso233-2": ISO2332_TO_UNICODE,
    # "arabtex": ARABTEX_TO_UNICODE, todo: not ready
    "asmo449": ASMO449_TO_UNICODE,
    # "iso8859-6": ISO88596_TO_UNICODE, todo: not ready
}


def available_transliterate_systems():
    return list(ROMANIZATION_SYSTEMS_MAPPINGS.keys())


def guess_romaization_system():
    # @todo
    pass


def transliterate(mode, string, ignore="", reverse=False):
    # @todo: arabtex and iso8859-6 need individual handling because in some cases using one-two mapping
    """
    encode & decode different  romanization systems
    :param mode:
    :param string:
    :param ignore:
    :param reverse:
    :return:
    """

    if mode in available_transliterate_systems():
        MAPPING = ROMANIZATION_SYSTEMS_MAPPINGS[mode]
    else:
        print(mode + "  not supported! \n")
        MAPPING = {}

    if reverse:
        mapping = {}
        for k, v in MAPPING.items():
            # reverse the mapping buckwalter <-> unicode
            mapping[v] = k
    else:
        mapping = MAPPING

    result = ""
    for char in string:
        if char in mapping.keys() and char not in ignore:
            result += mapping[char]
        else:
            result += char
    return result
