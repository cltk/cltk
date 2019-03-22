"""
Sources:
- https://en.wikipedia.org/wiki/Old_English_phonology
- https://ealdaenglisc.wordpress.com/old-english-lessons/lesson-0-alphabet-and-pronunciation/
"""

from cltk.phonology.orthophonology import *

__author__ = ["John Stewart <johnstewart@aya.yale.edu>"]


### The Consonants

# nasals
m  = Consonant(Place.bilabial, Manner.nasal, Voiced.pos, 'm')
n  = Consonant(Place.alveolar, Manner.nasal, Voiced.pos, 'n')
n0 = Consonant(Place.alveolar, Manner.nasal, Voiced.neg, 'n̥')
ng = Consonant(Place.velar, Manner.nasal, Voiced.pos, 'ŋ')

# plosives
p  = Consonant(Place.bilabial, Manner.stop, Voiced.neg, 'p')
b  = Consonant(Place.bilabial, Manner.stop, Voiced.pos, 'b')
t  = Consonant(Place.alveolar, Manner.stop, Voiced.neg, 't')
d  = Consonant(Place.alveolar, Manner.stop, Voiced.pos, 'd')
k  = Consonant(Place.velar, Manner.stop, Voiced.neg, 'k')
g  = Consonant(Place.velar, Manner.stop, Voiced.pos, 'g')

# affricates
tsh = Consonant(Place.post_alveolar, Manner.affricate, Voiced.neg, 't͡ʃ')
dsh = Consonant(Place.post_alveolar, Manner.affricate, Voiced.pos, 'd͡ʒ')

# fricatives
f  = Consonant(Place.bilabial, Manner.fricative, Voiced.neg, 'f')
v  = Consonant(Place.bilabial, Manner.fricative, Voiced.pos, 'v')
th = Consonant(Place.dental, Manner.fricative, Voiced.neg, 'θ')
dh = Consonant(Place.dental, Manner.fricative, Voiced.pos, 'ð')
s  = Consonant(Place.alveolar, Manner.fricative, Voiced.neg, 's')
z  = Consonant(Place.alveolar, Manner.fricative, Voiced.pos, 'z')
sh = Consonant(Place.post_alveolar, Manner.fricative, Voiced.neg, 'ʃ')
ch = Consonant(Place.palatal, Manner.fricative, Voiced.neg, 'ç')
x  = Consonant(Place.velar, Manner.fricative, Voiced.neg, 'x')
y  = Consonant(Place.velar, Manner.fricative, Voiced.pos, 'ɣ')
h  = Consonant(Place.glottal, Manner.fricative, Voiced.neg, 'h')

# approximants
l  = Consonant(Place.alveolar, Manner.approximant, Voiced.pos, 'l')
l0 = Consonant(Place.alveolar, Manner.approximant, Voiced.neg, 'l̥')
j  = Consonant(Place.palatal, Manner.approximant, Voiced.pos, 'j')
w  = Consonant(Place.velar, Manner.approximant, Voiced.pos, 'w')
w0 = Consonant(Place.velar, Manner.approximant, Voiced.neg, 'w')

# rhotics
r  = Consonant(Place.alveolar, Manner.approximant, Voiced.pos, 'r')
r0 = Consonant(Place.alveolar, Manner.approximant, Voiced.neg, 'r̥')	


### The Vowels

# monophongs
i  = Vowel(Height.close, Backness.front, Roundedness.neg, Length.short, 'i')
i_long = i.lengthen()
y  = Vowel(Height.close, Backness.front, Roundedness.pos, Length.short, 'y')
y_long = y.lengthen()
u  = Vowel(Height.close, Backness.back, Roundedness.pos, Length.short, 'u')
u_long = u.lengthen()
e  = Vowel(Height.mid, Backness.front, Roundedness.neg, Length.short, 'e')
e_long = e.lengthen()
oe = Vowel(Height.mid, Backness.front, Roundedness.pos, Length.short, 'ø')
oe_long = oe.lengthen()
o  = Vowel(Height.mid, Backness.back, Roundedness.pos, Length.short, 'o')
o_long = o.lengthen()
ae = Vowel(Height.open, Backness.front, Roundedness.neg, Length.short, 'æ')
ae_long = ae.lengthen()
a  = Vowel(Height.open, Backness.back, Roundedness.neg, Length.short, 'ɑ')
a_long = a.lengthen()

