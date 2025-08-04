"""Universal Dependencies (UD) Features and Values.

https://universaldependencies.org/u/feat/index.html
"""

from typing import Literal, Optional

from pydantic import BaseModel, ValidationError, field_validator, model_validator

from cltk.core.cltk_logger import logger


class UDFeatureValue(BaseModel):
    code: str  # e.g., "Masc"
    label: str  # e.g., "Masculine"
    description: str  # Full explanation
    is_deprecated: Optional[bool] = False


class UDFeature(BaseModel):
    key: str  # e.g., "Case"
    category: Literal["Lexical", "Inflectional", "Other"]
    description: str
    values: dict[str, UDFeatureValue]
    inflectional_class: Optional[Literal["Nominal", "Verbal"]] = None


class UDFeatureTag(BaseModel):
    # Use this when instantiated a tagged word
    key: str
    value: str
    value_label: str = ""
    category: Literal["Lexical", "Inflectional", "Other"] = "Lexical"
    inflectional_class: Optional[Literal["Nominal", "Verbal"]] = None

    @model_validator(mode="before")
    @classmethod
    def fill_fields(cls, data):
        key = data.get("key")
        value = data.get("value")
        if key not in UD_FEATURES_MAP:
            raise ValueError(f"Invalid UD feature key: '{key}'")
        feature = UD_FEATURES_MAP[key]
        if value not in feature.values:
            raise ValueError(f"Invalid value '{value}' for feature key '{key}'")
        data["category"] = feature.category
        data["inflectional_class"] = feature.inflectional_class
        data["value_label"] = feature.values[value].label
        return data

    def __str__(self):
        return f"UDFeatureTag(" f"{self.key}={self.value_label}" + ")"

    def __repr__(self):
        return self.__str__()


class UDFeatureTagSet(BaseModel):
    # `add_feature` would be a little faster if this were a dict
    # `features: dict[str, UDFeatureTag] = {}`
    features: list[UDFeatureTag] = []

    def add_feature(self, feature: UDFeatureTag) -> None:
        if any(f.key == feature.key for f in self.features):
            logger.error(
                f"Feature with key '{feature.key}' already exists in the tag set."
            )
            return None
        self.features.append(feature)
        logger.debug(f"Added feature {feature.key} to UDFeatureTagSet.")

    def __str__(self):
        features_str = ", ".join(str(f) for f in self.features)
        return f"UDFeatureTagSet([{features_str}])"

    def __repr__(self):
        return self.__str__()


