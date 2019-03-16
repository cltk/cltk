from enum import IntEnum, auto
from copy import deepcopy
from functools import reduce
import re

__author__ = ["John Stewart <johnstewart@aya.yale.edu>"]

# ------------------- Phonological Features -------------------

class PhonologicalFeature(IntEnum):
	pass

class Consonantal(PhonologicalFeature):
	neg = auto()
	pos = auto()

class Voiced(PhonologicalFeature):
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
	def __init__(self, features, ipa = None):
		# ensure unique features
		if len(set(features.keys())) != len(features.keys()):
			raise ValueError('non-unique features')

		# ensure feature values correctly match their types
		for feature_name, feature_value in features.items():
			if not issubclass(feature_name, PhonologicalFeature):
				raise TypeError(str(feature_name) + ' is not a phonological feature')
			if type(feature_value) != feature_name:
				raise TypeError(str(feature_value) + ' is not a ' + str(feature_name))

		self.features = features
		self.ipa = ipa

	def __getitem__(self, feature_name):
		if not issubclass(feature_name, PhonologicalFeature):
			raise TypeError(str(feature_name) + ' is not a phonological feature')
		return self.features[feature_name]

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

	def is_equal(self, other):
		return self.features == other.features

	def __eq__(self, other):
		return self.is_equal(other)


class Consonant(AbstractPhoneme):
	def __init__(self, place, manner, voiced, ipa, geminate = Geminate.neg):
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
			Geminate    : geminate}, 
			ipa)

	def is_more_sonorous(self, other):
		return True if isinstance(other, Consonant) and self[Manner] > other[Manner] else False


class Vowel(AbstractPhoneme):
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

	# for diphthongs
	def __add__(self, other):
		diphthong = deepcopy(self)
		diphthong.ipa += other.ipa
		return diphthong

	def lengthen(self):
		vowel = deepcopy(self)

		if vowel[Length] == Length.short:
			vowel[Length] = Length.long
		elif vowel[Length] == Length.long:
			vowel[Length] = Length.overlong

		vowel.ipa += ':'
		return vowel

	def is_more_sonorous(self, other):
		if isinstance(other, Consonant):
			return True
		elif self[Height] > other[Height]:
			return True
		elif self[Height] == other[Height]:
			return self[Backness] > other[Backness]
		else:
			return False


# ------------------- Phonological Rule Templates -------------------

class BasePhonologicalRule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def perform_action(self, phonemes, pos):
        return self.action(phonemes[pos])

    def __call__(self, phonemes, pos):
        return self.perform_action(phonemes, pos)

class PhonologicalRule(BasePhonologicalRule):
    def check_environment(self, phonemes, pos):
        before = phonemes[pos - 1] if pos > 0 else None
        after  = phonemes[pos + 1] if pos < len(phonemes) - 1 else None
        return self.condition(before, phonemes[pos], after)

class WordInitialPhonologicalRule(BasePhonologicalRule):
    def check_environment(self, phonemes, pos):
        return self.condition(phonemes[0], phonemes[1]) if pos == 0 and len(phonemes) > 1 else False

    def perform_action(self, phonemes, _):
        return self.action(phonemes[0])

class WordFinalPhonologicalRule(BasePhonologicalRule):
    def check_environment(self, phonemes, pos):
        last = len(phonemes) - 1
        return self.condition(phonemes[last - 1], phonemes[last]) if pos == last and len(phonemes) > 1 else False

    def perform_action(self, phonemes, _):
        return self.action(phonemes[len(phonemes) - 2])

class InnerPhonologicalRule(BasePhonologicalRule):
	def check_environment(self, phonemes, pos):
		if pos == 0 or pos == len(phonemes) - 1:
			return False
		return self.condition(phonemes[pos - 1], phonemes[pos], phonemes[pos + 1])

class SyllableInitialPhonologicalRule(BasePhonologicalRule):
	def check_environment(self, phonemes, pos):
		if pos == 0 and len(phonemes) > 0:
			return self.condition(phonemes[pos], phonemes[1]) 
		elif pos == len(phonemes) - 1:
			return False
		# apply simple SSP heuristic to determine if we're at a syllable start
		elif phonemes[pos - 1].is_more_sonorous(phonemes[pos]) and not phonemes[pos].is_more_sonorous(phonemes[pos + 1]):
			return self.condition(phonemes[pos], phonemes[1]) 
		else:
			return False

def check_features(phoneme, feature_values):
	return reduce(lambda a, b: a or b, [phoneme[type(f)] == f for f in feature_values])

def SimplePhonologicalRule(target, replacement, before=None, after=None):
	if before is not None and after is None:
		cond = lambda b, t, _: t == target and b is not None and check_features(b, before) 
	if before is not None and after is not None:
		cond = lambda b, t, a: t == target and b is not None and check_features(b, before) and a is not None and check_features(a, after)
	if before is None and after is not None:
		cond = lambda _, t, a: t == target and a is not None and check_features(a, after) 
	if before is None and after is None:
		cond = lambda _, t, __: t == target

	return PhonologicalRule(cond, lambda _ : replacement)


# ------------------- The orthophonology of a language -------------------#

class Orthophonology:
	def __init__(self, sound_inventory, alphabet, diphthongs, digraphs):
		self.sound_inventory = sound_inventory
		self.alphabet = alphabet
		self.diphthongs = diphthongs
		self.digraphs = digraphs
		self.di = {**self.diphthongs, **self.digraphs}
		self.rules = []

	def add_rule(self, rule):
		self.rules.append(rule)

	@staticmethod
	def tokenize(text):
		text = text.lower()
		text = re.sub(r"[.\";,:\[\]()!&?‘]", "", text)
		return text.split(' ')

	def transcribe_word(self, word):
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
				phonemes.append(self.alphabet[word[i]])
				i += 1

		# apply phonological rules.  Note: no restart!
		i = 0
		while i < len(phonemes):
		    for rule in self.rules:
		    	if rule.check_environment(phonemes, i):
		    		replacement = rule(phonemes, i)
		    		replacement = [replacement] if not isinstance(replacement, list) else replacement
		    		phonemes[i:i + 1] = replacement
		    		i += len(replacement)
		    		break
		    i += 1
		    		
		return phonemes

	def transcribe(self, text, as_phonemes = False):
		phoneme_words = [self.transcribe_word(word) for word in self.tokenize(text)]
		if not as_phonemes:
			words = [''.join([phoneme.ipa for phoneme in word]) for word in phoneme_words]
			return ' '.join(words)
		else:
			return phoneme_words

	def find_sound(self, phoneme) :
		for sound in self.sound_inventory:
			if sound.is_equal(phoneme):
				return sound
		return None

	def voice(self, consonant) :
		voiced_consonant = deepcopy(consonant)
		voiced_consonant[Voiced] = Voiced.pos
		return self.find_sound(voiced_consonant)

	@staticmethod
	def lengthen(vowel):
		return vowel.lengthen()
