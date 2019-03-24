'''
A module for representing the orthophonology of a language: 
the mapping from orthographic representations to IPA symbols.

Based on many ideas in cltk.phonology.utils by Clément Besnier <clemsciences@gmail.com>.
'''

from enum import IntEnum, auto
from copy import deepcopy
from functools import reduce
import re

__author__ = ["John Stewart <johnstewart@aya.yale.edu>"]

# ------------------- Phonological Features -------------------

# The list of features and their values are from the IPA charts.
# Features for non-pulmonic consonants (e.g. clicks, implosives) are not yet provided.

class PhonologicalFeature(IntEnum):
	def __sub__(self, other):
		return phoneme(self) - other

	def __rshift__(self, other):
		return phoneme(self) >> other

	def __le__(self, other):
		return phoneme(self) <= other

	def __ge__(self, other):
		return phoneme(self) >= other

	def matches(self, other):
		return phoneme(self).matches(other)

class Consonantal(PhonologicalFeature):
	neg = auto()
	pos = auto()

class Voiced(PhonologicalFeature):
	neg = auto()
	pos = auto()

class Aspirated(PhonologicalFeature):
	neg = auto()
	pos = auto()

class Geminate(PhonologicalFeature):
	neg = auto()
	pos = auto()

class Roundedness(PhonologicalFeature):
	neg = auto()
	pos = auto()

class Length(PhonologicalFeature):
    short = auto()
    long = auto()
    overlong = auto()

# order for Height, Backness, and Manner is important
# the feature values must be ordered by *increasing sonority*
class Height(PhonologicalFeature):
    close = auto()
    near_close = auto()
    close_mid = auto()
    mid = auto()
    open_mid = auto()
    near_open = auto()
    open = auto()

class Backness(PhonologicalFeature):
    front = auto()
    central = auto()
    back = auto()

class Manner(PhonologicalFeature):
	stop = auto()
	fricative = auto()
	affricate = auto()
	nasal = auto()
	lateral = auto()
	trill = auto()
	spirant = auto()
	approximant = auto()

class Place(PhonologicalFeature):
    bilabial = auto()
    labio_dental = auto()
    dental = auto()
    alveolar = auto()
    post_alveolar = auto()
    retroflex = auto()
    palatal = auto()
    velar = auto()
    uvular = auto()
    glottal = auto()


# ------------------- Phonemes -------------------

