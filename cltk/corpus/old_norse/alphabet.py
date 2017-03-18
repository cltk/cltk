#all the alphabets in old norse
ALPHABET = ['a','b','c','d','ð','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','þ','æ','ǫ','ø','œ']

#All the vowels in old norse
VOWELS = ['a', 'á', 'e', 'é', 'i', 'í', 'o', 'ó', 'u', 'ú', 'y', 'ý', 'æ','ǫ́', 'ǫ', 'ø', 'œ']

#All the consonants in old norse
CONSONANTS = ["b", "c", "d", "ð", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z", "þ"]

#All the Dipthongs in old norse
DIPTHONGS = ["au","ei","ey"]

#Similar to other Germanic languages, the vowel change, or umlaut, operates in Old Norse. There are two kinds: i-umlaut, and u-umlaut.
#I-umlaut caused vowels to become fronted, and in that way, drawn towards the ‘i’.
#The i-umlaut appears thus:
UMLAUT_I = {"a": "e", "á": "æ", "o": "ø", "ó": "œ", "u": "y", "ú": "ý"}
#examples of i-umluat:
#hafa > hef
#blása > blæs

#In certain circumstances, the presence of a 'u' in the endings of adjectives or nouns causes what is called 'u-umlaut' or 'back mutation' to the stem vowel. This is how that change presents itself:
UMLAUT_U = {"a": "ǫ", "á": "ǫ́", "e": "ø", "é": "œ", "i": "y", "í": "ý", "a": "u"}
#example of u-umlaut:
#saku>sǫk  