UD_FEATURES: list[UDFeature] = [
    UDFeature(
        key="PronType",
        category="Lexical",
        inflectional_class=None,
        description=(
            "PronType classifies pronouns and determiners by semantic or syntactic type, "
            "such as personal, demonstrative, interrogative, or indefinite. "
            "It applies to pronouns, determiners, and pronominal adverbs."
        ),
        values={
            "Prs": UDFeatureValue(
                code="Prs",
                label="Personal",
                description=(
                    "Personal pronouns refer to the speaker, addressee, or other participant. "
                    "E.g., I, you, he, she, we, they."
                ),
            ),
            "Rcp": UDFeatureValue(
                code="Rcp",
                label="Reciprocal",
                description="Reciprocal pronouns indicate mutual action or relation. E.g., each other.",
            ),
            "Ref": UDFeatureValue(
                code="Ref",
                label="Reflexive",
                description="Reflexive pronouns refer back to the subject. E.g., myself, yourself.",
            ),
            "Int": UDFeatureValue(
                code="Int",
                label="Interrogative",
                description="Used in questions. E.g., who, what, which.",
            ),
            "Rel": UDFeatureValue(
                code="Rel",
                label="Relative",
                description="Introduce relative clauses. E.g., who, which, that.",
            ),
            "Dem": UDFeatureValue(
                code="Dem",
                label="Demonstrative",
                description="Refer to specific entities. E.g., this, that, these, those.",
            ),
            "Emp": UDFeatureValue(
                code="Emp",
                label="Emphatic",
                description="Used for emphasis. Language-specific.",
            ),
            "Tot": UDFeatureValue(
                code="Tot",
                label="Total",
                description="Refer to the totality of a set. E.g., all, every.",
            ),
            "Neg": UDFeatureValue(
                code="Neg",
                label="Negative",
                description="Negative pronouns. E.g., nobody, nothing.",
            ),
            "Ind": UDFeatureValue(
                code="Ind",
                label="Indefinite",
                description="Refer to nonspecific entities. E.g., someone, anything.",
            ),
            "Exc": UDFeatureValue(
                code="Exc",
                label="Exclusive",
                description="Exclude certain referents. E.g., other, else.",
            ),
        },
    ),
    UDFeature(
        key="NumType",
        category="Lexical",
        inflectional_class=None,
        description=(
            "NumType classifies numerals and related determiners or pronouns by type, "
            "such as cardinal, ordinal, or multiplicative. It applies to adjectives, numerals, "
            "determiners, and pronominal words expressing numeric concepts."
        ),
        values={
            "Card": UDFeatureValue(
                code="Card",
                label="Cardinal",
                description="Basic counting numerals. E.g., one, two, three.",
            ),
            "Ord": UDFeatureValue(
                code="Ord",
                label="Ordinal",
                description="Express order or sequence. E.g., first, second, third.",
            ),
            "Mult": UDFeatureValue(
                code="Mult",
                label="Multiplicative",
                description="Indicate number of times something occurs. E.g., once, twice.",
            ),
            "Frac": UDFeatureValue(
                code="Frac",
                label="Fractional",
                description="Fractional numerals. E.g., half, third.",
            ),
            "Sets": UDFeatureValue(
                code="Sets",
                label="Set",
                description="Indicate a number of sets. E.g., double, triple.",
            ),
            "Dist": UDFeatureValue(
                code="Dist",
                label="Distributive",
                description="Distribute items in groups. E.g., each, every two.",
            ),
            "Gen": UDFeatureValue(
                code="Gen",
                label="General",
                description="Generic number word without clear numeric function. E.g., many.",
            ),
            "Range": UDFeatureValue(
                code="Range",
                label="Range",
                description="Express a numerical range. E.g., 5–10.",
            ),
        },
    ),
    UDFeature(
        key="Poss",
        category="Lexical",
        inflectional_class=None,
        description=(
            "Poss indicates whether a word (typically a pronoun, determiner, or adjective) "
            "expresses possession. This is common in possessive pronouns (e.g., my, your) "
            "and possessive adjectives."
        ),
        values={
            "Yes": UDFeatureValue(
                code="Yes",
                label="Possessive",
                description="The word is possessive (e.g., my, your, his, her).",
            )
        },
    ),
    UDFeature(
        key="Reflex",
        category="Lexical",
        inflectional_class=None,
        description=(
            "Reflex indicates whether a pronoun or other word is reflexive—that is, "
            "it refers back to the subject of the clause. Typically used for pronouns "
            "like 'myself', 'yourself', or 'themselves'."
        ),
        values={
            "Yes": UDFeatureValue(
                code="Yes",
                label="Reflexive",
                description="The word is reflexive and refers back to the subject.",
            )
        },
    ),
    UDFeature(
        key="Gender",
        category="Lexical",
        inflectional_class="Nominal",
        description=(
            "Gender is usually a lexical feature of nouns and an inflectional feature "
            "of other parts of speech that mark agreement with nouns. It typically "
            "reflects distinctions such as masculine, feminine, and neuter, though the "
            "exact set of genders is language-specific."
        ),
        values={
            "Masc": UDFeatureValue(
                code="Masc",
                label="Masculine",
                description="Used with male animate referents or masculine grammatical gender.",
            ),
            "Fem": UDFeatureValue(
                code="Fem",
                label="Feminine",
                description="Used with female animate referents or feminine grammatical gender.",
            ),
            "Neut": UDFeatureValue(
                code="Neut",
                label="Neuter",
                description="Used with inanimate referents or neuter grammatical gender.",
            ),
            "Com": UDFeatureValue(
                code="Com",
                label="Common",
                description="A gender category that merges masculine and feminine; e.g., Swedish utrum.",
            ),
            "Anim": UDFeatureValue(
                code="Anim",
                label="Animate",
                description="Grammatical gender used with animate referents.",
            ),
            "Inan": UDFeatureValue(
                code="Inan",
                label="Inanimate",
                description="Grammatical gender used with inanimate referents.",
            ),
            "Hum": UDFeatureValue(
                code="Hum",
                label="Human",
                description="Grammatical gender used with specifically human referents.",
            ),
            "Nhum": UDFeatureValue(
                code="Nhum",
                label="Non-human",
                description="Grammatical gender used with animate but non-human referents (e.g., animals).",
            ),
        },
    ),
    UDFeature(
        key="Animacy",
        category="Lexical",
        inflectional_class="Nominal",
        description=(
            "Animacy distinguishes between classes of nouns and related words "
            "according to whether they are alive, human, or personified. It is a "
            "lexical feature of nouns and an agreement feature of modifiers or verbs "
            "in some languages."
        ),
        values={
            "Anim": UDFeatureValue(
                code="Anim",
                label="Animate",
                description="Animate entities, typically human or animal, but may also include personified objects.",
            ),
            "Inan": UDFeatureValue(
                code="Inan",
                label="Inanimate",
                description="Inanimate entities such as objects, places, or abstract concepts.",
            ),
            "Hum": UDFeatureValue(
                code="Hum",
                label="Human",
                description="Specifically refers to human beings.",
            ),
            "Nhum": UDFeatureValue(
                code="Nhum",
                label="Non-human",
                description="Refers to animate but non-human entities, such as animals or supernatural beings.",
            ),
        },
    ),
    UDFeature(
        key="NounClass",
        category="Lexical",
        inflectional_class="Nominal",
        description=(
            "NounClass is a lexical feature of nouns and an agreement feature for other "
            "parts of speech in languages that use noun class systems (also called noun classes, "
            "genders, or classifiers). These systems can involve many more distinctions than traditional gender."
        ),
        values={
            "1": UDFeatureValue(
                code="1",
                label="Class 1",
                description="Typically used for human singulars in Bantu languages.",
            ),
            "2": UDFeatureValue(
                code="2",
                label="Class 2",
                description="Often plural counterpart to class 1 in Bantu.",
            ),
            "3": UDFeatureValue(
                code="3",
                label="Class 3",
                description="Used for trees, natural forces, or other non-human entities in some languages.",
            ),
            "4": UDFeatureValue(
                code="4", label="Class 4", description="Often the plural of class 3."
            ),
            "5": UDFeatureValue(
                code="5",
                label="Class 5",
                description="Various uses, sometimes augmentative or for paired objects.",
            ),
            "6": UDFeatureValue(
                code="6",
                label="Class 6",
                description="Often plural of class 5 or for mass nouns.",
            ),
            "7": UDFeatureValue(
                code="7", label="Class 7", description="Used for tools or objects."
            ),
            "8": UDFeatureValue(
                code="8", label="Class 8", description="Plural of class 7."
            ),
            "9": UDFeatureValue(
                code="9",
                label="Class 9",
                description="Common for animals or inanimate objects.",
            ),
            "10": UDFeatureValue(
                code="10", label="Class 10", description="Plural of class 9."
            ),
            "11": UDFeatureValue(
                code="11",
                label="Class 11",
                description="Augmentative or abstract forms in some languages.",
            ),
            "12": UDFeatureValue(
                code="12",
                label="Class 12",
                description="Diminutives or other derivational forms.",
            ),
            "13": UDFeatureValue(
                code="13",
                label="Class 13",
                description="Used for certain mass nouns or derived forms.",
            ),
            "14": UDFeatureValue(
                code="14",
                label="Class 14",
                description="Another mass noun class in some Bantu languages.",
            ),
            "15": UDFeatureValue(
                code="15",
                label="Class 15",
                description="Typically used for infinitive verb forms functioning as nouns.",
            ),
            # Extend up to 20+ classes as needed per language-specific implementations
        },
    ),
    UDFeature(
        key="Number",
        category="Inflectional",
        inflectional_class="Nominal",
        description=(
            "Number is an inflectional feature used to express count distinctions, such as singular, "
            "plural, or dual. It applies to nouns, pronouns, adjectives, and verbs that show agreement "
            "with a subject or object."
        ),
        values={
            "Sing": UDFeatureValue(
                code="Sing", label="Singular", description="Refers to one entity."
            ),
            "Plur": UDFeatureValue(
                code="Plur",
                label="Plural",
                description="Refers to more than one entity.",
            ),
            "Dual": UDFeatureValue(
                code="Dual", label="Dual", description="Refers to exactly two entities."
            ),
            "Trial": UDFeatureValue(
                code="Trial",
                label="Trial",
                description="Refers to exactly three entities. Used in some Oceanic languages.",
            ),
            "Pauc": UDFeatureValue(
                code="Pauc",
                label="Paucal",
                description="Refers to a small group greater than two but not many. Used in some Australian and Austronesian languages.",
            ),
            "Grpa": UDFeatureValue(
                code="Grpa",
                label="Greater paucal",
                description="Used for groups larger than paucal but not full plural. Language-specific.",
            ),
            "Grpl": UDFeatureValue(
                code="Grpl",
                label="Greater plural",
                description="Refers to a large or collective group. Language-specific.",
            ),
            "Inv": UDFeatureValue(
                code="Inv",
                label="Inverse",
                description="Inverse number marking. Indicates marked number differs from the noun’s default number.",
            ),
            "Count": UDFeatureValue(
                code="Count",
                label="Count plural",
                description="Plural form used only with numerals in some languages (e.g., Arabic).",
            ),
            "Ptan": UDFeatureValue(
                code="Ptan",
                label="Plurale tantum",
                description="Used for nouns that only occur in the plural (e.g., 'scissors').",
            ),
            "Coll": UDFeatureValue(
                code="Coll",
                label="Collective",
                description="Used for singular forms that refer to a group or mass (e.g., 'team', 'family').",
            ),
        },
    ),
    UDFeature(
        key="Case",
        category="Inflectional",
        inflectional_class="Nominal",
        description=(
            "Case is an inflectional feature used to mark a noun’s or pronoun’s syntactic or semantic role in a clause. "
            "It also appears on determiners, adjectives, numerals, and participles when they agree with a noun."
        ),
        values={
            "Nom": UDFeatureValue(
                code="Nom",
                label="Nominative",
                description="Marks the subject of a finite verb.",
            ),
            "Acc": UDFeatureValue(
                code="Acc",
                label="Accusative",
                description="Marks the direct object of a verb.",
            ),
            "Gen": UDFeatureValue(
                code="Gen",
                label="Genitive",
                description="Marks possession or other relationships between nouns.",
            ),
            "Dat": UDFeatureValue(
                code="Dat",
                label="Dative",
                description="Marks the indirect object or recipient.",
            ),
            "Abl": UDFeatureValue(
                code="Abl",
                label="Ablative",
                description="Marks movement away from something, source or cause.",
            ),
            "Loc": UDFeatureValue(
                code="Loc",
                label="Locative",
                description="Marks location or place where something happens.",
            ),
            "Voc": UDFeatureValue(
                code="Voc", label="Vocative", description="Used for direct address."
            ),
            "Ins": UDFeatureValue(
                code="Ins",
                label="Instrumental",
                description="Marks the instrument or means by which an action is performed.",
            ),
            "All": UDFeatureValue(
                code="All",
                label="Allative",
                description="Marks movement toward something.",
            ),
            "Ela": UDFeatureValue(
                code="Ela",
                label="Elative",
                description="Marks movement out of something.",
            ),
            "Ill": UDFeatureValue(
                code="Ill",
                label="Illative",
                description="Marks movement into something.",
            ),
            "Ade": UDFeatureValue(
                code="Ade",
                label="Adessive",
                description="Marks presence at or near something.",
            ),
            "Del": UDFeatureValue(
                code="Del",
                label="Delative",
                description="Marks movement off or away from a surface.",
            ),
            "Sub": UDFeatureValue(
                code="Sub",
                label="Sublative",
                description="Marks movement onto or under something.",
            ),
            "Sup": UDFeatureValue(
                code="Sup",
                label="Superessive",
                description="Marks location on a surface.",
            ),
            "Ter": UDFeatureValue(
                code="Ter",
                label="Terminative",
                description="Marks the endpoint or goal of an action.",
            ),
            "Lat": UDFeatureValue(
                code="Lat",
                label="Lative",
                description="Marks motion to a location, directionality.",
            ),
            "Tem": UDFeatureValue(
                code="Tem",
                label="Temporal",
                description="Marks relationships in time, like duration or time point.",
            ),
            "Tra": UDFeatureValue(
                code="Tra",
                label="Translative",
                description="Marks change of state or transformation into something.",
            ),
            "Cau": UDFeatureValue(
                code="Cau",
                label="Causal",
                description="Marks the cause or reason for something.",
            ),
            "Par": UDFeatureValue(
                code="Par",
                label="Partitive",
                description="Marks a subset or partial quantity of something.",
            ),
        },
    ),
    UDFeature(
        key="Definite",
        category="Lexical",
        inflectional_class="Nominal",
        description=(
            "Definiteness indicates whether a noun phrase refers to a specific entity that is identifiable "
            "in the given context. It commonly appears on determiners, pronouns, and sometimes on adjectives or nouns."
        ),
        values={
            "Def": UDFeatureValue(
                code="Def",
                label="Definite",
                description="Refers to a specific entity presumed known to the listener. E.g., 'the book'.",
            ),
            "Ind": UDFeatureValue(
                code="Ind",
                label="Indefinite",
                description="Refers to a nonspecific entity. E.g., 'a book'.",
            ),
            "Spec": UDFeatureValue(
                code="Spec",
                label="Specific indefinite",
                description="Refers to a specific but not uniquely identifiable entity. E.g., 'a certain book'.",
            ),
            "Cons": UDFeatureValue(
                code="Cons",
                label="Construct state",
                description="Marks construct state in Semitic languages, often as a form of definiteness.",
            ),
        },
    ),
    UDFeature(
        key="Deixis",
        category="Lexical",
        inflectional_class="Nominal",
        description=(
            "Deixis marks distinctions in deixis (reference to discourse context, typically in space or time), "
            "especially in demonstratives and deictic pronouns. It may also apply to spatial adverbs and determiners."
        ),
        values={
            "Prox": UDFeatureValue(
                code="Prox",
                label="Proximal",
                description="Refers to something close to the speaker. E.g., 'this'.",
            ),
            "Med": UDFeatureValue(
                code="Med",
                label="Medial",
                description="Refers to something near the listener or mid-distance. E.g., 'that' (in some languages).",
            ),
            "Dist": UDFeatureValue(
                code="Dist",
                label="Distal",
                description="Refers to something distant from both speaker and listener. E.g., 'that over there'.",
            ),
            "Remt": UDFeatureValue(
                code="Remt",
                label="Remote",
                description="Refers to a far-away or contextually very distant referent (space or time).",
            ),
            "Ablt": UDFeatureValue(
                code="Ablt",
                label="Ablative",
                description="Refers to a referent moving or located away from a point of reference.",
            ),
            "Allv": UDFeatureValue(
                code="Allv",
                label="Allative",
                description="Refers to a referent moving toward a point of reference.",
            ),
            "Locy": UDFeatureValue(
                code="Locy",
                label="Locative",
                description="Refers to a referent located at or near a point of reference.",
            ),
        },
    ),
    UDFeature(
        key="DeixisRef",
        category="Lexical",
        inflectional_class="Nominal",
        description=(
            "DeixisRef specifies the referent used to determine deictic orientation — usually the speaker, "
            "the addressee, or a third person. It is typically used in languages that have multiple demonstrative systems "
            "based on relative perspective."
        ),
        values={
            "Spkr": UDFeatureValue(
                code="Spkr",
                label="Speaker-oriented",
                description="Deictic frame is anchored to the speaker's location or perspective.",
            ),
            "Addr": UDFeatureValue(
                code="Addr",
                label="Addressee-oriented",
                description="Deictic frame is anchored to the addressee's perspective.",
            ),
            "Thrd": UDFeatureValue(
                code="Thrd",
                label="Third-person-oriented",
                description="Deictic frame is anchored to a third-person referent, neither speaker nor addressee.",
            ),
        },
    ),
    UDFeature(
        key="Degree",
        category="Inflectional",
        inflectional_class="Nominal",
        description=(
            "Degree is an inflectional feature of adjectives and adverbs that expresses comparison "
            "or intensity, such as positive, comparative, and superlative forms."
        ),
        values={
            "Pos": UDFeatureValue(
                code="Pos",
                label="Positive",
                description="Base form with no comparison. E.g., 'big', 'quickly'.",
            ),
            "Cmp": UDFeatureValue(
                code="Cmp",
                label="Comparative",
                description="Form that expresses a comparison between two entities. E.g., 'bigger', 'more quickly'.",
            ),
            "Sup": UDFeatureValue(
                code="Sup",
                label="Superlative",
                description="Form that expresses the extreme or highest degree. E.g., 'biggest', 'most quickly'.",
            ),
            "Abs": UDFeatureValue(
                code="Abs",
                label="Absolute superlative",
                description="Emphatic or intensifying form used in some languages. E.g., Spanish *altísimo* ('very tall').",
            ),
        },
    ),
    UDFeature(
        key="VerbForm",
        category="Inflectional",
        inflectional_class="Verbal",
        description=(
            "VerbForm indicates the morphological form of a verb, distinguishing among finite verbs, "
            "infinitives, participles, gerunds, supines, and other non-finite verb forms. "
            "This feature is crucial for understanding the syntactic role and inflectional behavior of verbs."
        ),
        values={
            "Fin": UDFeatureValue(
                code="Fin",
                label="Finite",
                description="Verb form marked for tense, mood, person, or number, and capable of serving as the main verb of a clause.",
            ),
            "Inf": UDFeatureValue(
                code="Inf",
                label="Infinitive",
                description="Basic verb form not marked for tense, person, or number. Often used as a non-finite complement.",
            ),
            "Part": UDFeatureValue(
                code="Part",
                label="Participle",
                description="Verb form used as an adjective or noun; may retain verbal features like voice or aspect.",
            ),
            "Ger": UDFeatureValue(
                code="Ger",
                label="Gerund",
                description="Verb form functioning as a noun (especially in English or Romance languages).",
            ),
            "Sup": UDFeatureValue(
                code="Sup",
                label="Supine",
                description="Non-finite verb form used in some languages (e.g., Latin, Romanian) in purpose or result constructions.",
            ),
            "Conv": UDFeatureValue(
                code="Conv",
                label="Converb",
                description="Non-finite verb form expressing adverbial subordination (e.g., 'while doing'). Common in Turkic and Uralic languages.",
            ),
            "Vnoun": UDFeatureValue(
                code="Vnoun",
                label="Verbal noun",
                description="Noun derived from a verb that retains some verbal properties. Common in Celtic and Slavic languages.",
            ),
        },
    ),
    UDFeature(
        key="Mood",
        category="Inflectional",
        inflectional_class="Verbal",
        description=(
            "Mood is an inflectional feature that expresses the speaker’s attitude toward the action or state "
            "of the verb. It often conveys distinctions such as indicative, imperative, conditional, subjunctive, "
            "and other modality-related categories."
        ),
        values={
            "Ind": UDFeatureValue(
                code="Ind",
                label="Indicative",
                description="Default factual mood used for statements and questions. E.g., 'He eats.'",
            ),
            "Imp": UDFeatureValue(
                code="Imp",
                label="Imperative",
                description="Used for commands or direct requests. E.g., 'Eat!'",
            ),
            "Cnd": UDFeatureValue(
                code="Cnd",
                label="Conditional",
                description="Expresses hypothetical or contingent actions. E.g., 'He would eat.'",
            ),
            "Sub": UDFeatureValue(
                code="Sub",
                label="Subjunctive",
                description="Used in subordinate clauses to express wishes, doubts, or unreal situations. E.g., 'If he were here...'",
            ),
            "Opt": UDFeatureValue(
                code="Opt",
                label="Optative",
                description="Expresses hope, desire, or permission. E.g., 'May you live long.'",
            ),
            "Des": UDFeatureValue(
                code="Des",
                label="Desiderative",
                description="Conveys a wish or desire to perform an action. E.g., 'He wants to eat.'",
            ),
            "Nec": UDFeatureValue(
                code="Nec",
                label="Necessitative",
                description="Expresses necessity or obligation. E.g., 'He must eat.'",
            ),
            "Pot": UDFeatureValue(
                code="Pot",
                label="Potential",
                description="Conveys possibility or ability. E.g., 'He might eat.'",
            ),
            "Jus": UDFeatureValue(
                code="Jus",
                label="Jussive",
                description="Used for indirect commands or exhortations. E.g., 'Let him go.'",
            ),
            "Adm": UDFeatureValue(
                code="Adm",
                label="Admirative",
                description="Expresses surprise, irony, or doubt. Found in languages like Albanian.",
            ),
            "Prp": UDFeatureValue(
                code="Prp",
                label="Purposive",
                description="Used to express purpose clauses. Found in some African languages.",
            ),
            "Qot": UDFeatureValue(
                code="Qot",
                label="Quotative",
                description="Used in reported speech or quoting. E.g., 'He said he eats.'",
            ),
            "Sim": UDFeatureValue(
                code="Sim",
                label="Similative",
                description="Used to express similarity or hypothetical parallel. E.g., 'as if he were king.'",
            ),
            "Int": UDFeatureValue(
                code="Int",
                label="Intentional",
                description="Used to express intent or plan. E.g., 'He is to eat.'",
            ),
        },
    ),
    UDFeature(
        key="Tense",
        category="Inflectional",
        inflectional_class="Verbal",
        description=(
            "Tense is an inflectional feature that situates the action or state of the verb in time, "
            "typically relative to the moment of speaking. Common tenses include past, present, and future, "
            "but some languages have more fine-grained distinctions."
        ),
        values={
            "Pres": UDFeatureValue(
                code="Pres",
                label="Present",
                description="Indicates that the situation holds at the moment of speaking or writing.",
            ),
            "Past": UDFeatureValue(
                code="Past",
                label="Past",
                description="Indicates that the situation held before the moment of speaking.",
            ),
            "Fut": UDFeatureValue(
                code="Fut",
                label="Future",
                description="Indicates that the situation will hold after the moment of speaking.",
            ),
            "Imp": UDFeatureValue(
                code="Imp",
                label="Imperfect",
                description="Refers to past actions that are habitual, ongoing, or incomplete. Common in Romance languages.",
            ),
            "Pqp": UDFeatureValue(
                code="Pqp",
                label="Pluperfect",
                description="Indicates that the event occurred prior to another past event. E.g., 'He had eaten.'",
            ),
        },
    ),
    UDFeature(
        key="Aspect",
        category="Inflectional",
        inflectional_class="Verbal",
        description=(
            "Aspect is an inflectional feature that encodes temporal structure—such as whether an action "
            "is completed, ongoing, repetitive, or bounded. It is often marked on verbs and auxiliaries, "
            "either morphologically or syntactically."
        ),
        values={
            "Imp": UDFeatureValue(
                code="Imp",
                label="Imperfective",
                description="Describes an ongoing, habitual, repeated, or unbounded event. E.g., 'He was running.'",
            ),
            "Perf": UDFeatureValue(
                code="Perf",
                label="Perfective",
                description="Describes a completed or bounded event. E.g., 'He ran.'",
            ),
            "Prog": UDFeatureValue(
                code="Prog",
                label="Progressive",
                description="Focuses on the internal structure of an ongoing event. E.g., 'He is running.'",
            ),
            "Hab": UDFeatureValue(
                code="Hab",
                label="Habitual",
                description="Indicates regularly recurring or habitual actions. E.g., 'He runs every day.'",
            ),
            "Prosp": UDFeatureValue(
                code="Prosp",
                label="Prospective",
                description="Marks events that are about to happen. E.g., 'He is going to run.'",
            ),
            "Iter": UDFeatureValue(
                code="Iter",
                label="Iterative",
                description="Describes events that occur repeatedly. E.g., 'He knocked and knocked.'",
            ),
            "Dur": UDFeatureValue(
                code="Dur",
                label="Durative",
                description="Emphasizes that the action lasted over a period of time.",
            ),
            "Tel": UDFeatureValue(
                code="Tel",
                label="Telic",
                description="Describes actions with a natural endpoint or goal.",
            ),
            "Atel": UDFeatureValue(
                code="Atel",
                label="Atelic",
                description="Describes actions without a fixed endpoint.",
            ),
        },
    ),
    UDFeature(
        key="Voice",
        category="Inflectional",
        inflectional_class="Verbal",
        description=(
            "Voice is an inflectional feature that encodes the relationship between the verb's arguments, "
            "especially the subject and object. It indicates whether the subject is the agent (active), "
            "patient (passive), or involved in other grammatical roles (middle, causative, etc.)."
        ),
        values={
            "Act": UDFeatureValue(
                code="Act",
                label="Active",
                description="The subject is the agent of the verb. E.g., 'The cat ate the mouse.'",
            ),
            "Pass": UDFeatureValue(
                code="Pass",
                label="Passive",
                description="The subject is the patient or recipient of the action. E.g., 'The mouse was eaten by the cat.'",
            ),
            "Mid": UDFeatureValue(
                code="Mid",
                label="Middle",
                description="The subject is both agent and patient; the action reflects back. E.g., 'The door opens easily.'",
            ),
            "Antip": UDFeatureValue(
                code="Antip",
                label="Antipassive",
                description="Demotes or omits the object, often used in ergative languages.",
            ),
            "Cau": UDFeatureValue(
                code="Cau",
                label="Causative",
                description="Indicates that the subject causes someone else to perform the action.",
            ),
            "Rcp": UDFeatureValue(
                code="Rcp",
                label="Reciprocal",
                description="Indicates mutual action among multiple participants. E.g., 'They hugged each other.'",
            ),
            "Adm": UDFeatureValue(
                code="Adm",
                label="Admissive",
                description="Marks a permitted or tolerated action. Language-specific.",
            ),
            "Bfoc": UDFeatureValue(
                code="Bfoc",
                label="Benefactive",
                description="Voice emphasizing the beneficiary of the action.",
            ),
            "Dir": UDFeatureValue(
                code="Dir",
                label="Direct",
                description="Indicates direct alignment of arguments (agent-focused).",
            ),
            "Inv": UDFeatureValue(
                code="Inv",
                label="Inverse",
                description="Reverses typical alignment; common in hierarchical or obviative systems.",
            ),
        },
    ),
    UDFeature(
        key="Evident",
        category="Inflectional",
        inflectional_class="Verbal",
        description=(
            "Evident is an inflectional feature used to indicate the source of information or evidence for a statement. "
            "It is found in languages with grammaticalized evidentiality, where speakers must specify whether they witnessed "
            "an event, inferred it, or heard it secondhand."
        ),
        values={
            "Fh": UDFeatureValue(
                code="Fh",
                label="Firsthand",
                description="The speaker claims direct evidence for the event (e.g., saw it happen).",
            ),
            "Nfh": UDFeatureValue(
                code="Nfh",
                label="Non-firsthand",
                description="The speaker did not witness the event directly; it may be inferred, reported, or assumed.",
            ),
        },
    ),
    UDFeature(
        key="Polarity",
        category="Inflectional",
        inflectional_class="Verbal",
        description=(
            "Polarity is an inflectional feature that indicates whether a clause or verb phrase "
            "is affirmative or negative. In many languages, negation is marked morphologically on the verb or auxiliary."
        ),
        values={
            "Pos": UDFeatureValue(
                code="Pos",
                label="Positive",
                description="Indicates that the statement or clause is affirmative.",
            ),
            "Neg": UDFeatureValue(
                code="Neg",
                label="Negative",
                description="Indicates that the statement or clause is negative.",
            ),
        },
    ),
    UDFeature(
        key="Person",
        category="Inflectional",
        inflectional_class="Verbal",
        description=(
            "Person is an inflectional feature that expresses the participant role of the word "
            "in the speech act: first person (speaker), second person (addressee), or third person "
            "(someone else). It appears on pronouns, verbs, and sometimes possessive determiners."
        ),
        values={
            "0": UDFeatureValue(
                code="0",
                label="Impersonal",
                description="Used in impersonal constructions with no specific subject, such as 'it rains'.",
            ),
            "1": UDFeatureValue(
                code="1",
                label="First person",
                description="The speaker or a group including the speaker. E.g., 'I', 'we'.",
            ),
            "2": UDFeatureValue(
                code="2",
                label="Second person",
                description="The addressee or a group including the addressee. E.g., 'you'.",
            ),
            "3": UDFeatureValue(
                code="3",
                label="Third person",
                description="Someone or something other than the speaker or addressee. E.g., 'he', 'she', 'they'.",
            ),
            "4": UDFeatureValue(
                code="4",
                label="Fourth person",
                description="Rarely used; in some languages, refers to obviative or logophoric referents.",
            ),
        },
    ),
    UDFeature(
        key="Polite",
        category="Inflectional",
        inflectional_class="Verbal",
        description=(
            "Polite is an inflectional feature that indicates the level of politeness, honorific status, or formality "
            "expressed by a pronoun, verb, or other part of speech. It is typically used in languages with honorific or "
            "formality distinctions (e.g., Japanese, Korean, Javanese)."
        ),
        values={
            "Infm": UDFeatureValue(
                code="Infm",
                label="Informal",
                description="Used for informal or familiar speech with close peers or subordinates.",
            ),
            "Form": UDFeatureValue(
                code="Form",
                label="Formal",
                description="Used for polite, respectful, or distant speech with strangers or superiors.",
            ),
            "Elev": UDFeatureValue(
                code="Elev",
                label="Elevated",
                description="Used to honor the referent. Often used for respected persons or social superiors.",
            ),
            "Humb": UDFeatureValue(
                code="Humb",
                label="Humble",
                description="Used to humble the speaker in relation to the listener or referent.",
            ),
            "Coll": UDFeatureValue(
                code="Coll",
                label="Colloquial",
                description="Casual or slang-like form. May mark relaxed register or dialectal usage.",
            ),
        },
    ),
    UDFeature(
        key="Clusivity",
        category="Inflectional",
        inflectional_class="Verbal",
        description=(
            "Clusivity is an inflectional feature of first-person plural pronouns and agreement markers that distinguishes "
            "between inclusive (including the addressee) and exclusive (excluding the addressee) reference. "
            "It is especially relevant in Austronesian, Dravidian, and Indigenous American languages."
        ),
        values={
            "In": UDFeatureValue(
                code="In",
                label="Inclusive",
                description="First person plural includes the speaker and the addressee (e.g., 'we' = you and I).",
            ),
            "Ex": UDFeatureValue(
                code="Ex",
                label="Exclusive",
                description="First person plural excludes the addressee (e.g., 'we' = I and others, but not you).",
            ),
        },
    ),
    UDFeature(
        key="Abbr",
        category="Other",
        inflectional_class=None,
        description=(
            "Abbr is a boolean feature used to indicate that a token is an abbreviation or acronym. "
            "This feature applies regardless of part of speech and is often used to explain nonstandard or shortened forms."
        ),
        values={
            "Yes": UDFeatureValue(
                code="Yes",
                label="Abbreviated",
                description="The word is an abbreviation or acronym (e.g., 'etc.', 'Dr.', 'USA').",
            )
        },
    ),
    UDFeature(
        key="Typo",
        category="Other",
        inflectional_class=None,
        description=(
            "Typo is a boolean feature used to indicate that a word is a misspelling or contains a typographical error. "
            "This feature is used primarily in treebanks that preserve the original, non-normalized form of the text."
        ),
        values={
            "Yes": UDFeatureValue(
                code="Yes",
                label="Typographical error",
                description="The token is a typographical or spelling error and appears uncorrected in the corpus.",
            )
        },
    ),
    UDFeature(
        key="Foreign",
        category="Other",
        inflectional_class=None,
        description=(
            "Foreign is a boolean feature used to mark tokens that are foreign words or phrases embedded "
            "in otherwise monolingual text. It helps distinguish between true code-switching and lone foreign insertions."
        ),
        values={
            "Yes": UDFeatureValue(
                code="Yes",
                label="Foreign word",
                description="The token is a foreign word or phrase used within another language's context.",
            )
        },
    ),
    UDFeature(
        key="ExtPos",
        category="Other",
        inflectional_class=None,
        description=(
            "ExtPos is a technical feature that stores an extended part-of-speech tag different from the universal POS (`upos`) "
            "for convenience or compatibility with language-specific schemes. It is often used when the original part of speech "
            "is lost due to promotion or transformation (e.g., a numeral used as a determiner)."
        ),
        values={
            "Yes": UDFeatureValue(
                code="Yes",
                label="Extended POS present",
                description="Indicates that the token has a language-specific extended POS tag stored in this field.",
            )
        },
    ),
]

