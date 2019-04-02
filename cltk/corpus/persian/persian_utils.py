import re
import cltk.corpus.persian.alphabet as alphabet
from cltk.corpus.arabic.alphabet import *

to_reform = [
    {
        "characters": [
            HAMZA,
            HAMZA_BELOW,
            HAMZA_ABOVE,
            HAMZA_ISOLATED,

            MINI_ALEF,
            SMALL_ALEF,
            SMALL_WAW,
            SMALL_YEH,

            KASHEEDA,
            FATHATAN,
            DAMMATAN,
            KASRATAN,
            FATHA,
            DAMMA,
            KASRA,
            SHADDA,
            SUKUN,
            alphabet.THOUSANDS,
            alphabet.DECIMAL
        ],
        "to_be": ""
    },
    {
        "characters": [
            ALEF_MADDA,
            ALEF_WASLA,
            HAMZA_BELOW_ALEF,
            HAMZA_ABOVE_ALEF,
        ],
        "to_be": alphabet.ALEF
    },
    {
        "characters": [
            ALEF_MAKSURA,
            YEH,
        ],
        "to_be": alphabet.YE
    },
    {
        "characters": [KAF],
        "to_be": alphabet.KAF
    },
    {
        "characters": [
            LAM_ALEF,
            LAM_ALEF_HAMZA_ABOVE,
            LAM_ALEF_HAMZA_BELOW,
            LAM_ALEF_MADDA_ABOVE,
        ],
        "to_be": alphabet.LAM + alphabet.ALEF
    },
    {
        "characters": [TEH_MARBUTA],
        "to_be": alphabet.HE2
    },
]

replacementDict = {}
for rule in toReform:
    for character in rule["characters"]:
        replacementDict[character] = rule["to_be"]

for originalForm, shapedForms in SHAPED_FORMS.items():
    for form in shapedForms:
        replacementDict[form] = replacementDict.get(originalForm, originalForm)

for i in range(10):
    replacementDict[EASTERN_ARABIC_NUMERALS[i]] = alphabet.NUMERALS[i]
    replacementDict[WESTERN_ARABIC_NUMERALS[i]] = alphabet.NUMERALS[i]
    # Use the commented parts for Word2Vec embeddings
    # replacementDict[alphabet.NUMERALS[i]] = " %s " % alphabet.NUMERALS_WRITINGS[i]


# for char in '[!"#%\'()*+,-./:;<=>?@\[\]^_`{|}~’”“′‘\\\]؟؛«»،٪':
#     replacementDict[char] = " "
#
# replacementDict[" +"] = " "

replacementRegex = re.compile("(%s)" % "|".join(map(re.escape, replacementDict.keys())))

def standardize(text):
    return replacementRegex.sub(lambda mo: replacementDict[mo.string[mo.start():mo.end()]], text)
