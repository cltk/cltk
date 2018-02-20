from cltk.tokenize.word import WordTokenizer
from cltk.corpus.middle_high_german.alphabet import normalize_middle_high_german
from cltk.stop.middle_high_german.stops import STOPS_LIST as MHG_STOPS
import re

__author__ = ['Eleftheria Chatziargyriou <ele.hatzy@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

"""
The biggest challenge when it comes to noun and adjective stemming is that -similarly to MG- MHG suffixes are based on gender,
which is difficult to determine without either a hard-coded dictionary or an efficient tagger. Statistical analysis could 
theoretically yield more  accurate results, but a lack of online resources make this approach somewhat unreliable.

Another core problem is the fact that unlike English, changes of the stem often occur in the middle of the word rather than the
end (bruoder -> brüeder).

The following algorithm is inspired by Modern German stemmers (namely Snowball), modified to better fit MHG morphological 
structure.

http://snowball.tartarus.org/algorithms/german/stemmer.html
http://www.inf.fu-berlin.de/lehre/WS98/digBib/projekt/_stemming.html
"""

exc_dict = dict() #User-defined exception dictionary, for stemmer.

umlaut_dict={"ë":"e", "ê":"e", "ä":"a", "â":"a", "î":"i", "ö":"o", "ô":"o", "û":"u", "ü":"u"}

def stem_helper(word, rem_umlaut = True):
	"""rem_umlat: Remove umlaut from text"""
	
	#Define R1 and R2 regions
	
	#R1 is defined as the region after the first consonant followed by a vowel
	
	try:
		R1 = list(re.finditer(r"[aëeiouäöüâêîôûæœ][bdghfcjklmnspqrtvwz]",word))[0].start() + 2
	except:
		R1 = len(word)
		
	#R2 is defined as the region within R1 after the first consonant followed by a vowel
	
	try:
		R2 = list(re.finditer(r"[aëeiouäöüâêîôûæœ][bdghfcjklmnspqrtvwz]",word[R1:]))[0].start() + 2 + R1
	except:
		R2 = len(word)
		
	#Make sure the index of R1 is at least 3. 
	
	if R1<3:
		try:
			R1 = list(re.finditer(r"[aëeiouäöüâêîôûæœ][bdghfcjklmnspqrtvwz]",word[1:]))[0].start() + 2
		except:
			R1 = len(word)
	
	if rem_umlaut:
		word = remove_umlaut(word)
	
	word = word[:R1] + re.sub(r'(wes|wen|est|ern|em|en|er|es|eȥ(?=[klmrt])s|(?=[lr])n|e)$',"",word[R1:])
	word = word[:R1] + re.sub(r'(est|er|en|re|in|iu|(?=.{3})st,word[R1:])$',"",word[R1:])
	word = word[:R2] + re.sub(r'(lich?.?.|keit|inc|isch?.?.)$',"",word[R2:])
	
	return word


def remove_umlaut(text):
	return "".join([umlaut_dict.get(l,l) for word in text for l in word])

	
def stemmer_middle_high_german(text_l, rem_umlauts = True, exceptions = exc_dict):
	"""text_l: text in string format
	   rem_umlauts: choose whether to remove umlauts from string
	   exceptions: hard-coded dictionary for the cases the algorithm fails"""
	
	#Normalize text
	text_l = normalize_middle_high_german(text_l, to_lower_all = False, to_lower_beginning = True)
	
	#Tokenize text
	word_tokenizer = WordTokenizer("middle_high_german")
	text_l = word_tokenizer.tokenize(text_l)
	text = []

	
	for word in text_l:
		try:
			text.append(exceptions[word]) #test if word in exception dictionary
			
		except:
			if word[0].isupper():
				#MHG only uses upper case for locations, people, etc. So any word that starts with a capital
				#letter while not being at the start of a sentence will automatically be excluded.
				text.append(word)
				
			elif word in MHG_STOPS: 
				text.append(word) #Filter stop words
				
			else:
				text.append(stem_helper(word, rem_umlaut = rem_umlauts))
	return text
