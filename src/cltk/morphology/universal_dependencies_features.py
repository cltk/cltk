"""Data types for each morphological category and features annotated
by the Universal Dependencies (UD) project
(<https://universaldependencies.org/guidelines.html>_).

These are from v2 of UD, except for ``Strength`` which is from v1
and was (as of 12/2020) still in the Gothic treebank.
"""
from enum import auto

from cltk.utils.utils import CLTKEnum


class MorphosyntacticFeature(CLTKEnum):
    """A generic multivalued morphosyntactic feature."""

    pass


# Categorial Features

# The following are the traditional categorial features [+/-N, +/-V] of generative linguistics,
# augmented with the +/-F(unctional) feature as developed by Fukui (1986).
# See Fukui, N. 1986. A theory of category projection and its applications. Ph.D. dissertation, MIT.
# Though simplistic by today's standards, the scheme is more-or-less sufficient to represent
# the parts of speech of the Universal Dependencies project (https://universaldependencies.org/u/pos/index.html).
# See http://primus.arts.u-szeged.hu/bese/Chapter1/1.3.1.htm for a readable explanation.


class N(MorphosyntacticFeature):
    """A `nominal word <https://en.wikipedia.org/wiki/Nominal_(linguistics)>_,
    "a category used to group together nouns and adjectives based on shared
    properties. The motivation for nominal grouping is that in many languages
    nouns and adjectives share a number of morphological and syntactic
    properties."
    """

    pos = auto()
    neg = auto()


class V(MorphosyntacticFeature):
    """A `verbal word <https://universaldependencies.org/u/pos/all.html#verb-verb>`_,
    which "typically signal events and actions, can constitute a minimal
    predicate in a clause, and govern the number and types of other
    constituents which may occur in the clause." See notes that verb-like forms
    may be better classed as eg, nouns, adjectives, etc..
    """

    pos = auto()
    neg = auto()


class F(MorphosyntacticFeature):
    """A `function word <https://en.wikipedia.org/wiki/Function_word>`_.
    These "have little lexical meaning or have ambiguous meaning and express
    grammatical relationships among other words within a sentence,
    or specify the attitude or mood of the speaker".
    """

    pos = auto()
    neg = auto()


class POS(MorphosyntacticFeature):
    """The POS "feature" represents the list of syntactic categories published by the UD project.
    See https://universaldependencies.org/u/pos/index.html
    """

    adjective = auto()
    adposition = auto()
    adverb = auto()
    auxiliary = auto()
    coordinating_conjunction = auto()
    determiner = auto()
    interjection = auto()
    noun = auto()
    numeral = auto()
    particle = auto()
    possessors_number = auto()
    pronoun = auto()
    proper_noun = auto()
    punctuation = auto()
    subordinating_conjunction = auto()
    symbol = auto()
    verb = auto()
    other = auto()


# Morphosyntactic Features.
# The inventory of features represented here are those of the Universal Dependencies project.
# See https://universaldependencies.org/u/feat/index.html
# While extensive, the inventory is naturally never quite complete.
# In particular, the list spatiotemporal cases is likely to grow over time.

# Verbal features, related to +V categories.


class VerbForm(MorphosyntacticFeature):
    """The inlectional type of the verb.
    Possibly this confuses tense, aspect, and other more privitive morphosyntactic informaition.
    see https://universaldependencies.org/u/feat/VerbForm.html
    """

    converb = auto()
    finite = auto()
    gerund = auto()
    gerundive = auto()
    infinitive = auto()
    participle = auto()
    supine = auto()
    masdar = auto()


class Mood(MorphosyntacticFeature):
    """The mood of a verb.
    see https://universaldependencies.org/u/feat/Mood.html
    """

    admirative = auto()
    conditional = auto()
    desiderative = auto()
    imperative = auto()
    indicative = auto()
    jussive = auto()
    necessitative = auto()
    optative = auto()
    potential = auto()
    purposive = auto()
    quotative = auto()
    subjunctive = auto()


class Tense(MorphosyntacticFeature):
    """The tense of a verb, i.e. the time of the eventuality in relation to a reference point in time.
    see https://universaldependencies.org/u/feat/Tense.html
    """

    future = auto()
    imperfect = auto()
    past = auto()
    pluperfect = auto()
    present = auto()


