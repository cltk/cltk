"""
   Convert an arabic word written in arabic native script to roman script using
   (Buckwalter, ISO233-2, arabtex, ISO 8859-6,ASMO 449, Windows 1256) Romanization systmes to unicode

   To validate: this implementation rely largely on these resources:
            1. http://languagelog.ldc.upenn.edu/myl/ldc/morph/buckwalter.html.
            2. https://github.com/Alfanous-team/alfanous/blob/master/src/alfanous/Romanization.py
            3. https://en.wikipedia.org/wiki/ArabTeX
"""

__author__ = ['Lakhdar Benzahia, <lakhdar.benzahia@gmail.com>']
__license__ = 'MIT License. See LICENSE.'
__reviewers__ = ['Taha Zerrouki taha.zerrouki@gmail.com', 'Kyle P. Johnson <kyle@kyle-p-johnson.com>']


BUCKWALTER_2_UNICODE = {"'": "\u0621", # hamza-on-the-line
                        "|": "\u0622", # madda
                        ">": "\u0623", # hamza-on-'alif
                        "&": "\u0624", # hamza-on-waaw
                        "<": "\u0625", # hamza-under-'alif
                        "}": "\u0626", # hamza-on-yaa'
                        "A": "\u0627", # bare 'alif
                        "b": "\u0628", # baa'
                        "p": "\u0629", # taa' marbuuTa
                        "t": "\u062A", # taa'
                        "v": "\u062B", # thaa'
                        "j": "\u062C", # jiim
                        "H": "\u062D", # Haa'
                        "x": "\u062E", # khaa'
                        "d": "\u062F", # daal
                        "*": "\u0630", # dhaal
                        "r": "\u0631", # raa'
                        "z": "\u0632", # zaay
                        "s": "\u0633", # siin
                        "$": "\u0634", # shiin
                        "S": "\u0635", # Saad
                        "D": "\u0636", # Daad
                        "T": "\u0637", # Taa'
                        "Z": "\u0638", # Zaa' (DHaa')
                        "E": "\u0639", # cayn
                        "g": "\u063A", # ghayn
                        "_": "\u0640", # taTwiil
                        "f": "\u0641", # faa'
                        "q": "\u0642", # qaaf
                        "k": "\u0643", # kaaf
                        "l": "\u0644", # laam
                        "m": "\u0645", # miim
                        "n": "\u0646", # nuun
                        "h": "\u0647", # haa'
                        "w": "\u0648", # waaw
                        "Y": "\u0649", # 'alif maqSuura
                        "y": "\u064A", # yaa'
                        "F": "\u064B", # fatHatayn
                        "N": "\u064C", # Dammatayn
                        "K": "\u064D", # kasratayn
                        "a": "\u064E", # fatHa
                        "u": "\u064F", # Damma
                        "i": "\u0650", # kasra
                        "~": "\u0651", # shaddah
                        "o": "\u0652", # sukuun
                        "`": "\u0670", # dagger 'alif
                        "{": "\u0671", # waSla
                        #extended here
                        "^": "\u0653", # Maddah
                        "#": "\u0654", # HamzaAbove

                        ":": "\u06DC", # SmallHighSeen
                        "@": "\u06DF", # SmallHighRoundedZero
                        "\"": "\u06E0", # SmallHighUprightRectangularZero
                        "[": "\u06E2", # SmallHighMeemIsolatedForm
                        ";": "\u06E3", # SmallLowSeen
                        ",": "\u06E5", # SmallWaw
                        ".": "\u06E6", # SmallYa
                        "!": "\u06E8", # SmallHighNoon
                        "-": "\u06EA", # EmptyCentreLowStop
                        "+": "\u06EB", # EmptyCentreHighStop
                        "%": "\u06EC", # RoundedHighStopWithFilledCentre
                        "]": "\u06ED"          #

                }


