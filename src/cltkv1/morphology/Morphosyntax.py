"""A module for representing universal morphosyntactic feature bundles."""

__author__ = ["John Stewart <free-variation>"]

from enum import IntEnum, auto

class MorphosyntacticFeature(IntEnum):
    def __eq__(self, other):
        return False if type(self) != type(other) else IntEnum.__eq__(self, other)

class PrivativeFeature(MorphosyntacticFeature):
    pass

class BinaryFeature(MorphosyntacticFeature):
    pass


# Categorial Features

class CategorialFeature(BinaryFeature):
    pass
    
class N(CategorialFeature):
    pos = auto()
    neg = auto()
    
class V(CategorialFeature):
    pos = auto()
    neg = auto()
    
class F(CategorialFeature):
    pos = auto()
    neg = auto()
    
    
# Verbal features

class VerbForm(MorphosyntacticFeature):
    converb = auto()
    finite = auto()
    gerund = auto()
    gerundive = auto()
    infinitive = auto()
    participle = auto()
    supine = auto()
    masdar = auto()
    
class Mood(MorphosyntacticFeature):
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
    future = auto()
    imperfect = auto()
    past = auto()
    pluperfect = auto()
    present = auto()
    
class Aspect(MorphosyntacticFeature):
    habitual = auto()
    imperfective = auto()
    iterative = auto()
    perfective = auto()
    progressive = auto()
    prospective = auto()
    
class Voice(MorphosyntacticFeature):
    active = auto()
    antipassive = auto()
    causative = auto()
    direct = auto()
    inverse = auto()
    middle = auto()
    passive = auto()
    reciprocal = auto()
    
class Evidentiality(MorphosyntacticFeature):
    first_hand = auto()
    non_first_hand = auto()
    
class Polarity(BinaryFeature):
    pos = auto()
    neg = auto()
    
class Person(MorphosyntacticFeature):
    zero = auto()
    one = auto()
    two = auto()
    three = auto()
    four = auto()
    
class Politeness(MorphosyntacticFeature):
    elevated = auto()
    formal = auto()
    humble = auto()
    informal = auto()
    
class Clusivity(MorphosyntacticFeature):
    exclusive = auto()
    inclusive = auto()
    
verbal_features = [VerbForm, Tense, Mood, Aspect, Voice, Person, Polarity, Politeness, Clusivity, Evidentiality]
    
# Nominal features
    
class Case(MorphosyntacticFeature):
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
    masculine = auto()
    feminine = auto()
    neuter = auto()
    common = auto()
    
class Animacy(MorphosyntacticFeature):
    animate = auto()
    human = auto()
    inaninate = auto()
    non_human = auto()
    
class Number(MorphosyntacticFeature):
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
    complex = auto()
    construct_state = auto()
    definite = auto()
    indefinite = auto()
    specific_indefinite = auto()
    
class Degree(MorphosyntacticFeature):
    absolute_superlative = auto()
    comparative = auto()
    equative = auto()
    positive = auto()
    superlative = auto()
    
nominal_features = [Case, Gender, Animacy, Number, Definiteness, Degree]
    
    
# Other lexical features
    
class PrononimalType(MorphosyntacticFeature):
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
    pass
    
class Numeral(MorphosyntacticFeature):
    cardinal = auto()
    distributive = auto()
    fractional = auto()
    multiplicative = auto()
    ordinal = auto()
    range = auto()
    sets = auto()
    
class Reflexive(PrivativeFeature):
    pass

class Foreign(PrivativeFeature):
    pass

class Abbr(PrivativeFeature):
    pass

class Typo(PrivativeFeature):
    pass


UnderspecifiedFeature = None

class MorphosyntacticFeatureBundle:
    def __init__(self, *features):
        """
        >>> f1 = MorphosyntacticFeatureBundle(F.neg, N.pos, V.neg, Case.accusative)
        >>> f1.features
        {<enum 'F'>: <F.neg: 2>,
         <enum 'N'>: <N.pos: 1>,
         <enum 'V'>: <V.neg: 2>,
         <enum 'Case'>: <Case.accusative: 2>}
        """
        self.features = {}
        for feature in features:
            if isinstance(feature, type) and issubclass(feature, MorphosyntacticFeature):
                self.features[feature] = UnspecifiedFeature
            else:
                self.features[type(feature)] = feature
        
    def __getitem__(self, feature_name):
        """
        Use dict-type syntax for accessing the values of features.
        >>> f1 = f(F.pos, N.pos)
        >>> f1[F]
        <F.pos: 1>
        >>> f1[V]
          ...
        KeyError: <enum 'V'>
        """
        if not issubclass(feature_name, MorphosyntacticFeature):
            raise TypeError(str(feature_name) + ' is not a morphosytactic feature')
        return self.features[feature_name]

    def __setitem__(self, feature_name, feature_value):
        """
        Use dict-type syntax to set the value of features.
        >>> f1 = f(F.pos)
        >>> f1[N] = N.neg
        >>> f1
        {<enum 'F'>: <F.pos: 1>, <enum 'N'>: <N.pos: 1>}
        """
        if not issubclass(feature_name, MorphosyntacticFeature):
            raise TypeError(str(feature_name) + ' is not a morphosyntactic feature')
        if feature_value is not None and type(feature_value) != feature_name:
            raise TypeError(str(feature_value) + ' is not a ' + str(feature_name))
        self.features[feature_name] = feature_value
        return self
    
    def underspecify(self, feature_name):
        """
        Underspecify the given feature in the bundle.
        >>> f1 = f(F.pos, N.pos, V.neg)
        >>> f1.underspecify(F)
        >>> f1[F] is UnderspecifiedFeature
        True
        """
        if not issubclass(feature_name, MorphosyntacticFeature):
            raise TypeError(str(feature_name) + ' is not a morphosytactic feature')
        self.features[feature_name] = UnderspecifiedFeature
        
    def matches(self, other):
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
            if self[f] is not UnderspecifiedFeature and \
                other[f] is not UnderspecifiedFeature and \
                not(self[f] == other[f]):
                return False
            
        return True
        
    def __str__(self):
        return str(self.features)
    
    __repr__ = __str__
        
f = MorphosyntacticFeatureBundle
