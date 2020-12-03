"""A module for representing universal morphosyntactic feature bundles."""

from enum import auto
from typing import List, Type, Union

from cltk.core.exceptions import CLTKException
from cltk.utils.utils import CLTKEnum

__author__ = ["John Stewart <free-variation>"]


class MorphosyntacticFeature(CLTKEnum):
    """A generic multivalued morphosyntactic feature.
    """

    pass


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
# augmented with the +/-F(unctional) feature as developed by Fukui (1986).
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

    zeroth = auto()
    first = auto()
    second = auto()
    third = auto()
    fourth = auto()


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


nominal_features = [Case, Gender, Animacy, Number, Definiteness, Degree, Strength]


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


class Abbreviation(PrivativeFeature):
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
    def __init__(self, *features: List[MorphosyntacticFeature]) -> None:
        """
        >>> f1 = MorphosyntacticFeatureBundle(F.neg, N.pos, V.neg, Case.accusative)
        >>> f1.features
        {F: [neg], N: [pos], V: [neg], Case: [accusative]}
        """
        self.features = {}
        for feature in features:
            if isinstance(feature, type) and issubclass(
                feature, MorphosyntacticFeature
            ):
                self.features[feature] = Underspecified
            else:
                if type(feature) in self.features:
                    self.features[type(feature)].append(feature)
                else:
                    self.features[type(feature)] = [feature]

    def __getitem__(
        self, feature_name: Type[MorphosyntacticFeature]
    ) -> List[MorphosyntacticFeature]:
        """
        Use dict-type syntax for accessing the values of features.
        >>> f1 = f(F.pos, N.pos)
        >>> f1[F]
        [pos]
        >>> f1[V]
        Traceback (most recent call last):
        cltk.core.exceptions.CLTKException: {F: [pos], N: [pos]} unspecified for V
        """
        if not issubclass(feature_name, MorphosyntacticFeature):
            raise TypeError(str(feature_name) + " is not a morphosytactic feature")

        if feature_name in self.features:
            return self.features[feature_name]
        else:
            raise CLTKException(f"{self} unspecified for {feature_name}")

    def __setitem__(
        self,
        feature_name: Type[MorphosyntacticFeature],
        feature_values: Union[MorphosyntacticFeature, List[MorphosyntacticFeature]],
    ) -> "MorphosyntacticFeatureBundle":
        """
        Use dict-type syntax to set the value of features.
        >>> f1 = f(F.pos)
        >>> f1[N] = N.neg
        >>> f1
        {F: [pos], N: [neg]}
        """
        if not issubclass(feature_name, MorphosyntacticFeature):
            raise TypeError(str(feature_name) + " is not a morphosyntactic feature")

        if type(feature_values) is not list:
            feature_values = [feature_values]

        for value in feature_values:
            if value is not None and type(value) != feature_name:
                raise TypeError(str(value) + " is not a " + str(feature_name))

        self.features[feature_name] = feature_values
        return self

    def underspecify(self, feature_name: Type[MorphosyntacticFeature]) -> None:
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

    def matches(self, other: "MorphosyntacticFeatureBundle") -> bool:
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

    def __str__(self) -> str:
        return str(self.features)

    __repr__ = __str__


f = MorphosyntacticFeatureBundle


def to_categorial(pos: int) -> "MorphosyntacticFeatureBundle":
    """Maps UD parts of speech to binary categorial feature bundles.
    In some cases these are underspecified, including empty bundles for interjections.
    >>> to_categorial(POS.adjective)
    {F: [neg], N: [pos], V: [pos]}
    >>> to_categorial(POS.particle)
    {F: [pos]}
    >>> to_categorial(POS.interjection)
    {}
    """

    if pos == POS.adjective or pos == POS.adverb:
        return f(F.neg, N.pos, V.pos)
    elif pos == POS.adposition:
        return f(F.pos, N.neg, V.neg)
    elif pos == POS.auxiliary:
        return f(F.pos, N.neg, V.pos)
    elif (
        pos == POS.coordinating_conjunction
        or pos == POS.subordinating_conjunction
        or pos == POS.particle
    ):
        return f(F.pos)
    elif pos == POS.determiner or pos == POS.pronoun or pos == POS.numeral:
        return f(F.pos, N.pos, V.neg)
    elif pos == POS.noun or pos == POS.proper_noun:
        return f(F.neg, N.pos, V.neg)
    elif pos == POS.verb:
        return f(F.neg, N.neg, V.pos)
    else:
        return f()