# For faster lookup
UD_FEATURES_MAP = {feature.key: feature for feature in UD_FEATURES}


def normalize_ud_feature_key(key: str) -> Optional[str]:
    """
    Normalize a UD feature key to the standard key used in UD_FEATURES_MAP.
    Extend this mapping as new variants or errors are encountered.

    Args:
        key (str): The feature key to normalize (e.g., "case", "Case", "GENDER").

    Returns:
        str: The normalized UD feature key (e.g., "Case", "Gender"). `False` if unable to normalize.
    """
    key_map = {
        # Common alternate/abbreviated forms
        # Note: The key should be lowercase so lookup can be case-insensitive
        "gen": "Gender",
        "partform": "Part",
        # Add more as needed
    }
    try:
        return key_map[key.lower()]
    except KeyError:
        logger.warning(
            f"Unknown UD feature key '{key}'. Cannot normalize to UD feature key."
        )
        return None


def normalize_ud_feature_pair(key: str, value: str) -> Optional[tuple[str, str]]:
    """
    Normalize a UD feature key-value pair to the standard form used in UD_FEATURES_MAP.

    Args:
        key (str): The feature key (e.g., "Case").
        value (str): The feature value (e.g., "Nom").

    Returns:
        tuple[str, str]: The normalized key and value if valid, otherwise raises ValueError.
    """
    ud_feature_pair_remap = {
        ("Tense", "Perf"): ("Aspect", "Perf"),
        ("Tense", "Aor"): ("Tense", "Past"),
        ("Tense", "Plup"): ("Tense", "Pqp"),
        ("Degree", "Comp"): ("Degree", "Cmp"),
        # ("", ""): ("", ""),
        # Add more as needed
    }
    remap = ud_feature_pair_remap.get((key, value))
    if remap:
        norm_key, norm_value = remap
        logger.warning(f"Remapped {key}={value} to {norm_key}={norm_value}")
        return norm_key, norm_value
    logger.warning(f"Failed to normalize UD feature pair: {key}={value}.")
    return None


