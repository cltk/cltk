"""UD features unique to Latin treebanks.

https://github.com/UniversalDependencies/docs/tree/pages-source/_la/feat

"""

from cltk.core.data_types import UDFeature, UDFeatureValue

UD_FEATURES_LAT: list[UDFeature] = [
    UDFeature(
        key="InflClass",
        category="Inflectional",
        description=(
            "InflClass identifies the inflectional (declension/conjugation) class of a Latin lemma/form. "
            "UD Latin uses Indo-European stem-class-inspired labels (prefixed IndEur) for declensions, "
            "and Lat* labels for conjugations and Latin-confined patterns. "
            "Some Greek-inherited classes are mapped onto existing values and may be additionally marked "
            "with Variant=Greek in annotation practice."
        ),
        values={
            # --- Nominal declension classes ---
            "IndEurA": UDFeatureValue(
                code="IndEurA",
                label="First declension (-a stems)",
                description=(
                    "Nominal inflection class originating from stems terminating in -a. "
                    "Mostly feminine; includes a subset of masculine nouns. "
                    "First-class adjectives (incl. perfect/future participles, gerundives) follow it in the feminine; "
                    "superlatives follow it in the feminine."
                ),
                inflectional_class="Nominal",
            ),
            "IndEurO": UDFeatureValue(
                code="IndEurO",
                label="Second declension (-o/-e stems)",
                description=(
                    "Nominal inflection class originating from stems terminating in -e/o. "
                    "Mostly masculine and neuter; includes some feminine nouns in -us (often tree names). "
                    "First-class adjectives (incl. perfect/future participles, gerundives/gerunds) follow it in the masculine/neuter; "
                    "superlatives follow it in the masculine/neuter."
                ),
                inflectional_class="Nominal",
            ),
            "IndEurX": UDFeatureValue(
                code="IndEurX",
                label="Third declension (consonant stems)",
                description=(
                    "Nominal inflection class originating from athematic consonant-final stems. "
                    "All genders represented. Mostly nouns and comparative forms, with a few second-class adjectives."
                ),
                inflectional_class="Nominal",
            ),
            "IndEurI": UDFeatureValue(
                code="IndEurI",
                label="Third declension (i-stems)",
                description=(
                    "Nominal inflection class originating from stems terminating in -i. "
                    "All genders represented. Covers nearly all second-class adjectives (including present participles), "
                    "and also some determiners and numerals."
                ),
                inflectional_class="Nominal",
            ),
            "IndEurU": UDFeatureValue(
                code="IndEurU",
                label="Fourth declension (-u stems)",
                description=(
                    "Nominal inflection class originating from stems terminating in -u. "
                    "Mostly masculine; includes some feminine nouns in -us and neuter nouns in -u. "
                    "Mostly nouns and the supine."
                ),
                inflectional_class="Nominal",
            ),
            "IndEurE": UDFeatureValue(
                code="IndEurE",
                label="Fifth declension (-e stems)",
                description=(
                    "Nominal inflection class originating from stems terminating in -e. "
                    "Mostly restricted to feminine nouns."
                ),
                inflectional_class="Nominal",
            ),
            "LatPron": UDFeatureValue(
                code="LatPron",
                label="Pronominal declension",
                description=(
                    "Pronominal/determiner declension class (non-personal pronouns and many determiners). "
                    "Similar to the first/second-declension adjective alternation but deviates notably: "
                    "(i) singular genitive and dative are characteristically identical across genders; "
                    "(ii) neuter sg nom/acc ends in -d; "
                    "(iii) masculine sg nominative may lack -s. "
                    "Some forms also occur with clitic-like suffixes that add semantic/pragmatic nuances."
                ),
                inflectional_class="Nominal",
            ),
            # --- Verbal conjugation classes ---
            "LatA": UDFeatureValue(
                code="LatA",
                label="First conjugation (thematic -a-)",
                description=(
                    "Verbal inflection class with thematic vowel -a- (from convergence of different verbal stems)."
                ),
                inflectional_class="Verbal",
            ),
            "LatE": UDFeatureValue(
                code="LatE",
                label="Second conjugation (thematic -e-)",
                description=(
                    "Verbal inflection class with thematic vowel -e- (from convergence of different verbal stems)."
                ),
                inflectional_class="Verbal",
            ),
            "LatX": UDFeatureValue(
                code="LatX",
                label="Third conjugation (athematic / short-i stems)",
                description=(
                    "Verbal inflection class for (supposedly) athematic stems (sometimes analyzed as short-ĭ stems)."
                ),
                inflectional_class="Verbal",
            ),
            "LatI": UDFeatureValue(
                code="LatI",
                label="Fourth conjugation (thematic -i-)",
                description=(
                    "Verbal inflection class with thematic vowel -i- (from convergence of different verbal stems)."
                ),
                inflectional_class="Verbal",
            ),
            "LatI2": UDFeatureValue(
                code="LatI2",
                label='Mixed conjugation ("fifth" conjugation)',
                description=(
                    'Mixed ("fifth") conjugation historically arising from the fourth conjugation on rhythmic grounds; '
                    "differs from LatI only in a small set of forms (e.g., capio-type)."
                ),
                inflectional_class="Verbal",
            ),
            # --- Irregular / special ---
            "LatAnom": UDFeatureValue(
                code="LatAnom",
                label="Anomalous / irregular inflection",
                description=(
                    "Irregular patterns (especially some verbs and personal pronouns) whose paradigms cannot be fully "
                    "reduced to other classes; labeled anomalous (uerbum anomalum). "
                    "UD Latin notes there are no anomalous nouns/adjectives/determiners under this definition."
                ),
                inflectional_class=None,
            ),
            "Ind": UDFeatureValue(
                code="Ind",
                label="Indeclinable (deprecated)",
                description=(
                    "Indeclinable member of a POS class that normally inflects (e.g., loanwords; infinitives as verbal nouns). "
                    "This value is deprecated in UD Latin: it represents absence of an inflectional class and should typically "
                    "be left unannotated rather than marked as InflClass=Ind."
                ),
                inflectional_class=None,
            ),
        },
    ),
    UDFeature(
        key="Compound",
        category="Lexical",
        description=(
            "This is a binary (yes/no) morphological feature that is only annotated when its value is Yes."
        ),
        values={
            "Yes": UDFeatureValue(
                code="Yes",
                label="Yes",
                description="Univerbation of two or more words. When two or more otherwise independent words (i.e. not considering clitics or bound morphemes) have become fused and crystallised into a single word that is no more the “sum of its parts”, and this word is set down as such in writing, the corresponding token is marked with Compound=Yes.",
                inflectional_class=None,
            ),
        },
    ),
    UDFeature(
        key="Form",
        category="Lexical",
        description=(
            "Form is a Latin-specific morphological feature used to mark certain emphatic or expanded word forms. "
            "It is only annotated when it has a non-empty value."
        ),
        values={
            "Emp": UDFeatureValue(
                code="Emp",
                label="Emphatic",
                description=(
                    "Emphatic form of a word: a token appears in an expanded/emphatic form with respect to a more basic form, "
                    "or incorporates common emphatic elements and can no longer be analyzed as a compound (if it ever was). "
                    "Examples include enim (vs. nam), equidem (vs. quidem), ecce (presentative particle with -ce), "
                    "namque (vs. nam), and possessives with -pte (e.g., meopte)."
                ),
                inflectional_class=None,
            ),
        },
    ),
    UDFeature(
        key="NumValue",
        category="Lexical",
        description=(
            "NumValue is a Latin-specific feature used to mark a small set of determiners/pronominal-like forms "
            "that imply a specific cardinality but are not treated as numerals. "
            "UD Latin restricts this feature to the lowest values 1 and 2."
        ),
        values={
            "1": UDFeatureValue(
                code="1",
                label="Numeric value 1",
                description=(
                    "Marks determiners/pronominal-like forms implying the numeric value 1 (e.g., unus ‘one; a(n)’). "
                    "In UD Latin this is used for ambivalent ‘one/a(n)’ items that often follow the pronominal inflectional paradigm."
                ),
                inflectional_class=None,
            ),
            "2": UDFeatureValue(
                code="2",
                label="Numeric value 2",
                description=(
                    "Marks determiners/pronominal-like forms implying the numeric value 2 (e.g., ambo ‘both’)."
                ),
                inflectional_class=None,
            ),
        },
    ),
]
