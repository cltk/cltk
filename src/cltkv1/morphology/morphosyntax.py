"""A module for representing universal morphosyntactic feature bundles."""

from enum import IntEnum, auto
from typing import List, Type

__author__ = ["John Stewart <free-variation>"]


class MorphosyntacticFeature(IntEnum):
    def __eq__(self : 'MorphosyntacticFeature', other : 'MorphosyntacticFeature') -> bool :
        return False if type(self) != type(other) else IntEnum.__eq__(self, other)


class PrivativeFeature(MorphosyntacticFeature):
    """A privative feature either exists, or it does not exist.
    There is no value associated with the feature."""

    pass


class BinaryFeature(MorphosyntacticFeature):
    """A binary feature takes either a positive or negative value."""

    pass


# Categorial Features


class CategorialFeature(BinaryFeature):
    """A categorial feature is a binary feature that contributes to
    identifying the part of speech of a lexical unit."""

    pass


# The following are the traditional categorial features [+/-N, +/-V] of generative linguistics,
# extended with the +/-F(unctional) feature as developed by Fukui (1986).
# See Fukui, N. 1986. A theory of category projection and its applications. Ph.D. dissertation, MIT.
# Though simplistic by today's standards, the scheme is more-or-less sufficient to represent
# the parts of speech of the Universal Dependencies project (https://universaldependencies.org/u/pos/index.html).
# See http://primus.arts.u-szeged.hu/bese/Chapter1/1.3.1.htm for a readable explanation.


class N(CategorialFeature):
    pos = auto()
    neg = auto()


class V(CategorialFeature):
    pos = auto()
    neg = auto()


class F(CategorialFeature):
    pos = auto()
    neg = auto()


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


class Polarity(BinaryFeature):
    """Is the proposition negative or positive?
    see https://universaldependencies.org/u/feat/Polarity.html
    """

    pos = auto()
    neg = auto()


class Person(MorphosyntacticFeature):
    """The grammatical person of the verb, i.e. the participant indicated by the subject.
    # see https://universaldependencies.org/u/feat/Person.html
    """

    zero = auto()
    one = auto()
    two = auto()
    three = auto()
    four = auto()


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


verbal_features = [
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


class Animacy(MorphosyntacticFeature):
    """The soul-type of an entity (as it were.)
    see https://universaldependencies.org/u/feat/Animacy.html
    """

    animate = auto()
    human = auto()
    inaninate = auto()
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


nominal_features = [Case, Gender, Animacy, Number, Definiteness, Degree]


# Other lexical features


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


class Possessive(PrivativeFeature):
    """Is this nominal form marked as a possessive?
    see https://universaldependencies.org/u/feat/Poss.html
    """

    pass


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


class Reflexive(PrivativeFeature):
    """Is the pronoun reflexive?
    see https://universaldependencies.org/u/feat/Reflex.html
    """

    pass


class Foreign(PrivativeFeature):
    """Is this a foreign word, relative to the language of the sentences?
    see https://universaldependencies.org/u/feat/Foreign.html
    """

    pass


class Abbr(PrivativeFeature):
    """Is this word an abbreviation?
    see https://universaldependencies.org/u/feat/Abbr.html
    """

    pass


class Typo(PrivativeFeature):
    """Does this word contain a typo?
    see https://universaldependencies.org/u/feat/Typo.html
    """

    pass


# the feature value of an underspecified feature.
Underspecified = None


class MorphosyntacticFeatureBundle:
    def __init__(self, *features : List[MorphosyntacticFeature]) -> None:
        """
        >>> f1 = MorphosyntacticFeatureBundle(F.neg, N.pos, V.neg, Case.accusative)
        >>> f1.features
        {<enum 'F'>: <F.neg: 2>, <enum 'N'>: <N.pos: 1>, <enum 'V'>: <V.neg: 2>, <enum 'Case'>: <Case.accusative: 2>}
        """
        self.features = {}
        for feature in features:
            if isinstance(feature, type) and issubclass(
                feature, MorphosyntacticFeature
            ):
                self.features[feature] = Underspecified
            else:
                self.features[type(feature)] = feature

    def __getitem__(self, feature_name : Type[MorphosyntacticFeature]) -> MorphosyntacticFeature:
        """
        Use dict-type syntax for accessing the values of features.
        >>> f1 = f(F.pos, N.pos)
        >>> f1[F]
        <F.pos: 1>
        >>> f1[V]
        Traceback (most recent call last):
        KeyError: <enum 'V'>
        """
        if not issubclass(feature_name, MorphosyntacticFeature):
            raise TypeError(str(feature_name) + " is not a morphosytactic feature")
        return self.features[feature_name]

    def __setitem__(self, feature_name : Type[MorphosyntacticFeature], 
        feature_value : MorphosyntacticFeature) -> 'MorphosyntacticFeatureBundle' :
        """
        Use dict-type syntax to set the value of features.
        >>> f1 = f(F.pos)
        >>> f1[N] = N.neg
        >>> f1
        {<enum 'F'>: <F.pos: 1>, <enum 'N'>: <N.neg: 2>}
        """
        if not issubclass(feature_name, MorphosyntacticFeature):
            raise TypeError(str(feature_name) + " is not a morphosyntactic feature")
        if feature_value is not None and type(feature_value) != feature_name:
            raise TypeError(str(feature_value) + " is not a " + str(feature_name))
        self.features[feature_name] = feature_value
        return self

    def underspecify(self, feature_name : Type[MorphosyntacticFeature]) -> None:
        """
        Underspecify the given feature in the bundle.
        >>> f1 = f(F.pos, N.pos, V.neg)
        >>> f1.underspecify(F)
        >>> f1[F] is Underspecified
        True
        """
        if not issubclass(feature_name, MorphosyntacticFeature):
            raise TypeError(str(feature_name) + " is not a morphosytactic feature")
        self.features[feature_name] = Underspecified

    def matches(self, other : 'MorphosyntacticFeatureBundle') -> bool :
        """
        This feature bundle matches other if other contains all the features of this bundle,
        i.e. if this bundle is an improper subset of other.
        Underspecified features will match.
        
        >>> f1 = f(F, N.pos, V.neg)
        >>> f2 = f(F.neg, N.pos, V.neg)
        >>> f3 = f(F.pos, N.neg, V.pos)
        >>> f1.matches(f2)
        True
        >>> f1.matches(f3)
        False
        """
        if other is None:
            return False
        for f in self.features.keys():
            if f not in other.features:
                return False
            if (
                self[f] is not Underspecified
                and other[f] is not Underspecified
                and not (self[f] == other[f])
            ):
                return False

        return True

    def __str__(self) -> str :
        return str(self.features)

    __repr__ = __str__


f = MorphosyntacticFeatureBundle
