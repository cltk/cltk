"""Test cltk.phonology.orthophonology"""

__author__ = ["John Stewart <johnstewart@aya.yale.edu"]

import unittest
from copy import deepcopy

from cltk.phonology.orthophonology import *


# ------------------- Orthophonology of Etruscan (latin letters) -------------------
# Sounce: https://en.wikipedia.org/wiki/Etruscan_language#Phonology

# Consonants
m  = Consonant(Place.bilabial, Manner.nasal, Voiced.pos, 'm')
n  = Consonant(Place.alveolar, Manner.nasal, Voiced.pos, 'n')

p  = Consonant(Place.bilabial, Manner.stop, Voiced.neg, 'p')
ph = Consonant(Place.bilabial, Manner.stop, Voiced.neg, 'pʰ', aspirated = Aspirated.pos)
t  = Consonant(Place.alveolar, Manner.stop, Voiced.neg, 't')
th = Consonant(Place.alveolar, Manner.stop, Voiced.neg, 'tʰ', aspirated = Aspirated.pos)
k  = Consonant(Place.velar, Manner.stop, Voiced.neg, 'k')
kh = Consonant(Place.velar, Manner.stop, Voiced.neg, 'kʰ', aspirated = Aspirated.pos)

ts = Consonant(Place.dental, Manner.affricate, Voiced.neg, 'ts')

f  = Consonant(Place.bilabial, Manner.fricative, Voiced.neg, 'ɸ')
s  = Consonant(Place.alveolar, Manner.fricative, Voiced.neg, 's')
sh = Consonant(Place.post_alveolar, Manner.fricative, Voiced.neg, 'ʃ')
h  = Consonant(Place.glottal, Manner.fricative, Voiced.neg, 'h')

l  = Consonant(Place.alveolar, Manner.approximant, Voiced.pos, 'l')
j  = Consonant(Place.palatal, Manner.approximant, Voiced.pos, 'j')
w  = Consonant(Place.velar, Manner.approximant, Voiced.pos, 'w')

r  = Consonant(Place.alveolar, Manner.approximant, Voiced.pos, 'r')

# Vowels
i  = Vowel(Height.close, Backness.front, Roundedness.neg, Length.short, 'i')
u  = Vowel(Height.close, Backness.back, Roundedness.pos, Length.short, 'u') #o as allophone?
e  = Vowel(Height.mid, Backness.front, Roundedness.neg, Length.short, 'e')
a  = Vowel(Height.open, Backness.back, Roundedness.neg, Length.short, 'ɑ')

# diphthongs
ei = e + i
ai = a + i
au = a + u
ui = u + i
eu = e + ui

consonants = [m, n, p, ph, t, th, k, kh, ts, f, s, sh, h, l, j, w, r]
vowels = [i, u, e, a]
diphthongs = [ei, ai, au, ui, eu]

alphabet = {
	'a' : a,
	'c' : k,
	'd' : t,
	'θ' : th,
	'e' : e,
	'f' : f,
	'h' : h,
	'i' : i,
	'k' : k,
	'l' : l,
	'm' : m,
	'n' : n,
	'o' : u,
	'p' : p,
	'φ' : ph,
	'q' : k,
	'r' : r,
	's' : s,
	'ś' : sh,
	't' : t,
	'u' : u,
	'v' : w,
	'χ' : kh,
	'z' : ts
}

diphthongs_ipa = {
	'ei' : ei,
	'ai' : ai,
	'au' : au,
	'ui' : ui,
	'eu' : eu,

}


etruscan = Orthophonology(vowels + consonants + diphthongs, alphabet, diphthongs_ipa, {})