class AbstractPhoneme:
	'''
	An abstract phoneme is just a bundle of phonological features.
	'''

	def __init__(self, features = {}, ipa = None):
		# ensure unique features
		if len(set(features.keys())) != len(features.keys()):
			raise ValueError('non-unique features')

		# ensure feature values correctly match their types
		# this is a barbaric bit of type checking that the language should provide
		for feature_name, feature_value in features.items():
			if not issubclass(feature_name, PhonologicalFeature):
				raise TypeError(str(feature_name) + ' is not a phonological feature')
			if type(feature_value) != feature_name:
				raise TypeError(str(feature_value) + ' is not a ' + str(feature_name))

		self.features = features
		self.ipa = ipa

	def is_vowel(self):
		return self[Consonantal] == Consonantal.neg

	def _check_disjunctive_features(self, feature_values):
		return reduce(lambda a, b: a or b, [self[type(f)] == f for f in feature_values])

	def merge(self, other):
		phoneme = deepcopy(self)

		# special case for list of phonemes
		if type(other) == list and len(other) > 0 and issubclass(type(other[0]), AbstractPhoneme):
			return other

		if issubclass(type(other), AbstractPhoneme):
			feature_values = other.features.values()
		elif type(other) != list and type(other) != tuple:
			feature_values = [other]
		else:
			feature_values = other

		for f in feature_values:
			if type(f) == list:
				for inner_f in f:
					phoneme[type(inner_f)] = inner_f
			elif issubclass(type(f), AbstractPhoneme):
				phoneme = phoneme << f
			else:
				phoneme[type(f)] = f

		if issubclass(type(other), AbstractPhoneme) and other.ipa is not None:
			phoneme.ipa = other.ipa

		return phoneme

	def is_equal(self, other):
		return self.features == other.features

	def matches(self, other):
		if other is None:
			return False
		if type(other) == list or issubclass(type(other), PhonologicalFeature):
			other = phoneme(other)
		return other.features.items() >= self.features.items()

	def __getitem__(self, feature_name):
		'''
		Use dict-type syntax for accessing the values of features.
		'''
		if not issubclass(feature_name, PhonologicalFeature):
			raise TypeError(str(feature_name) + ' is not a phonological feature')
		return self.features.get(feature_name, None)

	def __setitem__(self, feature_name, feature_value):
		if not issubclass(feature_name, PhonologicalFeature):
			raise TypeError(str(feature_name) + ' is not a phonological feature')
		if type(feature_value) != feature_name:
			raise TypeError(str(feature_value) + ' is not a ' + str(feature_name))
		self.features[feature_name] = feature_value
		return self

	def __str__(self):
		return  ('IPA:{0} '.format(self.ipa) if self.ipa is not None else '') + \
		' '.join([str(v) for v in self.features.values()])

	__repr__ = __str__

	def __eq__(self, other):
		return self.is_equal(other)

	def __le__ (self, other):
		return self.matches(other)

	def __ge__ (self, other):
		return other.matches(self)

	def __lt__ (self, other):
		return other.is_more_sonorous(self)

	def __gt__ (self, other):
		return self.is_more_sonorous(other)

	def __rshift__(self, other):
		return PhonologicalRule(
			condition = lambda _, target, __: self <= target,
			action = lambda target : target << other)

	def __lshift__(self, other):
		return self.merge(other)

	def __sub__(self, other):
		other = phoneme(other) if not issubclass(type(other), AbstractPhoneme) else other
		env_start = PositionedPhoneme(self, env_start = True)
		env_end = PositionedPhoneme(self, env_end = True)
		return lambda before, _, after : env_start <= before and env_end <= after

def phoneme(*feature_values):
	phoneme = AbstractPhoneme({})
	phoneme = phoneme << feature_values
	return phoneme

def PositionedPhoneme(phoneme, 
	word_initial = False, word_final = False, 
	syllable_initial = False, syllable_final = False,
	env_start = False, env_end = False):
	
	pos_phoneme = deepcopy(phoneme)
	pos_phoneme.word_initial = word_initial
	pos_phoneme.word_final = word_final
	pos_phoneme.syllable_initial = syllable_initial
	pos_phoneme.syllable_final = syllable_final
	pos_phoneme.env_start = env_start
	pos_phoneme.env_end = env_end

	return pos_phoneme

class AlwaysMatchingPseudoPhoneme(AbstractPhoneme):
	def matches(self, other):
		return True

class WordBoundaryPseudoPhoneme(AbstractPhoneme):
	def __init__(self):
		AbstractPhoneme.__init__(self, ipa = '#')

	def matches(self, other):
		return other is None
	
	def is_equal(self, other):
		return self is other

class SyllableBoundaryPseudoPhoneme(AbstractPhoneme):
	def __init__(self):
		AbstractPhoneme.__init__(self, ipa = '$')

	def matches(self, other):
		if other is None:
			return True
		elif getattr(self, 'env_start', False) and getattr(other, 'syllable_final', False):
			return True
		elif getattr(self, 'env_end', False) and getattr(other, 'syllable_initial', False):
			return True
		else:
			return False


ANY = AlwaysMatchingPseudoPhoneme()
W = WordBoundaryPseudoPhoneme()
S = SyllableBoundaryPseudoPhoneme()


