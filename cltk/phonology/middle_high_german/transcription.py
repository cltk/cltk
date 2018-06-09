"""Note: there are no definite MHG  phonological rules, so this module serves as an approximate reconstruction of the original. As of this version, the Transcribe class doesn't support any specific dialects and serves as a superset encompassing various regional accents. 
 
 To-do: add stress, syllabify module, CV tier
 
 Sources:
 * https://www.germanistik.uni-bonn.de/institut/abteilungen/germanistische-mediavistik/studium/leitfaeden-reader-links/b1-reader-oktober-2009-endversion.pdf
* [A Middle High German Primer - Joseph Wright](http://www.minnesang.com/Themen/Ulrich%20Mueller%20zur%20Aussprache.pdf)
"""

import re
import unicodedata
from cltk.stem.middle_high_german.stem import remove_umlaut

#IPA Dictionary
Dipthongs_IPA = {
	"ei": "ɛ͡ɪ", #Dipthongs
	"ie": "i͡ə",
	"üe": "y͡ə",
	"uo": "u͡ə",
	"iu": "yː",
	"öu": "ø͡u",
	"ou": "ɔ͡ʊ",
	"ch": "χ",
	"qu": "k",
	"tt": "t·t",
	"bb": "b·b",
	"gg": "g·g",
	"pp": "p·p",
	"tt": "t·t",
	"ck": "k·k",  #c and k indicate the same sound and while c was most oftenly used at the beginning of a word, k was usually used at the end of a syllable
	"ff": "f·f",
	"ss": "s·s",
	"mm": "m·m",
	"nn": "n·n",
	"ll": "l·l",
	"rr": "r·r"
}

IPA = {
	"a": "a",  #Short vowels
	"ä": "æ",
	"e": "e",
	"ë": "e",
	"i": "ɪ",
	"o": "ɒ",
	"ö": "ọ̈",
	"u": "ʊ",
	"ü": "ʏ",
	"â": "ɑː", #Long vowels
	"æ": "ɛ",
	"œ": "iu",
	"ê": "eː",
	"î": "iː",
	"ô": "oː",
	"û": "uː",
	"k": "k", #Consonants
	"l": "l",
	"m": "m",
	"n": "n",
	"p": "p",
	"t": "t",
	"w": "w",
	"b": "b̥",  #Ιn MHG. the consonants b, d, g were not voiced explosives like English b, d, g, but were voiceless lenes,
	"d": "d̥",  # and only differed from the fortes p, t, k in being produced with less intensity or force 
	"g": "ɡ̊",  # - A Middle High German Primer, Joseph Wright
	"c": "k",
	"f": "f",  # Only accounts for labiodental form of latter HG
	"v": "f",
	"j": "j",
	"r": "r", # Alveolar trilled r in all positions
	"w": "w",
	"z": "t͡s",
	"ȥ": "t͡s"
}

#Soundex Dictionary
dict_dipth_SE = {
	"ng":"2",
	"ch":"2",
	"pf":"4",
	"ts":"4",
}

dict_SE = {
	"f":"1",
	"b":"1",
	"p":"1",
	"v":"1",
	"w":"1",
	"m":"2",
	"n":"2",
	"t":"3",
	"d":"3",
	"r":"3",
	"l":"3",
	"k":"3",
	"c":"3",
	"g":"3",
	"s":"3",
	"z":"4",
	"ȥ":"4",
	"s":"4",
	"r":"5",
	"l":"5",
	"j":"6"
}
	
class Transcriber:
	
	def __init__(self):
		pass #To-do: Add different dialects and/or notations
				
	def transcribe(self, text, punctuation = True):
		"""Accepts a word and returns a string of an approximate pronounciation (IPA)"""
		
		if not punctuation:
			text = re.sub(r"[\.\";\,\:\[\]\(\)!&?‘]","",text)
		
		text = re.sub(r'sch','ʃ',text)
		text = re.sub(r'(?<=[aeiouäëöüâæœêîôû])h','χ',text) 
		text = re.sub(r'h(?=[aeiouäëöüâæœêîôû])','χ',text)
		text = re.sub(r'(?<=[aeiouäëöüâæœêîôû])s(?=[aeiouäëöüâæœêîôû])','z̥',text)
		text = re.sub(r'^s(?=[aeiouäëöüâæœêîôû])','z̥',text)
		
		for w,val in zip(Dipthongs_IPA.keys(), Dipthongs_IPA.values()):
			text = text.replace(w, val)
			
		for w,val in zip(IPA.keys(), IPA.values()):
			text = text.replace(w, val)
			
		return "[" + text + "]"

"""
Soundex variant was based on the original American Soundex  developed by Russel and King, altered to better fit Middle High 
German morphology. The replacement rules were based on matching places and manners of articulation between the two languages 
(AE and MHG).

Algorithm:

-N ormalize word and convert the first letter to uppercase
-Remove other vowels 

Replacement Rules:
- f,v,b,p,w -> 1 Labiodental fricatives [f,v] and bilabial plosives [p,b], approximant [w]
- m,n,ng -> 2 Nasals
- t,d,r,l,k,c,g,ch,s -> 3 [non-nasal velars/alveolars]
- pf, ts, z, s -> 4  Affricates and alveolar fricatives
- r,l -> 5 Liquids
- j -> 6 Palatal Approximant

-Remove double numbers
-Remove remaining letters
-Retain first 3 numbers (add 0 if less than 3)
"""

class Word:

	def __init__(self, word):
		self.word = word
	
	def phonetic_indexing(self, p = "SE"):
		"""Specifies the phonetic indexing method.
		SE: Soundex variant for MHG"""
		
		if p == "SE":
			return self._Soundex()
		else:
			print("Parameter value not supported")
		
	def _Soundex(self):
		t_word = remove_umlaut(self.word[0].lower()).upper() + remove_umlaut(self.word[1:]).lower()
		
		for w,val in zip(dict_dipth_SE.keys(), dict_dipth_SE.values()):
			t_word = t_word.replace(w,val)
		
		for w,val in zip(dict_SE.keys(), dict_SE.values()):
			t_word = t_word.replace(w,val)
			
		#Remove adjacent duplicate numbers
		t_word = re.sub(r"(\d)\1+",r"\1" ,t_word)
		
		#Strip remaining letters
		t_word = re.sub(r"[a-zæœ]+","",t_word)
		
		return (t_word + "0"*3) [:4] #Add trailing zeroes
	
	def ASCII_encoding(self):
		"""Returns the ASCII encoding of a string"""
		
		w = unicodedata.normalize('NFKD', self.word).encode('ASCII','ignore') #Encode into ASCII, returns a bytestring
		w = w.decode('utf-8') #Convert back to string
		
		return w