def get_ud_feature(key: str, value: str) -> Optional[UDFeatureTag]:
    # Get feature key with input string
    try:
        UD_FEATURE: UDFeature = UD_FEATURES_MAP[key]
    except KeyError:
        logger.warning(f"Unknown UD feature key '{key}'. Attempting to normalize.")
        normalized_feature = normalize_ud_feature_key(key=key)
        if not normalized_feature:
            # No normalization remapping was possible
            return None
        try:
            UD_FEATURE: UDFeature = UD_FEATURES_MAP[normalized_feature]
        except KeyError:
            logger.error(
                "Even with normalization, the feature key is not found; this is not expected and means that the re-mapping output is invalid."
            )
            return None
    try:
        UD_VALUE: UDFeatureValue = UD_FEATURE.values[value]
    except KeyError:
        logger.warning(
            f"Unknown UD feature value '{value}' for feature '{UD_FEATURE.key}'. Attempting to normalize key-value pair."
        )
        # Get new UDFeature since this may have been changed during remapping
        normalized_pair = normalize_ud_feature_pair(key=UD_FEATURE.key, value=value)
        if not normalized_pair:
            logger.warning(
                f"Failed to normalize UD feature pair: {UD_FEATURE.key}={value}."
            )
            return None
        normalized_feature, normalized_value = normalized_pair
        try:
            UD_FEATURE: UDFeature = UD_FEATURES_MAP[normalized_feature]
        except KeyError:
            logger.error(
                f"Unknown UD feature key '{normalized_feature}'. This is unexpected and means there is a mistake in the key of the remapped pair."
            )
            return None
        try:
            UD_VALUE: UDFeatureValue = UD_FEATURE.values[normalized_value]
        except KeyError:
            logger.error(
                f"Failed to find UD feature pair even after normalization to {UD_FEATURE.key}={value}. This is not expected and means that there is a mistake in the rammapped value."
            )
            return None
    return UDFeatureTag(
        key=UD_FEATURE.key,
        value=UD_VALUE.code,
        value_label=UD_VALUE.label,
        category=UD_FEATURE.category,
        inflectional_class=UD_FEATURE.inflectional_class,
    )