class Consonant(AbstractPhoneme):
	'''
	Based on cltk.phonology.utils by @clemsciences.
	A consonant is a phoneme that is specified for the features listed in the IPA chart for consonants:
	Place, Manner, Voicing.  These may be read directly off the IPA chart, which also gives the IPA symbol.
	The Consonantal feature is set to positive, and the aspirated is defaulted to negative.
	See http://www.ipachart.com/
	'''

	def __init__(self, place, manner, voiced, ipa, geminate = Geminate.neg, aspirated = Aspirated.neg):
		assert place is not None
		assert manner is not None
		assert voiced is not None
		assert geminate is not None
		assert ipa is not None

		AbstractPhoneme.__init__(self, {
			Consonantal : Consonantal.pos,
			Place       : place,
			Manner      : manner,
			Voiced      : voiced,
			Aspirated   : aspirated,
			Geminate    : geminate}, 
			ipa)

	def is_more_sonorous(self, other):
		'''
		compare this phoneme to another for sonority.
		Used for SSP considerations.
		'''
		return True if isinstance(other, Consonant) and self[Manner] > other[Manner] else False


class Vowel(AbstractPhoneme):
	'''
	The representation of a vowel by its features, as given in the IPA chart for vowels.
	See http://www.ipachart.com/
	'''

	def __init__(self, height, backness, rounded, length, ipa):
		assert height is not None
		assert backness is not None
		assert rounded is not None
		assert length is not None
		assert ipa is not None

		AbstractPhoneme.__init__(self, {
			Consonantal : Consonantal.neg,
			Height      : height, 
			Backness    : backness, 
			Roundedness : rounded, 
			Length      : length},
			ipa)

	def __add__(self, other):
		'''
		Summed vowels produce diphthongs, returning a copy of the first vowel
		and the concatenation of the IPA symbols.
		A hack because the features of the second vowel are lost.
		'''
		diphthong = deepcopy(self)
		diphthong.ipa += other.ipa
		return diphthong

	def lengthen(self):
		'''
		Returns a new Vowel with its Length lengthened, 
		and ":" appended to its IPA symbol.
		'''
		vowel = deepcopy(self)

		if vowel[Length] == Length.short:
			vowel[Length] = Length.long
		elif vowel[Length] == Length.long:
			vowel[Length] = Length.overlong

		vowel.ipa += ':'
		return vowel

	def is_more_sonorous(self, other):
		'''
		compare this phoneme to another for sonority.
		Used for SSP considerations.
		'''
		if isinstance(other, Consonant):
			return True
		elif self[Height] > other[Height]:
			return True
		elif self[Height] == other[Height]:
			return self[Backness] > other[Backness]
		else:
			return False


# ------------------- Phonological Rule Templates -------------------

def _wrapped_print(x):
	print(x)
	return True

class BasePhonologicalRule:
	'''
	Base class for conditional phonological rules.
	A phonological rule relates an item (a phoneme) to its environment to define a transformation.
	Specifically, a rule specifies a condition and an action.

	* The condition characterizes the phonological environment of a phoneme in terms of the 
	characteristics of the phomeme before it (if any), and after it (if any).
	In general it is a function taking three arguments: before, target, after, the phonemes in the environment,
	an returning a boolean for whether the rule should fire.

	* The action defines a transformation of the target phoneme, e.g. its vocalization.
	It is a function taking only the action, which returns the replacement phoneme OR a *list* of phonemes.
	'''
	def __init__(self, condition, action):
		self.condition = condition
		self.action = action

	def perform_action(self, phonemes, pos):
		return self.action(phonemes[pos])

	def __call__(self, phonemes, pos):
		return self.perform_action(phonemes, pos)

	def __or__(self, other_condition):
		prev_function = self.condition
		self.condition = lambda before, target, after: prev_function(before, target, after) and \
		other_condition(before, target, after)
		return self

def is_syllable_initial(phonemes, pos):
	if pos == len(phonemes) - 1:
		return False
	return pos == 0 or \
	(phonemes[pos - 1].is_more_sonorous(phonemes[pos]) and not phonemes[pos].is_more_sonorous(phonemes[pos + 1]))

def is_syllable_final(phonemes, pos):
	if pos == 0:
		return False
	return pos == len(phonemes) -1  or \
	(phonemes[pos + 1].is_more_sonorous(phonemes[pos]) and not phonemes[pos].is_more_sonorous(phonemes[pos - 1]))