ISO2332_TO_UNICODE = { "ˌ": "\u0621", # hamza-on-the-line
                    #"|": "\u0622", # madda
                    "ˈ": "\u0623", # hamza-on-'alif
                    "ˈ": "\u0624", # hamza-on-waaw
                    #"<": "\u0625", # hamza-under-'alif
                    "ˈ": "\u0626", # hamza-on-yaa'
                    "ʾ": "\u0627", # bare 'alif
                    "b": "\u0628", # baa'
                    "ẗ": "\u0629", # taa' marbuuTa
                    "t": "\u062A", # taa'
                    "ṯ": "\u062B", # thaa'
                    "ǧ": "\u062C", # jiim
                    "ḥ": "\u062D", # Haa'
                    "ẖ": "\u062E", # khaa'
                    "d": "\u062F", # daal
                    "ḏ": "\u0630", # dhaal
                    "r": "\u0631", # raa'
                    "z": "\u0632", # zaay
                    "s": "\u0633", # siin
                    "š": "\u0634", # shiin
                    "ṣ": "\u0635", # Saad
                    "ḍ": "\u0636", # Daad
                    "ṭ": "\u0637", # Taa'
                    "ẓ": "\u0638", # Zaa' (DHaa')
                    "ʿ": "\u0639", # cayn
                    "ġ": "\u063A", # ghayn
                    #"_": "\u0640", # taTwiil
                    "f": "\u0641", # faa'
                    "q": "\u0642", # qaaf
                    "k": "\u0643", # kaaf
                    "l": "\u0644", # laam
                    "m": "\u0645", # miim
                    "n": "\u0646", # nuun
                    "h": "\u0647", # haa'
                    "w": "\u0648", # waaw
                    "ỳ": "\u0649", # 'alif maqSuura
                    "y": "\u064A", # yaa'
                    "á": "\u064B", # fatHatayn
                    "ú": "\u064C", # Dammatayn
                    "í": "\u064D", # kasratayn
                    "a": "\u064E", # fatHa
                    "u": "\u064F", # Damma
                    "i": "\u0650", # kasra
                    #"~": "\u0651", # shaddah
                    "°": "\u0652", # sukuun
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

ARABTEX_TO_UNICODE = { "'": "\u0621", # hamza-on-the-line
                        #"|": "\u0622", # madda
                        "a'": "\u0623", # hamza-on-'alif
                        "U'": "\u0624", # hamza-on-waaw
                       # "<": "\u0625", # hamza-under-'alif
                        "'y": "\u0626", # hamza-on-yaa'
                        "A": "\u0627", # bare 'alif
                        "b": "\u0628", # baa'
                        "T": "\u0629", # taa' marbuuTa
                        "t": "\u062A", # taa'
                        "_t": "\u062B", # thaa'
                        "j": "\u062C", # jiim
                        ".h": "\u062D", # Haa'
                        "x": "\u062E", # khaa'
                        "d": "\u062F", # daal
                        "_d": "\u0630", # dhaal
                        "r": "\u0631", # raa'
                        "z": "\u0632", # zaay
                        "s": "\u0633", # siin
                        "^s": "\u0634", # shiin
                        ".s": "\u0635", # Saad
                        ".d": "\u0636", # Daad
                        ".t": "\u0637", # Taa'
                        ".z": "\u0638", # Zaa' (DHaa')
                        "`": "\u0639", # cayn
                        ".g": "\u063A", # ghayn
                        #"_": "\u0640", # taTwiil
                        "f": "\u0641", # faa'
                        "q": "\u0642", # qaaf
                        "k": "\u0643", # kaaf
                        "l": "\u0644", # laam
                        "m": "\u0645", # miim
                        "n": "\u0646", # nuun
                        "h": "\u0647", # haa'
                        "w": "\u0648", # waaw
                        "I*": "\u0649", # 'alif maqSuura
                        "y": "\u064A", # yaa'
                        "aN": "\u064B", # fatHatayn
                        "uN": "\u064C", # Dammatayn
                        "iN": "\u064D", # kasratayn
                        "a": "\u064E", # fatHa
                        "u": "\u064F", # Damma
                        "i": "\u0650", # kasra
                        "xx": "\u0651", # shaddah
                        #"o": "\u0652", # sukuun
                        #"`": "\u0670", # dagger 'alif
                        #"{": "\u0671", # waSla
                        #extended here
                        #"^": "\u0653", # Maddah
                        #"#": "\u0654", # HamzaAbove

                        #":": "\u06DC", # SmallHighSeen
                        #"@": "\u06DF", # SmallHighRoundedZero
                        #"\"": "\u06E0", # SmallHighUprightRectangularZero
                        #"[": "\u06E2", # SmallHighMeemIsolatedForm
                        #";": "\u06E3", # SmallLowSeen
                        #",": "\u06E5", # SmallWaw
                        #".": "\u06E6", # SmallYa
                        #"!": "\u06E8", # SmallHighNoon
                        #"-": "\u06EA", # EmptyCentreLowStop
                        #"+": "\u06EB", # EmptyCentreHighStop
                        #"%": "\u06EC", # RoundedHighStopWithFilledCentre
                        #"]": "\u06ED"          #
                 }

ROMANIZATION_SYSTEMS_MAPPINGS = { "buckwalter": BUCKWALTER_2_UNICODE,
                                   "iso233-2": ISO2332_TO_UNICODE
                                   #"arabtex": ARABTEX_TO_UNICODE todo: not ready
                                 }

def available_transliterate_systems():
    return list(ROMANIZATION_SYSTEMS_MAPPINGS.keys())

def guess_romaization_system():
    # @todo
    pass

def transliterate(mode, string, ignore = '', reverse = False ):
    # @todo: arabtex Needs individual handling because in some cases uses 2 roman symbols to represent one arabic letter
    """
    encode & decode different  romanization systems
    :param mode:
    :param string:
    :param ignore:
    :param reverse:
    :return:
    """

    if mode in ROMANIZATION_SYSTEMS_MAPPINGS.keys():
        MAPPING = ROMANIZATION_SYSTEMS_MAPPINGS[mode]
    else:
        print(mode+"  not supported! \n")
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