if __name__ == "__main__":
    # Use of functions in this module
    UD_FEATURE_SET: UDFeatureTagSet = UDFeatureTagSet()
    FEAT_1: Optional[UDFeatureTag] = get_ud_feature("Case", "Nom")
    if FEAT_1:
        # Use of validators in pydantic models
        UD_FEATURE_SET.add_feature(FEAT_1)
    FEAT_2: Optional[UDFeatureTag] = get_ud_feature("Gen", "Fem")
    if FEAT_2:
        # Use of validators in pydantic models
        UD_FEATURE_SET.add_feature(FEAT_2)
    print(UD_FEATURE_SET)

    # Use of validators in pydantic models
    from cltk.morphology.ud_features import UDFeatureTag, UDFeatureTagSet

    # This will succeed if "Case" and "Nom" are valid
    tag1 = UDFeatureTag(
        key="Case",
        value="Nom",
    )
    print("tag1:", tag1)
    # This will raise a ValidationError if the key or value is invalid
    try:
        tag2 = UDFeatureTag(
            key="Case",
            value="InvalidValue",
        )
    except ValueError as e:
        print(e)

    # Other examples showing the use of UDFeatureTag's own "before" validation
    print("")
    tag = UDFeatureTag(key="Case", value="Nom")
    print("tag:", tag)
    print(tag.category)  # "Inflectional"
    print(tag.inflectional_class)  # "Nominal"
    print(tag.value_label)  # "Nominative