from_ud_map = {
    # parts of speech
    "POS": {
        "ADJ": POS.adjective,
        "ADP": POS.adposition,
        "ADV": POS.adverb,
        "AUX": POS.auxiliary,
        "CCONJ": POS.coordinating_conjunction,
        "DET": POS.determiner,
        "INTJ": POS.interjection,
        "NOUN": POS.noun,
        "NUM": POS.numeral,
        "PART": POS.particle,
        "PRON": POS.pronoun,
        "PROPN": POS.proper_noun,
        "PUNCT": POS.punctuation,
        "SCONJ": POS.subordinating_conjunction,
        "SYM": POS.symbol,
        "VERB": POS.verb,
        "X": POS.other,
    },
    # verbal features
    "VerbForm": {
        "Conv": VerbForm.converb,
        "Fin": VerbForm.finite,
        "Gdv": VerbForm.gerundive,
        "Ger": VerbForm.gerund,
        "Inf": VerbForm.infinitive,
        "Part": VerbForm.participle,
        "Sup": VerbForm.supine,
        "Vnoun": VerbForm.masdar,
    },
    "Mood": {
        "Adm": Mood.admirative,
        "Cnd": Mood.conditional,
        "Des": Mood.desiderative,
        "Imp": Mood.imperative,
        "Ind": Mood.indicative,
        "Jus": Mood.jussive,
        "Nec": Mood.necessitative,
        "Opt": Mood.optative,
        "Pot": Mood.potential,
        "Prp": Mood.purposive,
        "Qot": Mood.quotative,
        "Sub": Mood.subjunctive,
    },
    "Tense": {
        "Fut": Tense.future,
        "Imp": Tense.imperfect,
        "Past": Tense.past,
        "Pqp": Tense.pluperfect,
        "Pres": Tense.present,
    },
    "Aspect": {
        "Hab": Aspect.habitual,
        "Imp": Aspect.imperfective,
        "Iter": Aspect.iterative,
        "Perf": Aspect.perfective,
        "Prog": Aspect.progressive,
        "Prosp": Aspect.prospective,
    },
    "Voice": {
        "Act": Voice.active,
        "Antip": Voice.antipassive,
        "Bfoc": Voice.beneficiary_focus,
        "Lfoc": Voice.location_focus,
        "Caus": Voice.causative,
        "Dir": Voice.direct,
        "Inv": Voice.inverse,
        "Mid": Voice.middle,
        "Pass": Voice.passive,
        "Rcp": Voice.reciprocal,
    },
    "Evident": {"Fh": Evidentiality.first_hand, "Nfh": Evidentiality.non_first_hand},
    "Polarity": {"Pos": Polarity.pos, "Neg": Polarity.neg},
    "Person": {
        "0": Person.zeroth,
        "1": Person.first,
        "2": Person.second,
        "3": Person.third,
        "4": Person.fourth,
    },
    "Polite": {
        "Elev": Politeness.elevated,
        "Form": Politeness.formal,
        "Humb": Politeness.humble,
        "Infm": Politeness.informal,
    },
    "Clusivity": {"Ex": Clusivity.exclusive, "In": Clusivity.inclusive},
    # nominal
    "Gender": {
        "Com": Gender.common,
        "Fem": Gender.feminine,
        "Masc": Gender.masculine,
        "Neut": Gender.neuter,
    },
    "Animacy": {
        "Anim": Animacy.animate,
        "Hum": Animacy.human,
        "Inan": Animacy.inanimate,
        "Nhum": Animacy.non_human,
    },
    "Number": {
        "Coll": Number.collective,
        "Count": Number.count_plural,
        "Dual": Number.dual,
        "Grpa": Number.greater_paucal,
        "Grpl": Number.greater_plural,
        "Inv": Number.inverse_number,
        "Pauc": Number.paucal,
        "Plur": Number.plural,
        "Ptan": Number.plurale_tantum,
        "Sing": Number.singular,
        "Tri": Number.trial,
    },
    "Case": {
        # structural cases
        "Nom": Case.nominative,
        "Acc": Case.accusative,
        "Erg": Case.ergative,
        "Abs": Case.absolutive,
        # oblique cases
        "Abe": Case.abessive,
        "Ben": Case.befefactive,
        "Caus": Case.causative,
        "Cmp": Case.comparative,
        "Cns": Case.considerative,
        "Com": Case.comitative,
        "Dat": Case.dative,
        "Dis": Case.distributive,
        "Equ": Case.equative,
        "Gen": Case.genitive,
        "Ins": Case.instrumental,
        "Par": Case.partitive,
        "Voc": Case.vocative,
        # spatiotemporal cases
        "Abl": Case.ablative,
        "Add": Case.additive,
        "Ade": Case.adessive,
        "All": Case.allative,
        "Del": Case.delative,
        "Ela": Case.elative,
        "Ess": Case.essive,
        "Ill": Case.illative,
        "Ine": Case.inessive,
        "Lat": Case.lative,
        "Loc": Case.locative,
        "Per": Case.perlative,
        "Sub": Case.sublative,
        "Sup": Case.superessive,
        "Ter": Case.terminative,
        "Tem": Case.temporal,
        "Tra": Case.translative,
    },
    "Definite": {
        "Com": Definiteness.complex,
        "Cons": Definiteness.construct_state,
        "Def": Definiteness.definite,
        "Ind": Definiteness.indefinite,
        "Spec": Definiteness.specific_indefinite,
    },
    "Degree": {
        "Abs": Degree.absolute_superlative,
        "Cmp": Degree.comparative,
        "Equ": Degree.equative,
        "Pos": Degree.positive,
        "Sup": Degree.superlative,
    },
    # other lexical
    "PronType": {
        "Art": PrononimalType.article,
        "Dem": PrononimalType.demonstrative,
        "Emp": PrononimalType.emphatic,
        "Exc": PrononimalType.exclamative,
        "Ind": PrononimalType.indefinite,
        "Int": PrononimalType.interrogative,
        "Neg": PrononimalType.negative,
        "Prs": PrononimalType.personal,
        "Rcp": PrononimalType.reciprocal,
        "Rel": PrononimalType.relative,
        "Tot": PrononimalType.total,
    },
    "AdpType": {
        "Prep": AdpositionalType.preposition,
        "Post": AdpositionalType.postposition,
        "Circ": AdpositionalType.circumposition,
        "Voc": AdpositionalType.vocalized_adposition,
    },
    "AdvType": {
        "Man": AdverbialType.manner,
        "Loc": AdverbialType.location,
        "Tim": AdverbialType.time,
        "Deg": AdverbialType.degree,
        "Cau": AdverbialType.cause,
        "Mod": AdverbialType.modality,
    },
    "VerbType": {
        "Aux": VerbType.auxiliary,
        "Cop": VerbType.copula,
        "Mod": VerbType.modal,
        "Light": VerbType.light,
    },
    "NumType": {
        "Card": Numeral.cardinal,
        "Dist": Numeral.distributive,
        "Frac": Numeral.fractional,
        "Mult": Numeral.multiplicative,
        "Ord": Numeral.ordinal,
        "Range": Numeral.range,
        "Sets": Numeral.sets,
    },
    "NameType": {
        "Geo": NameType.place,
        "Prs": NameType.person,
        "Giv": NameType.person_given_name,
        "Sur": NameType.person_surname,
        "Nat": NameType.nationality,
        "Com": NameType.company,
        "Pro": NameType.product,
        "Oth": NameType.other,
    },
    "Strength": {"Strong": Strength.strong, "Weak": Strength.weak},
    "Poss": {"Yes": Possessive},
    "Reflex": {"Yes": Reflexive},
    "Foreign": {"Yes": Foreign},
    "Abbr": {"Yes": Abbreviation},
    "Typo": {"Yes": Typo},
}


def from_ud(feature_name: str, feature_value: str) -> MorphosyntacticFeature:
    """For a given Universal Dependencies feature name and value,
    return the appropriate feature class/value.
    >>> from_ud('Case', 'Abl')
    ablative
    >>> from_ud('Abbr', 'Yes')
    Abbreviation
    >>> from_ud('PronType', 'Ind')
    indefinite
    """
    if feature_name in from_ud_map:
        feature_map = from_ud_map[feature_name]
    else:
        raise CLTKException(f"{feature_name}: Unrecognized UD feature name")

    values = feature_value.split(",")
    for value in values:
        if value in feature_map:
            return feature_map[value]
        else:
            raise CLTKException(
                f"{value}: Unrecognized value for UD feature {feature_name}"
            )