class PhonologicalRule(BasePhonologicalRule):
	'''
	The most general phonological rule can apply anywhere in the word.
	before and after phonemes may therefore be null when calling the condition.
	'''
	def check_environment(self, phonemes, pos):
		if pos >= len(phonemes):
			return False

		before = None if pos == 0 else phonemes[pos - 1]
		after = None if pos == len(phonemes) - 1 else phonemes[pos + 1]
		return self.condition(before, phonemes[pos], after)

class WordInitialPhonologicalRule(BasePhonologicalRule):
	'''
	A rule applying to the first phoneme in the word.
	The condition only takes two arguments: target and after.
	'''
	def check_environment(self, phonemes, pos):
	    return self.condition(phonemes[0], phonemes[1]) if pos == 0 and len(phonemes) > 1 else False

	def perform_action(self, phonemes, _):
	    return self.action(phonemes[0])

class WordFinalPhonologicalRule(BasePhonologicalRule):
	'''
	A rule applying to the last phoneme in the word.
	The condition only takes two arguments: before and target.
	'''
	def check_environment(self, phonemes, pos):
	    last = len(phonemes) - 1
	    return self.condition(phonemes[last - 1], phonemes[last]) if pos == last and len(phonemes) > 1 else False

	def perform_action(self, phonemes, _):
	    return self.action(phonemes[len(phonemes) - 1])

class InnerPhonologicalRule(BasePhonologicalRule):
	'''
	A rule applying to a position inside a word.
	The before and after arguments to the condition will always be actual phonemes (not None).
	'''
	def check_environment(self, phonemes, pos):
		if pos == 0 or pos == len(phonemes) - 1:
			return False
		return self.condition(phonemes[pos - 1], phonemes[pos], phonemes[pos + 1])

class SyllableInitialPhonologicalRule(BasePhonologicalRule):
	'''
	A rule applying to the first phoneme in a syllable.
	Syllable breaks are determined by a simple, language-independent SSP heuristic.
	The condition only takes two arguments: target and after.
	'''
	def check_environment(self, phonemes, pos):
		if pos == 0 and len(phonemes) > 0:
			return self.condition(phonemes[pos], phonemes[1]) 
		elif pos == len(phonemes) - 1:
			return False
		# apply simple SSP heuristic to determine if we're at a syllable start
		elif phonemes[pos - 1].is_more_sonorous(phonemes[pos]) and not phonemes[pos].is_more_sonorous(phonemes[pos + 1]):
			return self.condition(phonemes[pos], phonemes[pos + 1]) 
		else:
			return False


def SimplePhonologicalRule(target, replacement, before=None, after=None):
	'''
	Systactic sugar for simple item-specific rules.
	* target and replacement are phonemes.
	* before and after, optionally specified, are disjunctive lists of *phonological features*.
	That is, the rule will fire if ANY of the features listed in e.g. before is present in the preceding phoneme.
	If neither before nor after are specified, then the rule is UNconditional.  Useful for elsewhere conditions.
	''' 
	if before is not None and after is None:
		cond = lambda b, t, _: t in target and b is not None and b & before
	if before is not None and after is not None:
		cond = lambda b, t, a: t in target and b is not None and b & before and a is not None and a & after
	if before is None and after is not None:
		cond = lambda _, t, a: t in target and a is not None and a & after
	if before is None and after is None:
		cond = lambda _, t, __: t in target

	return PhonologicalRule(cond, lambda _ : replacement if _wrapped_print(replacement) else replacement)


# ------------------- The ortho-phonology of a language -------------------#