class Aspect(MorphosyntacticFeature):
    """The aspect of the verb, i.e. the temporal structure of the eventuality.
    see https://universaldependencies.org/u/feat/Aspect.html
    """

    habitual = auto()
    imperfective = auto()
    iterative = auto()
    perfective = auto()
    progressive = auto()
    prospective = auto()


class Voice(MorphosyntacticFeature):
    """The voice of the verb, i.e. the relation of the participants to the eventuality.
    see https://universaldependencies.org/u/feat/Voice.html
    """

    active = auto()
    antipassive = auto()
    beneficiary_focus = auto()
    location_focus = auto()
    causative = auto()
    direct = auto()
    inverse = auto()
    middle = auto()
    passive = auto()
    reciprocal = auto()


class Evidentiality(MorphosyntacticFeature):
    """What evidence is there for the assertion of the eventuality described by the verb?
    Is it based on the speaker's knowledge, or indirect?
    see https://universaldependencies.org/u/feat/Evident.html
    """

    first_hand = auto()
    non_first_hand = auto()


class Polarity(MorphosyntacticFeature):
    """Is the proposition negative or positive?
    see https://universaldependencies.org/u/feat/Polarity.html
    """

    pos = auto()
    neg = auto()


class Person(MorphosyntacticFeature):
    """The grammatical person of the verb, i.e. the participant indicated by the subject.
    # see https://universaldependencies.org/u/feat/Person.html
    """

    zeroth = auto()
    first = auto()
    second = auto()
    third = auto()
    fourth = auto()
    psor = auto()
    subj = auto()


class Politeness(MorphosyntacticFeature):
    """The morphological reflex of the formal register with which participants
    are addressed in the sentence, affecting verbs and pronouns.
    see https://universaldependencies.org/u/feat/Polite.html
    """

    elevated = auto()
    formal = auto()
    humble = auto()
    informal = auto()


class Clusivity(MorphosyntacticFeature):
    """Does a first person plural subject include the addressee?
    see https://universaldependencies.org/u/feat/Clusivity.html
    """

    exclusive = auto()
    inclusive = auto()


class Strength(MorphosyntacticFeature):
    """Is this a strong or weak verb or adjective?
    UDv1 feature, specific to Gothic.
    see http://universaldependencies.org/docsv1/got/feat/Strength.html
    """

    strong = auto()
    weak = auto()


VERBAL_FEATURES = [
    VerbForm,
    Tense,
    Mood,
    Aspect,
    Voice,
    Person,
    Polarity,
    Politeness,
    Clusivity,
    Evidentiality,
    Strength,
]

# Nominal features, related to the +N categories.


class Case(MorphosyntacticFeature):
    """The case of a noun phrase.
    see https://universaldependencies.org/u/feat/Case.html
    """

    # structural cases
    nominative = auto()
    accusative = auto()
    ergative = auto()
    absolutive = auto()

    # oblique cases
    abessive = auto()
    befefactive = auto()
    causative = auto()
    comparative = auto()
    considerative = auto()
    comitative = auto()
    dative = auto()
    distributive = auto()
    equative = auto()
    genitive = auto()
    instrumental = auto()
    partitive = auto()
    vocative = auto()

    # spatiotemporal cases
    ablative = auto()
    additive = auto()
    adessive = auto()
    allative = auto()
    delative = auto()
    elative = auto()
    essive = auto()
    illative = auto()
    inessive = auto()
    lative = auto()
    locative = auto()
    perlative = auto()
    sublative = auto()
    superessive = auto()
    terminative = auto()
    temporal = auto()
    translative = auto()


class Gender(MorphosyntacticFeature):
    """The grammatical gender of a nominal.
    see https://universaldependencies.org/u/feat/Gender.html
    """

    masculine = auto()
    feminine = auto()
    neuter = auto()
    common = auto()
    psor = auto()


class Animacy(MorphosyntacticFeature):
    """The soul-type of an entity (as it were.)
    see https://universaldependencies.org/u/feat/Animacy.html
    """

    animate = auto()
    human = auto()
    inanimate = auto()
    non_human = auto()


class Number(MorphosyntacticFeature):
    """The count type of an entity.
    see https://universaldependencies.org/u/feat/Number.html
    """

    collective = auto()
    count_plural = auto()
    dual = auto()
    greater_paucal = auto()
    greater_plural = auto()
    inverse_number = auto()
    paucal = auto()
    plural = auto()
    plurale_tantum = auto()
    singular = auto()
    trial = auto()
    psor = auto()


