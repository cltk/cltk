"""Sources: Schreibkonventionen des klassischen Mittelhochdeutschen - Ad fontes Simone Berchtold, Deutsches Seminar
            https://de.wikipedia.org/wiki/Mittelhochdeutsch"""

#Alphabet of Middle High German

# c is used at the beginning of only loanwords and is pronounced the same as k (e.g. calant, cappitain)

# Double consonants are pronounced the same way as their corresponding letters in Modern Standard German (e.g. pp/p)

# schl, schm, schn, schw are written in MHG as sw, sl, sm, sn

ALPHABET = ["a", "ë", "e", "i", "o", "u", "ä", "ö", "ü", "â", "ê", "î", "ô", "û", "æ", "œ", "iu", "b", "d", "g", "h", "f", "c", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "z","ȥ"]

# The consonants of Middle High German are categorized as:
# Stops: ⟨p t k/c/q b d g⟩
# Affricates: ⟨pf/ph tz/z⟩ 
# Fricatives: ⟨v f s ȥ sch ch h⟩
# Nasals: ⟨m n⟩
# Liquids: ⟨l r⟩
# Semivowels: ⟨w j⟩

CONSONANTS = ["b", "d", "g", "h", "f", "c", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "z"]

VOWELS = ["a", "ë", "e", "i", "o", "u", "ä", "ö", "ü", "â", "ê", "î", "ô", "û", "æ", "œ", "iu"]

SHORT_VOWELS = ["a", "ë", "e", "i", "o", "u", "ä", "ö", "ü"]

# æ (also seen as ae), œ (also seen as oe) and iu denote the use of Umlaut over â, ô and û respectively

LONG_VOWELS = ["â", "ê", "î", "ô", "û", "æ", "œ", "iu"]

DIPTHONGS = ["ei", "ie", "ou", "öu", "uo", "üe"]

# ȥ or ʒ is used in modern handbooks and grammars to indicate the s or s-like sound which arose from Germanic t in the High German consonant shift. 

import re

def normalize_middle_high_german(text, to_lower_all = True, to_lower_beginning = False, alpha_conv = True, punct = True):
    """
       to_lower_all: convert whole text to lowercase
       alpha_conv: convert alphabet to canonical form
       punct: remove punctuation
    """
 
    if to_lower_all:
        text = text.lower()
   
    if to_lower_beginning:
        text = text[0].lower() + text[1:]
        text = re.sub(r"(?<=[\.\?\!]\s)(\w)",lambda x: x.group(1).lower(),text)

    if alpha_conv:
        text = text.replace("ē","ê").replace("ī","î").replace("ā","â").replace("ō","ô").replace("ū","û")
        text = text.replace("ae","æ").replace("oe","œ")

    if punct:
        text = re.sub(r"[\.\";\,\:\[\]\(\)!&?‘]","",text)
    
    return text