class Orthophonology:
	'''
	The ortho-phonology of a language is described by:
	* The inventory of all the phonemes of the language.
	* A mapping of orthographic symbols to phonemes.
	* mappings of orthographic symbols pairs to:
	    * diphthongs
	    * phonemes (i.e. digraphs)
	* phonological rules for the contexutal transformation of phonological representations.

	The class is very clearly aimed at alphabetic orthographies.  
	Its usefulness for e.g. pictographic orthographies is questionable.
	'''
	def __init__(self, sound_inventory, alphabet, diphthongs, digraphs):
		self.sound_inventory = sound_inventory
		self.alphabet = alphabet
		self.diphthongs = diphthongs
		self.digraphs = digraphs
		self.di = {**self.diphthongs, **self.digraphs}
		self.rules = []

	def add_rule(self, rule):
		'''
		Adds a rule to the orthophonology.
		The *order* in which rules are added is critcial, since the first rule that matches fires.'''
		self.rules.append(rule)

	@staticmethod
	def _tokenize(text):
		text = text.lower()
		text = re.sub(r"[.\";,:\[\]()!&?‘]", "", text)
		return text.split(' ')

	def transcribe_word(self, word):
		'''
		The heart of the transcription process.
		Similar to the system in in cltk.phonology.utils, the algorithm:
		1) Applies digraphs and diphthongs to the text of the word.
		2) Carries out a naive ("greedy", per @clemsciences) substitution of letters to phonemes,
		according to the alphabet.
		3) Applies the conditions of the rules to the environment of each phoneme in turn.
		The first rule matched fires.  There is no restart and later rules are not tested.
		Also, if a rule returns multiple phonemes, these are never re-tested by the rule set.
		'''
		phonemes = []

		i = 0
		while i < len(word):
			# check for digraphs and dipththongs
			if i < len(word) - 1 and word[i:i + 2] in self.di:
				letter_pair = word[i:i + 2]
				replacement = self.di[letter_pair]
				phonemes.append(replacement)
				i += 2
			else:
				phonemes.append(self[word[i]])
				i += 1

		# mark syllable boundaries, and, in future, other positional features
		for i in range(len(phonemes)):
			phonemes[i] = PositionedPhoneme(phonemes[i])
			phonemes[i].is_syllable_initial = is_syllable_initial(phonemes, i)
			phonemes[i].is_syllable_final = is_syllable_final(phonemes, i)

		# apply phonological rules.  Note: no restart!
		i = 0
		while i < len(phonemes):
		    for rule in self.rules:
		    	if rule.check_environment(phonemes, i):
		    		replacement = rule(phonemes, i)
		    		replacement = [replacement] if not isinstance(replacement, list) else replacement
		    		replacement = [self._find_sound(p) for p in replacement]
		    		phonemes[i:i + 1] = replacement
		    		i += len(replacement) - 1
		    		break
		    i += 1
		    		
		return phonemes

	def transcribe(self, text, as_phonemes = False):
		'''
		Trascribes a text, which is first tokenized for words, then each word is transcribed.
		If as_phonemes is true, returns a list of list of phoneme objects,
		else returns a string concatenation of the IPA symbols of the phonemes.
		'''
		phoneme_words = [self.transcribe_word(word) for word in self._tokenize(text)]
		if not as_phonemes:
			words = [''.join([phoneme.ipa for phoneme in word]) for word in phoneme_words]
			return ' '.join(words)
		else:
			return phoneme_words

	def _find_sound(self, phoneme) :
		for sound in self.sound_inventory:
			if sound.is_equal(phoneme):
				return sound
		return None

	def voice(self, consonant) :
		'''
		Voices a consonant, by searching the sound inventory for a consonant having the same
		features as the argument, but +voice.
		'''
		voiced_consonant = deepcopy(consonant)
		voiced_consonant[Voiced] = Voiced.pos
		return self._find_sound(voiced_consonant)

	def aspirate(self, consonant) :
		'''
		Aspirates a consonant, by searching the sound inventory for a consonant having the same
		features as the argument, but +aspirated.
		'''
		aspirated_consonant = deepcopy(consonant)
		aspirated_consonant[Aspirated] = Aspirated.pos
		return self._find_sound(aspirated_consonant)

	@staticmethod
	def lengthen(vowel):
		'''
		Returns a lengthened copy of the vowel argument.
		'''
		return vowel.lengthen()

	def __call__(self, text, as_phonemes = False):
		'''
		syntactic sugar for call the transcribe method
		'''
		return self.transcribe(text, as_phonemes)

	def __getitem__(self, letter):
		'''
		Returns the phoneme associated with a letter, or None.
		'''
		return self.alphabet.get(letter, None)

	def __lshift__(self, rule):
		'''
		Syntactic sugar for adding a rule
		'''
		self.add_rule(rule)