# diphthongs
aea = ae + a
ae_long_a = ae_long + a
eo = e + o
e_long_o = e_long + o
iu = i + u
i_long_u = i_long + u


consonants = [
	m, n, n0, ng,
	p, b, t, d, k, g,
	tsh, dsh,
	f, v, th, dh, s, z, sh, ch, x, y, h,
	l, l0, j, w, w0,
	r, r0
]

vowels = [
	i, i_long, y, y_long, u, u_long,
	e, e_long, oe, oe_long, o, o_long,
	ae, ae_long, a, a_long
]

diphthongs = [
	aea, ae_long_a, eo, e_long_o, iu, i_long_u
]

sound_inventory = consonants + vowels + diphthongs

# these are the UNCONDITIONED sounds of the letters.
alphabet = {
	'a' : a,
	'ā' : a_long,
	'æ' : ae,
	'ǣ' : ae_long,
	'b' : b,
	'c' : k,
	'ċ' : tsh,
	'd' : d,
	'ð' : dh,
	'e' : e,
	'ē' : e_long,
	'f' : f,
	'g' : g,
	'ġ' : j,
	'h' : h,
	'i' : i,
	'ī' : i_long,
	'l' : l,
	'm' : m,
	'n' : n,
	'o' : o,
	'ō' : o_long,
	'p' : p,
	'r' : r,
	's' : s,
	't' : t,
	'u' : u,
	'ū' : u_long,
	'w' : w,
	'x' : x,
	'y' : y,
	'ȳ' : y_long,
	'þ' : th
}

diphthongs_ipa = {
	'ea' : aea,
	'ēa' : ae_long_a,
	'ie' : i,
	'īe' : i_long,
	'eo' : eo,
	'ēo' : e_long_o,
	'io' : iu,
	'īo' : i_long_u
}

digraphs_ipa = {
	'cg' : dsh,
	'ng' : ng,
	'sc' : sh
}

oe = Orthophonology(sound_inventory, alphabet, diphthongs_ipa, digraphs_ipa)

# intervocalic fricatives are voiced
oe << InnerPhonologicalRule(
	condition = lambda before, target, after: 
		before.is_vowel() and target in [f, s, th] and after.is_vowel(),
	action = lambda target: 
		oe.voice(target))

# could also be:
# Manner.fricative >> Voiced.pos | Consonantal.neg - Consonantal.neg
# or
# [Manner.fricative] >> [Voiced.pos] | [Consonantal.neg] - [Consonantal.neg]

# /k/ is palatized in specific environments
oe << PhonologicalRule(
	condition = lambda before, target, after:
		target == k and
		(after is not None and after[Backness] == Backness.front or
		(before is not None and before == i and 
			(after is None or (isinstance(after, Vowel) and after[Backness] != Backness.back)))),
	action = lambda _: tsh)

# palatization of /g/
oe << InnerPhonologicalRule(
	condition = lambda before, target, after:
		target == g and
		(after[Backness] == Backness.front or
		(before[Backness] == Backness.front and not(after[Backness] == Backness.back))),
	action = lambda _ : j)

# /g/ is fricativized when intervocalic
oe << InnerPhonologicalRule(
	condition = lambda before, target, after:
		(before.is_vowel() or before[Voiced] == Voiced.pos) and
		target == g and
		(after.is_vowel() or after[Voiced] == Voiced.pos),
	action = lambda _ : y)


oe.add_rule(h >> x | Backness.back - ANY )

oe.add_rule(h >> ch | Backness.front - ANY)

# 'sc' is *not* a digraph after a back consonant
oe << PhonologicalRule(
	condition = lambda before, target, _ : target == sh and Backness.back in before,
	action = lambda _ : [s, k])

OldEnglishOrthophonology = oe

