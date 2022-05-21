"""A module for representing universal morphosyntactic feature bundles."""

from typing import Dict, List, Optional, Tuple, Type, Union

from cltk.core.exceptions import CLTKException
from cltk.morphology.universal_dependencies_features import *

__author__ = ["John Stewart <free-variation>"]


class MorphosyntacticFeatureBundle:
    """A representation of a set of features, usually associated with a word form."""

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
        self, feature_name: Union[str, Type[MorphosyntacticFeature]]
    ) -> List[MorphosyntacticFeature]:
        """
        Use dict-type syntax for accessing the values of features.
        >>> f1 = f(F.pos, N.pos)
        >>> f1[F]
        [pos]
        >>> f1[V]
        Traceback (most recent call last):
        cltk.core.exceptions.CLTKException: {F: [pos], N: [pos]} unspecified for V
        >>> f1['F']
        [pos]
        """
        if type(feature_name) == str:
            if feature_name not in globals():
                raise TypeError(feature_name + " is not a morphosytactic feature")
            feature_name = globals()[feature_name]

        if not issubclass(feature_name, MorphosyntacticFeature):
            raise TypeError(str(feature_name) + " is not a morphosytactic feature")

        if feature_name in self.features:
            return self.features[feature_name]
        else:
            raise CLTKException(f"{self} unspecified for {feature_name}")

    def __setitem__(
        self,
        feature_name: Union[str, Type[MorphosyntacticFeature]],
        feature_values: Union[MorphosyntacticFeature, List[MorphosyntacticFeature]],
    ) -> "MorphosyntacticFeatureBundle":
        """
        Use dict-type syntax to set the value of features.
        >>> f1 = f(F.pos)
        >>> f1[N] = N.neg
        >>> f1
        {F: [pos], N: [neg]}
        >>> f1['V'] = V.pos
        >>> f1
        {F: [pos], N: [neg], V: [pos]}
        """
        if type(feature_name) == str:
            if feature_name not in globals():
                raise TypeError(feature_name + " is not a morphosytactic feature")
            feature_name = globals()[feature_name]

        if not issubclass(feature_name, MorphosyntacticFeature):
            raise TypeError(str(feature_name) + " is not a morphosyntactic feature")

        if type(feature_values) is not list:
            feature_values = [feature_values]

        for value in feature_values:
            if value is not None and type(value) != feature_name:
                raise TypeError(str(value) + " is not a " + str(feature_name))

        self.features[feature_name] = feature_values
        return self

    def all(
        self,
    ) -> List[Tuple[Type[MorphosyntacticFeature], List[MorphosyntacticFeature]]]:
        return self.features.items()

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

    def __iter__(self):
        return iter(self.features)

    __repr__ = __str__

    def keys(self):
        return self.features.keys()

    def values(self):
        return self.features.values()

    def items(self):
        return self.features.items()

    def __len__(self):
        return len(self.features)

    def __contains__(self, item: MorphosyntacticFeature):
        if not isinstance(item, MorphosyntacticFeature):
            # raise TypeError(str(item) + " is not a MorphosyntacticFeature")
            return False
        else:
            for i in self.features:
                if item in self.features[i]:
                    return True
            return False


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


FORM_UD_MAP: Dict[str, Dict[str, MorphosyntacticFeature]] = {
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
        "Psor": Person.psor,
        "Subj": Person.subj,
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
        "Psor": Gender.psor,
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
        "Psor": Number.psor,
    },
    "NumForm": {
        "Word": NumForm.word,
        "Digit": NumForm.digit,
        "Roman": NumForm.roman,
        "Reference": NumForm.reference,
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
    "Poss": {"Yes": Possessive.pos},
    "Reflex": {"Yes": Reflexive.pos},
    "Foreign": {"Yes": Foreign.pos},
    "Abbr": {"Yes": Abbreviation.pos},
    "Typo": {"Yes": Typo.pos},
}


def from_ud(feature_name: str, feature_value: str) -> Optional[MorphosyntacticFeature]:
    """For a given Universal Dependencies feature name and value,
    return the appropriate feature class/value.
    >>> from_ud('Case', 'Abl')
    ablative
    >>> from_ud('Abbr', 'Yes')
    pos
    >>> from_ud('PronType', 'Ind')
    indefinite
    """
    # Do cleanup on certain inputs that look like ``"Number[psor]``
    # Thus this is rewritten to ``feature_name = Number``
    # and ``feature_value = psor``.
    if "[" in feature_name and "]" in feature_name:
        feature_name_split: List[str] = feature_name.split("[", maxsplit=1)
        feature_name = feature_name_split[0]
        feature_value = feature_name_split[1][:-1]
        feature_value = feature_value.title()

    if feature_name in FORM_UD_MAP:
        feature_map = FORM_UD_MAP[feature_name]
    else:
        msg1: str = f"Unrecognized UD `feature_name` ('{feature_name}') with `feature_value` ('{feature_value}')."
        msg2: str = f"Please raise an issue at <https://github.com/cltk/cltk/issues> and include a small sample to reproduce the error."
        print(msg1)
        print(msg2)
        # raise CLTKException(msg)
        return None

    values = feature_value.split(",")
    for value in values:
        if value in feature_map:
            return feature_map[value]
        else:
            raise CLTKException(
                f"{value}: Unrecognized value for UD feature {feature_name}"
            )