class NumForm(MorphosyntacticFeature):
    """Feature of cardinal and ordinal numbers.
    Is the number expressed by digits or as a word?
    See `<https://universaldependencies.org/cs/feat/NumForm.html>`_.
    """

    word = auto()
    digit = auto()
    roman = auto()
    reference = auto()


class Definiteness(MorphosyntacticFeature):
    """The relationship between noun phrases and
    entities in or not in the discoursive context.
    see https://universaldependencies.org/u/feat/Definiteness.html
    """

    complex = auto()
    construct_state = auto()
    definite = auto()
    indefinite = auto()
    specific_indefinite = auto()


class Degree(MorphosyntacticFeature):
    """The degree of adjectives.
    see https://universaldependencies.org/u/feat/Degree.html
    """

    absolute_superlative = auto()
    comparative = auto()
    equative = auto()
    positive = auto()
    superlative = auto()


NOMINAL_FEATURES = [Case, Gender, Animacy, Number, Definiteness, Degree, Strength]


# Other lexical features


class NameType(MorphosyntacticFeature):
    """The type of a named entity, mostly applying to proper nouns.
    see https://universaldependencies.org/u/feat/NameType.html
    """

    place = auto()
    person = auto()
    person_given_name = auto()
    person_surname = auto()
    nationality = auto()
    company = auto()
    product = auto()
    other = auto()


class PrononimalType(MorphosyntacticFeature):
    """A subclassification of pronouns.
    see https://universaldependencies.org/u/feat/PronType.html
    """

    article = auto()
    demonstrative = auto()
    emphatic = auto()
    exclamative = auto()
    indefinite = auto()
    interrogative = auto()
    negative = auto()
    personal = auto()
    reciprocal = auto()
    relative = auto()
    total = auto()


class AdpositionalType(MorphosyntacticFeature):
    """Defines the position of an adposition.
    see https://universaldependencies.org/u/feat/AdpType.html
    """

    preposition = auto()
    postposition = auto()
    circumposition = auto()
    vocalized_adposition = auto()


class AdverbialType(MorphosyntacticFeature):
    """What type of adverb is this?
    see https://universaldependencies.org/u/feat/AdvType.html
    """

    manner = auto()
    location = auto()
    time = auto()
    degree = auto()
    cause = auto()
    modality = auto()


class VerbType(MorphosyntacticFeature):
    """If this is a functional verb, what kind is it?
    see https://universaldependencies.org/u/feat/VerbType.html
    """

    auxiliary = auto()
    copula = auto()
    modal = auto()
    light = auto()


class Possessive(MorphosyntacticFeature):
    """Is this nominal form marked as a possessive?
    see https://universaldependencies.org/u/feat/Poss.html
    """

    pos = auto()
    neg = auto()


class Numeral(MorphosyntacticFeature):
    """A subclassification of numeric types.
    see https://universaldependencies.org/u/feat/NumType.html
    """

    cardinal = auto()
    distributive = auto()
    fractional = auto()
    multiplicative = auto()
    ordinal = auto()
    range = auto()
    sets = auto()


class Reflexive(MorphosyntacticFeature):
    """Is the pronoun reflexive?
    see https://universaldependencies.org/u/feat/Reflex.html
    """

    pos = auto()
    neg = auto()


class Foreign(MorphosyntacticFeature):
    """Is this a foreign word, relative to the language of the sentences?
    see https://universaldependencies.org/u/feat/Foreign.html
    """

    pos = auto()
    neg = auto()


class Abbreviation(MorphosyntacticFeature):
    """Is this word an abbreviation?
    see https://universaldependencies.org/u/feat/Abbr.html
    """

    pos = auto()
    neg = auto()

    pass


class Typo(MorphosyntacticFeature):
    """Does this word contain a typo?
    see https://universaldependencies.org/u/feat/Typo.html
    """

    pos = auto()
    neg = auto()


# the feature value of an underspecified feature.
Underspecified = None

OTHER_FEATURES = [
    NameType,
    PrononimalType,
    AdpositionalType,
    AdverbialType,
    VerbType,
    Possessive,
    Numeral,
    Reflexive,
    Foreign,
    Abbreviation,
    Typo,
]
