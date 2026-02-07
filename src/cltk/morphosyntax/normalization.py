"""Normalization of text for morphosyntactic analysis."""

from typing import Optional

from cltk.core.cltk_logger import logger
from cltk.core.data_types import UDFeatureTag, UDFeatureTagSet


# TODO: Remove this? Not called anymore
def normalize_ud_feature_key(key: str) -> Optional[str]:
    """Normalize a UD feature key to the canonical form in ``UD_FEATURES_MAP``.

    Extend this mapping as new variants or upstream errors are encountered.

    Args:
        key: Feature key to normalize (e.g., "case", "Case", "GENDER").

    Returns:
        The normalized UD feature key (e.g., "Case", "Gender"), or ``None`` if
        it cannot be normalized.

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
    """Normalize a feature ``(key, value)`` to canonical UD form.

    Args:
        key: The feature key (e.g., "Case").
        value: The feature value (e.g., "Nom").

    Returns:
        The normalized ``(key, value)`` pair if a mapping is known; otherwise
        ``None``.

    """
    ud_feature_pair_remap: dict[tuple[str, str], tuple[str, str]] = {
        ("Tense", "Perf"): ("Aspect", "Perf"),
        ("Tense", "Aor"): ("Tense", "Past"),
        ("Tense", "Plup"): ("Tense", "Pqp"),
        ("Degree", "Comp"): ("Degree", "Cmp"),
        ("Aspect", "Aor"): ("Tense", "Past"),
        ("Aspect", "Pres"): ("Tense", "Pres"),
        ("Aspect", "Fut"): ("Tense", "Fut"),
        ("Mood", "Fut"): ("Tense", "Fut"),
        ("Emph", "Yes"): ("PronType", "Emp"),
        ("Emphatic", "Yes"): ("PronType", "Emp"),
        ("Indef", "Yes"): ("PronType", "Indef"),
        ("Demonstrative", "Yes"): ("PronType", "Dem"),
        ("Indefinite", "Yes"): ("PronType", "Ind"),
        ("Participle", "Yes"): ("VerbForm", "Part"),
        ("PartForm", "Pres"): ("Tense", "Pres"),
        ("Partic", "Yes"): ("VerbForm", "Part"),
        ("Tense", "Present"): ("Tense", "Pres"),
        ("Definite", "Yes"): ("Definite", "Def"),
        ("Mood", "Inf"): ("VerbForm", "Inf"),
        ("Mood", "Indicative"): ("Mood", "Ind"),
        ("Mood", "Indic"): ("Mood", "Ind"),
        ("Number", "Pl"): ("Number", "Plur"),
        ("Voice", "Medium"): ("Voice", "Mid"),  # double check this
        ("Voice", "Active"): ("Voice", "Act"),  # double check this
        ("Voice", "Passive"): ("Voice", "Pass"),  # double check this
        ("Tense", "Aorist"): ("Tense", "Past"),
        ("Tense", "Future"): ("Tense", "Fut"),
        ("Tense", "Imperfect"): ("Tense", "Imp"),
        ("Tense", "Imperf"): ("Tense", "Imp"),
        ("Tense", "Impft"): ("Tense", "Imp"),
        ("Tense", "Impft."): ("Tense", "Imp"),
        ("Degree", "Positive"): ("Degree", "Pos"),
        ("Rel", "Yes"): ("PronType", "Rel"),
        ("Gender", "Mas"): ("Gender", "Masc"),
        ("Gender", "Mas."): ("Gender", "Masc"),
        ("Gender", "Neuter"): ("Gender", "Neut"),
        ("Def", "Def"): ("Definite", "Def"),
        ("Definiteness", "Def"): ("Definite", "Def"),
        ("Definiteness", "Ind"): ("Definite", "Ind"),
        ("Voice", "Middle"): ("Voice", "Mid"),
        ("Voice", "Med"): ("Voice", "Mid"),
        ("Reflexive", "Yes"): ("Reflex", "Yes"),
        ("Mood", "Pres"): ("Tense", "Pres"),
        ("Mood", "Participle"): ("VerbForm", "Part"),
        ("Mood", "Part"): ("VerbForm", "Part"),
        ("Degree", "Superlative"): ("Degree", "Sup"),
        ("Case", "Accusative"): ("Case", "Acc"),
        ("Mood", "Subj"): ("Mood", "Sub"),
        ("Aspect", "Perfect"): ("Aspect", "Perf"),
        ("Mood", "Perf"): ("Aspect", "Perf"),
        ("PronType", "Pron"): ("PronType", ""),
        ("Degree", "Comparative"): ("Degree", "Cmp"),
        ("Vocative", "Yes"): ("Case", "Voc"),
        # Added for Old Norse (tags used in old PROIEL)
        # Mappings from legacy SubPOS → UD (FEATS or UPOS)
        # Degree (adjectives/adverbs)
        # ("SubPOS", "Pos."): ("Degree", "Pos"),
        # ("SubPOS", "Comp."): ("Degree", "Cmp"),
        # ("SubPOS", "Sup."): ("Degree", "Sup"),
        # ("SubPOS", "Prf."): ("Degree", "Abs"),  # absolute superlative
        # Pronouns / determiners
        ("SubPOS", "Dem."): ("PronType", "Dem"),
        ("SubPOS", "Int."): ("PronType", "Int"),
        ("SubPOS", "Rel."): ("PronType", "Rel"),
        ("SubPOS", "Rel"): ("PronType", "Rel"),
        ("SubPOS", "Ind."): ("PronType", "Ind"),
        ("SubPOS", "Pers."): ("PronType", "Prs"),
        ("SubPOS", "Refl."): ("Reflex", "Yes"),
        ("SubPOS", "Poss."): ("Poss", "Yes"),
        # # Verbs
        # ("SubPOS", "Fin."): ("VerbForm", "Fin"),
        # ("SubPOS", "Inf."): ("VerbForm", "Inf"),
        # ("SubPOS", "Part."): ("VerbForm", "Part"),
        # ("SubPOS", "Ger."): ("VerbForm", "Ger"),
        # ("SubPOS", "Sup."): ("VerbForm", "Sup"),
        # Nouns
        # TODO: Map via UPOS, which is part of UD but not a FEAT)
        # ("SubPOS", "Com."): ("UPOS", "NOUN"),
        # ("SubPOS", "Prop."): ("UPOS", "PROPN"),
        # ("SubPOS", "Abstr."): ("UPOS", "NOUN"),
        # Adpositions / conjunctions / particles
        ("SubPOS", "Prep."): ("AdpType", "Prep"),
        ("SubPOS", "Post."): ("AdpType", "Post"),
        # ("SubPOS", "Conj."): ("UPOS", "CCONJ"),
        # ("SubPOS", "Sub."): ("UPOS", "SCONJ"),
        # ("SubPOS", "Part."): ("UPOS", "PART"),
        # Other
        # ("SubPOS", "Num."): ("UPOS", "NUM"),
        ("SubPOS", "Abbr."): ("Abbr", "Yes"),
        ("SubPOS", "Foreign."): ("Foreign", "Yes"),
        ("AdvType", "Place"): ("AdvType", "Loc"),
        # Normalization of tags used in Sanskrit Dependency Treebank (SDT)
        # --- UPOS (legacy POS → UD UPOS) ---
        ("POS", "N"): ("UPOS", "NOUN"),
        ("POS", "PROPN"): ("UPOS", "PROPN"),
        ("POS", "PRO"): ("UPOS", "PRON"),
        ("POS", "PRON"): ("UPOS", "PRON"),
        ("POS", "ADJ"): ("UPOS", "ADJ"),
        ("POS", "ADV"): ("UPOS", "ADV"),
        ("POS", "V"): ("UPOS", "VERB"),
        ("POS", "AUX"): ("UPOS", "AUX"),
        ("POS", "NUM"): ("UPOS", "NUM"),
        ("POS", "DET"): ("UPOS", "DET"),
        ("POS", "ADP"): ("UPOS", "ADP"),
        ("POS", "POST"): ("UPOS", "ADP"),  # postposition
        ("POS", "PREP"): ("UPOS", "ADP"),  # preposition (rare in Sanskrit)
        ("POS", "CCONJ"): ("UPOS", "CCONJ"),
        ("POS", "CONJ"): ("UPOS", "CCONJ"),
        ("POS", "SCONJ"): ("UPOS", "SCONJ"),
        ("POS", "PART"): ("UPOS", "PART"),
        ("POS", "INTJ"): ("UPOS", "INTJ"),
        ("POS", "PUNCT"): ("UPOS", "PUNCT"),
        ("POS", "SYM"): ("UPOS", "SYM"),
        ("POS", "X"): ("UPOS", "X"),
        # --- Case (legacy → UD) ---
        ("Case", "NOM"): ("Case", "Nom"),
        ("Case", "ACC"): ("Case", "Acc"),
        ("Case", "DAT"): ("Case", "Dat"),
        ("Case", "GEN"): ("Case", "Gen"),
        ("Case", "LOC"): ("Case", "Loc"),
        ("Case", "INS"): ("Case", "Ins"),
        ("Case", "ABL"): ("Case", "Abl"),
        ("Case", "VOC"): ("Case", "Voc"),
        # Numeric case codes used by some Sanskrit taggers (1–8)
        ("Case", "1"): ("Case", "Nom"),
        ("Case", "2"): ("Case", "Acc"),
        ("Case", "3"): ("Case", "Ins"),
        ("Case", "4"): ("Case", "Dat"),
        ("Case", "5"): ("Case", "Abl"),
        ("Case", "6"): ("Case", "Gen"),
        ("Case", "7"): ("Case", "Loc"),
        ("Case", "8"): ("Case", "Voc"),
        # --- Number (legacy → UD) ---
        ("Number", "SG"): ("Number", "Sing"),
        ("Number", "DU"): ("Number", "Dual"),
        ("Number", "Sg"): ("Number", "Sing"),
        ("Number", "Du"): ("Number", "Dual"),
        # --- Gender (legacy → UD) ---
        ("Gender", "M"): ("Gender", "Masc"),
        ("Gender", "F"): ("Gender", "Fem"),
        ("Gender", "N"): ("Gender", "Neut"),
        ("Gender", "m"): ("Gender", "Masc"),
        ("Gender", "f"): ("Gender", "Fem"),
        ("Gender", "n"): ("Gender", "Neut"),
        # --- Person (legacy → UD) ---
        ("Person", "1"): ("Person", "1"),
        ("Person", "2"): ("Person", "2"),
        ("Person", "3"): ("Person", "3"),
        # --- Degree (ADJ/ADV) ---
        ("Degree", "POS"): ("Degree", "Pos"),
        ("Degree", "COMP"): ("Degree", "Cmp"),
        ("Degree", "SUPER"): ("Degree", "Sup"),
        ("Degree", "ABS"): (
            "Degree",
            "Abs",
        ),  # "absolute" superlative (if present in your source)
        # --- Polarity ---
        ("Polarity", "NEG"): ("Polarity", "Neg"),
        ("Polarity", "POS"): ("Polarity", "Pos"),
        # --- Pronouns / determiners ---
        ("PronType", "DEM"): ("PronType", "Dem"),
        ("PronType", "REL"): ("PronType", "Rel"),
        ("PronType", "INT"): ("PronType", "Int"),
        ("PronType", "INDF"): ("PronType", "Ind"),
        ("PronType", "PRS"): ("PronType", "Prs"),
        ("PronType", "NEG"): ("PronType", "Neg"),
        ("PronType", "TOT"): ("PronType", "Tot"),
        ("Reflex", "REFL"): ("Reflex", "Yes"),
        ("Poss", "POSS"): ("Poss", "Yes"),
        # --- Numerals ---
        ("NumType", "CARD"): ("NumType", "Card"),
        ("NumType", "ORD"): ("NumType", "Ord"),
        ("NumType", "FRAC"): ("NumType", "Frac"),
        ("NumType", "DIST"): ("NumType", "Dist"),
        ("NumType", "MULT"): ("NumType", "Mult"),
        ("NumType", "SETS"): ("NumType", "Sets"),
        # --- Adpositions ---
        ("AdpType", "POST"): ("AdpType", "Post"),
        ("AdpType", "PREP"): ("AdpType", "Prep"),
        # --- Adverbs (semantic type) ---
        ("AdvType", "Time"): ("AdvType", "Tim"),
        ("AdvType", "Manner"): ("AdvType", "Man"),
        ("AdvType", "Degree"): ("AdvType", "Deg"),
        ("AdvType", "Cause"): ("AdvType", "Cau"),
        ("AdvType", "Freq"): ("AdvType", "Freq"),
        ("AdvType", "Mod"): ("AdvType", "Mod"),
        # --- Tense (legacy → UD) ---
        ("Tense", "PRES"): ("Tense", "Pres"),
        ("Tense", "PR"): ("Tense", "Pres"),
        ("Tense", "PRS"): ("Tense", "Pres"),
        ("Tense", "FUT"): ("Tense", "Fut"),
        # Past categories in legacy Sanskrit tagsets
        # Imperfect (IMPF) → simple Past in UD
        ("Tense", "IMPF"): ("Tense", "Past"),
        ("Tense", "IMPERF"): ("Tense", "Past"),
        # Aorist / Perfect often annotated with Aspect=Perf in UD Sanskrit
        ("Tense", "AOR"): (
            "Tense",
            "Past",
        ),  # (optionally add Aspect=Perf in your pipeline)
        ("Tense", "PERF"): ("Tense", "Past"),  # (optionally add Aspect=Perf)
        # --- Aspect (when present) ---
        ("Aspect", "PERF"): ("Aspect", "Perf"),
        ("Aspect", "IPFV"): ("Aspect", "Imp"),
        # --- Mood (legacy → UD) ---
        ("Mood", "IND"): ("Mood", "Ind"),
        ("Mood", "IMP"): ("Mood", "Imp"),
        ("Mood", "JUS"): ("Mood", "Jus"),
        ("Mood", "OPT"): ("Mood", "Opt"),
        # Less common legacy moods; map to nearest UD value
        ("Mood", "SBJV"): (
            "Mood",
            "Sub",
        ),  # Vedic subjunctive (UD allows Sub universally)
        ("Mood", "COND"): ("Mood", "Cnd"),  # conditional (rare; UD allows Cnd)
        ("Mood", "BEN"): (
            "Mood",
            "Jus",
        ),  # benedictive/precative → closest UD value is Jussive
        ("Mood", "INJ"): (
            "Mood",
            "Ind",
        ),  # injunctive → treated as indicative in UD Sanskrit
        # --- Voice (legacy → UD) ---
        ("Voice", "ACT"): ("Voice", "Act"),  # parasmaipada
        ("Voice", "MID"): ("Voice", "Mid"),  # ātmanepada
        ("Voice", "PASS"): ("Voice", "Pass"),
        ("Voice", "CAUS"): (
            "Voice",
            "Caus",
        ),  # UD Sanskrit admits Caus as a voice value
        # --- VerbForm / non-finites (legacy → UD) ---
        ("VerbForm", "FIN"): ("VerbForm", "Fin"),
        ("VerbForm", "INF"): ("VerbForm", "Inf"),
        # Absolutive / “gerund” (ktvā/lyap): normalize to UD Conv
        ("VerbForm", "GER"): ("VerbForm", "Conv"),
        ("VerbForm", "ABS"): ("VerbForm", "Conv"),
        ("VerbForm", "CONV"): ("VerbForm", "Conv"),
        # Participles (map to UD Part + tense/voice if available upstream)
        ("VerbForm", "PART"): ("VerbForm", "Part"),
        ("PartType", "PAP"): (
            "VerbForm",
            "Part",
        ),  # Present Active Part. → add Tense=Pres|Voice=Act
        ("PartType", "PMP"): (
            "VerbForm",
            "Part",
        ),  # Present Middle Part. → add Tense=Pres|Voice=Mid
        ("PartType", "PPP"): (
            "VerbForm",
            "Part",
        ),  # Past Passive Part.  → add Tense=Past|Voice=Pass
        ("PartType", "FAP"): (
            "VerbForm",
            "Part",
        ),  # Future Active Part. → add Tense=Fut|Voice=Act
        ("PartType", "FMP"): (
            "VerbForm",
            "Part",
        ),  # Future Middle Part. → add Tense=Fut|Voice=Mid
        ("PartType", "PFP"): (
            "VerbForm",
            "Part",
        ),  # Gerundive → add Tense=Fut|Voice=Pass
        # Periphrastic future participle (bhavitā etc.)—treated as Part
        ("PartType", "PERIPH_FUT"): ("VerbForm", "Part"),
        # --- Definiteness (for borrowed/article-like usages; rare in Sanskrit) ---
        ("Definiteness", "DEF"): ("Definiteness", "Def"),
        ("Definiteness", "IND"): ("Definiteness", "Ind"),
        # --- Foreign / Abbreviation (if present) ---
        ("Foreign", "Y"): ("Foreign", "Yes"),
        ("Abbr", "Y"): ("Abbr", "Yes"),
        # Many legacy Indo-Aryan tagsets use conjunctive participle for Sanskrit/Pāli absolutives (ktvā / -ya)
        ("PartType", "Conj."): ("VerbForm", "Conv"),
        # Most taggers meant "personal" here.
        ("PronType", "Part"): ("PronType", "Prs"),
        # 2) ParticleType=Clitic → UD has no ParticleType feature.
        #    Best practice: mark cliticness with a dedicated feature key if your schema allows it.
        #    Many validators accept Clitic=Yes. If yours does not, drop to MISC.
        # ("ParticleType", "Clitic"): ("Clitic", "Yes"),
        # 3) PartType=Prt → 'Prt' isn’t a UD value. If the goal is just “this is a particle”,
        #    capture it via UPOS (PART) and drop the feature.
        # ("PartType", "Prt"): ("UPOS", "PART"),
        # 4) Polarity=Aff → UD uses Pos/Neg, not Aff.
        ("Polarity", "Aff"): ("Polarity", "Pos"),
        # 5) ConjType=Coord → coordination/subordination is encoded in UPOS, not ConjType.
        # ("ConjType", "Coord"): ("UPOS", "CCONJ"),
        ("VerbForm", "Opt"): ("Mood", "Opt"),
        ("VerbForm", "Imp"): ("Mood", "Imp"),
        # ("PronType", "Proper"): ("UPOS", "PROPN"),
        # Conjunction subtype → UPOS (UD encodes sub/coord at UPOS level)
        # ("ConjType", "Sub"):  ("UPOS", "SCONJ"),
        # Preposition subtype → UPOS (if your validator flags AdpType, drop it)
        # ("AdpType", "Prep"): ("UPOS", "ADP"),
        # TODO: Consider post-rules for things like this and also to change/add UPOS
        # Note (recommended): In UD, Optative and Imperative are moods on a finite verb. After applying the above mappings, if a token has Mood ∈ {Opt,Imp} and no VerbForm, set:
        # post‑rule:
        # if "Mood" in {"Opt","Imp"} and not has_feature("VerbForm"):
        #     add_feature(("VerbForm","Fin"))
        # ("", ""): ("", ""),
    }
    remap: Optional[tuple[str, str]] = ud_feature_pair_remap.get((key, value))
    if remap:
        norm_key, norm_value = remap
        logger.info(f"Remapped {key}={value} to {norm_key}={norm_value}")
        return norm_key, norm_value
    logger.warning(f"Failed to normalize UD feature pair: {key}={value}.")
    return None


def convert_pos_features_to_ud(feats_raw: str) -> Optional[UDFeatureTagSet]:
    """Parse a raw feature string into a validated ``UDFeatureTagSet``.

    The input is expected in the common CoNLL‑U style, e.g.,
    ``"Case=Nom|Number=Sing|Gender=Masc"``. Unknown or unmappable pairs are
    skipped with a warning.

    Args:
        feats_raw: Raw feature string containing ``key=value`` pairs separated by
            ``|``.

    Returns:
        A ``UDFeatureTagSet`` containing validated features (possibly empty).

    """
    features_tag_set = UDFeatureTagSet()
    raw_features_pairs: list[tuple[str, str]] = [
        tup
        for tup in (
            tuple(pair.split("=", maxsplit=1))
            for pair in feats_raw.split("|")
            if "=" in pair
        )
        if len(tup) == 2
    ]
    logger.debug(f"raw_features_pairs: {raw_features_pairs}")
    for raw_feature_key, raw_feature_value in raw_features_pairs:
        try:
            feature_tag = UDFeatureTag(
                key=raw_feature_key,
                value=raw_feature_value,
            )
            features_tag_set.features.append(feature_tag)
            logger.debug(f"feature_tag: {feature_tag}")
        except ValueError as e:
            logger.warning(
                f"Skipping invalid feature: {raw_feature_key}={raw_feature_value} ({e})"
            )
            continue  # Skip this feature and move on
    return features_tag_set