class TestOrthophonology(unittest.TestCase):
	"""Class for unit tests."""

	# phoneme tests
	def test_phoneme_category(self):
		self.assertEqual(a.features[Consonantal], Consonantal.neg)
		self.assertEqual(p.features[Consonantal], Consonantal.pos)

	def test_phoneme_getter(self):
		self.assertEqual(a[Backness], Backness.back)

	def test_phoneme_getter_nonfeature(self):
		self.assertEqual(a[Place], None)

	def test_phoneme_setter(self):
		k1 = deepcopy(k)
		k1[Aspirated] = Aspirated.pos
		self.assertEqual(k1[Aspirated], Aspirated.pos)

	def test_phoneme_equal(self):
		h1 = deepcopy(h)
		self.assertTrue(h1 == h)

	def test_phoneme_not_equal(self):
		self.assertFalse(u == e)

	def test_consonant_sonority(self):
		self.assertTrue(s.is_more_sonorous(p))
		self.assertFalse(p.is_more_sonorous(s))
		self.assertFalse(t.is_more_sonorous(s))

	def test_vowel_add(self):
		ae = a + e
		self.assertEqual(ae.ipa, a.ipa + e.ipa)
		self.assertEqual(ae[Backness], Backness.back)

	def test_vowel_lengthen(self):
		long_i = i.lengthen()
		self.assertEqual(long_i.ipa, i.ipa + ':')
		self.assertEqual(long_i[Length], Length.long)
		self.assertEqual(long_i[Backness], Backness.front)

	def test_vowel_sonority(self):
		self.assertTrue(a.is_more_sonorous(i))
		self.assertFalse(i.is_more_sonorous(e))

	def test_is_vowel(self):
		self.assertTrue(a.is_vowel())
		self.assertFalse(f.is_vowel())

	# Rule tests
	rule1 = BasePhonologicalRule(
		lambda before, target, after: target == a and before is not None and before[Consonantal] == Consonantal.pos\
		and after is not None and after[Consonantal] == Consonantal.pos,
		lambda target: target.lengthen())
	rule2 = PhonologicalRule(
		lambda before, target, after: isinstance(target, Consonant) and isinstance(before, Vowel),
		lambda target: etruscan.aspirate(target))

	# phonological rules using the DSL
	rule3 = Consonantal.pos >> Aspirated.pos | W - Backness.back
	rule4 = Consonantal.neg >> Length.long | Manner.fricative - W
	rule5 = Manner.stop >> sh | Consonantal.neg - Consonantal.neg
	rule6 = Consonantal.pos >> Aspirated.pos | S - Height.close
	rule7_1 = k >> sh | ANY - Backness.central
	rule7_2 = k >> sh | ANY - Backness.back
	rule8 = k >> [k, a] | ANY - Backness.back 
	rule9 = i // u >> a // e | W - ANY

	def test_base_phonological_rule(self):
		self.assertTrue(self.rule1.condition(p, a, t))
		self.assertFalse(self.rule1.condition(None, a, t))
		self.assertEqual(self.rule1([a], 0), a.lengthen())

	def test_phonological_rule(self):
		self.assertTrue(self.rule2.check_environment([a, t], 1))
		self.assertFalse(self.rule2.check_environment([t, a, k], 1))
		self.assertFalse(self.rule2.check_environment([], 1))
		self.assertEqual(self.rule2([a, t], 1), th)

	def test_word_initial_phonological_rule(self):
		self.assertTrue(self.rule3.check_environment([p, u, n], 0))
		self.assertFalse(self.rule3.check_environment([p, u, n], 1))
		self.assertFalse(self.rule3.check_environment([a, u, n], 0))
		self.assertFalse(self.rule3.check_environment([p], 0))
		self.assertFalse(self.rule3.check_environment([], 0))
		self.assertEqual(self.rule3([p, u, n], 0), ph)

	def test_word_final_phonological_rule(self):
		self.assertTrue(self.rule4.check_environment([u, f, a], 2))
		self.assertFalse(self.rule4.check_environment([u, f, a], 1))
		self.assertFalse(self.rule4.check_environment([u, f, f], 0))
		self.assertFalse(self.rule4.check_environment([a], 0))
		self.assertFalse(self.rule4.check_environment([], 0))
		self.assertEqual(self.rule4([u, f, a], 2), a.lengthen())

	def test_inner_phonological_rule(self):
		self.assertTrue(self.rule5.check_environment([a, t, i], 1))
		self.assertFalse(self.rule5.check_environment([a, f, i], 1))
		self.assertFalse(self.rule5.check_environment([p, i], 0))
		self.assertFalse(self.rule5.check_environment([a, k], 1))
		self.assertFalse(self.rule5.check_environment([t], 0))
		self.assertFalse(self.rule5.check_environment([], 0))
		self.assertEqual(self.rule5([a, t, i], 1), sh)

	def test_syllable_initial_phonological_rule(self):
		self.assertTrue(self.rule6.check_environment([t, i, n], 0))
		self.assertTrue(self.rule6.check_environment(etruscan._position_phonemes([a, k, e, t, i, n]), 3))
		self.assertFalse(self.rule6.check_environment([a, k, e, t, s, i, n], 4))
		self.assertFalse(self.rule6.check_environment([a, k, e, t, i, n], 0))
		self.assertFalse(self.rule6.check_environment([a, k, e, t, i, n], 2))
		self.assertFalse(self.rule6.check_environment([a, k, e, t, i, n], 4))
		self.assertFalse(self.rule6.check_environment([a, k, e, t, i, n], 5))
		self.assertEqual(self.rule6([a, k, e, t, i, n], 3), th)

	def test_simple_phonological_rule(self):
		self.assertTrue(self.rule7_2.check_environment([k, a], 0))
		self.assertFalse(self.rule7_2.check_environment([k, a], 1))
		self.assertTrue(self.rule7_2.check_environment([e, k, a], 1))
		self.assertFalse(self.rule7_1.check_environment([k], 0))
		self.assertFalse(self.rule7_1.check_environment([], 1))
		self.assertEqual(self.rule7_2([k, a], 0), sh)

	# Test the transcription system
	def test_transcription_letter(self):
		self.assertEqual(etruscan('a'), a.ipa)
		self.assertEqual(etruscan('a', as_phonemes = True), [[a]])

	def test_transcription_word(self):
		self.assertEqual(etruscan('cel'), 'kel')
		self.assertEqual(etruscan('qutum'), 'kutum')
		self.assertEqual(etruscan('qutum', as_phonemes = True), [[k, u, t, u, m]])
		self.assertEqual(etruscan('śuθina'), sh.ipa + u.ipa + th.ipa + i.ipa + n.ipa + a.ipa)

	def test_diphthongs(self):
		self.assertEqual(etruscan('aurum'), au.ipa + r.ipa + u.ipa + m.ipa)
		self.assertEqual(etruscan('leinθ'), l.ipa + ei.ipa + n.ipa + th.ipa)

	def setUp(self):
		self.etruscan2 = deepcopy(etruscan)

	def test_add_rule(self):
		self.etruscan2.add_rule(self.rule7_1)
		self.assertEqual(len(self.etruscan2.rules), 1)

	def test_add_rule(self):
		self.etruscan2 << self.rule3
		self.assertEqual(len(self.etruscan2.rules), 1)

	def test_rule_application(self):
		self.etruscan2.add_rule(self.rule7_1)
		self.etruscan2.add_rule(self.rule7_2)
		self.assertEqual(self.etruscan2('qutum'), 'ʃutum')

	def test_rule_ordering1(self):
		self.etruscan2.add_rule(self.rule7_1)
		self.etruscan2.add_rule(self.rule7_2)
		self.etruscan2.add_rule(self.rule3)
		self.assertEqual(self.etruscan2('qutum'), 'ʃutum')

	def test_rule_ordering2(self):
		self.etruscan2.add_rule(self.rule3)
		self.etruscan2.add_rule(self.rule7_1)
		self.etruscan2.add_rule(self.rule7_2)
		self.assertEqual(self.etruscan2('qutum'), kh.ipa + 'utum')

	def test_rule_multiple_phonemes_ordering(self):
		self.etruscan2.add_rule(self.rule8)
		self.etruscan2.add_rule(self.rule7_1)
		self.etruscan2.add_rule(self.rule7_2)
		self.assertEqual(self.etruscan2('qutum'), 'k' + a.ipa + 'utum')

	def test_rule_syntax1(self):
		self.etruscan2.add_rule(Consonantal.neg >> [Backness.back, Roundedness.pos] | Consonantal.pos - Consonantal.pos)
		self.assertEqual(self.etruscan2('kip'), 'k' + u.ipa + 'p')

	def test_is_syllable_initial(self):
		self.assertTrue(etruscan.is_syllable_initial([t, r, i], 0))
		self.assertTrue(etruscan.is_syllable_initial([a, k, u, p], 1))
		self.assertTrue(etruscan.is_syllable_initial([a, k, s, u], 1))
		self.assertFalse(etruscan.is_syllable_initial([a, k, u, p], 2))
		self.assertFalse(etruscan.is_syllable_initial([t, r, i], 2))

	def test_is_syllable_final(self):
		self.assertTrue(etruscan.is_syllable_final([t, r, i], 2))
		self.assertTrue(etruscan.is_syllable_final([a, k, u, p], 0))
		self.assertTrue(etruscan.is_syllable_final([a, k, s, u, r, t, i], 4))
		self.assertFalse(etruscan.is_syllable_final([a, k, u, p], 2))
		self.assertFalse(etruscan.is_syllable_final([t, r, i], 0))

	def test_disjunctive_phoneme_list(self):
		self.etruscan2.add_rule(self.rule9)
		self.assertEqual(self.etruscan2('iqut'), a.ipa + e.ipa + 'kut')
		self.assertEqual(self.etruscan2('uqut'), a.ipa + e.ipa + 'kut')
		self.assertNotEqual(self.etruscan2('equt'), a.ipa + e.ipa + 'kut')



