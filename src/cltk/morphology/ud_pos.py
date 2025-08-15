"""Universal Dependencies (UD) Part-of-Speech (POS) Tags.

https://universaldependencies.org/u/pos/index.html
"""

__license__ = "MIT License. See LICENSE."

from pydantic import BaseModel, ValidationError, field_validator, model_validator

from cltk.core.cltk_logger import logger


class UDPartOfSpeech(BaseModel):
    tag: str  # UD abbreviation, e.g., "ADJ"
    name: str  # Human-readable name
    description: str  # Official UD description
    open_class: bool  # True if open class, False if closed class


from typing import Literal, Optional

from pydantic import BaseModel


class UDPartOfSpeechTag(BaseModel):
    # Use this when instantiating a tagged word
    tag: str  # UD abbreviation, e.g., "ADJ"
    name: Optional[str] = None  # Human-readable name (auto-filled)
    open_class: Optional[
        bool
    ] = None  # True if open class, False if closed class (auto-filled)

    @field_validator("tag")
    @classmethod
    def validate_tag(cls, v):
        v = v.upper()
        if v not in UD_POS_TAGS:
            raise ValueError(f"Invalid UD POS tag: '{v}'")
        return v

    @model_validator(mode="after")
    def fill_fields(self):
        pos = UD_POS_TAGS.get(self.tag)
        if pos:
            object.__setattr__(self, "name", pos.name)
            object.__setattr__(self, "open_class", pos.open_class)
        return self

    def __str__(self):
        return f'UDPartOfSpeechTag(tag="{self.tag}", name="{self.name}")'

    def __repr__(self):
        return self.__str__()


# UD POS Registry
UD_POS_TAGS: dict[str, UDPartOfSpeech] = {
    "ADJ": UDPartOfSpeech(
        tag="ADJ",
        name="adjective",
        description="Adjectives are words that typically modify nouns and specify their properties or attributes.",
        open_class=True,
    ),
    "ADP": UDPartOfSpeech(
        tag="ADP",
        name="adposition",
        description="Adpositions are words that introduce prepositional or postpositional phrases. They typically express relationships in space or time.",
        open_class=False,
    ),
    "ADV": UDPartOfSpeech(
        tag="ADV",
        name="adverb",
        description="Adverbs modify verbs, adjectives, other adverbs, or whole clauses. They often express time, manner, place, or degree.",
        open_class=True,
    ),
    "AUX": UDPartOfSpeech(
        tag="AUX",
        name="auxiliary",
        description="Auxiliary verbs accompany the main verb and express grammatical distinctions such as tense, aspect, mood, or voice.",
        open_class=False,
    ),
    "CCONJ": UDPartOfSpeech(
        tag="CCONJ",
        name="coordinating conjunction",
        description="Coordinating conjunctions link words, phrases, or clauses that are syntactically equal.",
        open_class=False,
    ),
    "DET": UDPartOfSpeech(
        tag="DET",
        name="determiner",
        description="Determiners modify nouns and express reference, quantity, possession, etc. They include articles, demonstratives, possessives, etc.",
        open_class=False,
    ),
    "INTJ": UDPartOfSpeech(
        tag="INTJ",
        name="interjection",
        description="Interjections are words or phrases that express emotion, hesitation, or fillers. They often stand alone outside sentence structure.",
        open_class=True,
    ),
    "NOUN": UDPartOfSpeech(
        tag="NOUN",
        name="noun",
        description="Nouns are a part of speech typically denoting a person, place, thing, animal or idea.",
        open_class=True,
    ),
    "NUM": UDPartOfSpeech(
        tag="NUM",
        name="numeral",
        description="Numerals are words that express numbers or quantities.",
        open_class=False,
    ),
    "PART": UDPartOfSpeech(
        tag="PART",
        name="particle",
        description="Particles are function words that do not fit well into other categories and are often used to express grammatical relationships.",
        open_class=False,
    ),
    "PRON": UDPartOfSpeech(
        tag="PRON",
        name="pronoun",
        description="Pronouns substitute for nouns or noun phrases and often encode grammatical features such as person, number, and gender.",
        open_class=False,
    ),
    "PROPN": UDPartOfSpeech(
        tag="PROPN",
        name="proper noun",
        description="Proper nouns are names of specific people, places, organizations, etc., and are usually capitalized.",
        open_class=True,
    ),
    "PUNCT": UDPartOfSpeech(
        tag="PUNCT",
        name="punctuation",
        description="Punctuation marks are non-alphabetic symbols that structure and organize written language.",
        open_class=False,
    ),
    "SCONJ": UDPartOfSpeech(
        tag="SCONJ",
        name="subordinating conjunction",
        description="Subordinating conjunctions introduce dependent (subordinate) clauses and indicate relationships such as cause, time, or condition.",
        open_class=False,
    ),
    "SYM": UDPartOfSpeech(
        tag="SYM",
        name="symbol",
        description="Symbols are non-verbal characters used to represent concepts or quantities (e.g., currency, math, music).",
        open_class=False,
    ),
    "VERB": UDPartOfSpeech(
        tag="VERB",
        name="verb",
        description="Verbs are words that typically denote actions, processes, or states and agree with the subject in person and number.",
        open_class=True,
    ),
    "X": UDPartOfSpeech(
        tag="X",
        name="other",
        description="This category is used for words that do not fit into any other category, such as foreign words or unclassified items.",
        open_class=False,
    ),
}


def normalize_pos_tag(tag: str) -> str:
    """
    Normalize a POS tag to the standard UD tag used in UD_POS_TAGS.
    Extend this mapping as new variants or errors are encountered.

    Args:
        tag (str): The POS tag to normalize (e.g., "N", "NOUN", "v", "VERB").

    Returns:
        str: The normalized UD POS tag (e.g., "NOUN", "VERB").

    Raises:
        ValueError: If the tag cannot be normalized to a known UD POS tag.
    """
    tag_map = {
        # Common alternate/abbreviated forms
        "N": "NOUN",
        "V": "VERB",
        "PRP": "PRON",  # Sometimes used for pronoun
        "PROPN": "PROPN",
        "ADP": "ADP",
        "CC": "CCONJ",
        "SC": "SCONJ",
        # Add more as needed
    }
    tag_upper = tag.upper()
    if tag_upper in UD_POS_TAGS:
        return tag_upper
    if tag_upper in tag_map:
        return tag_map[tag_upper]
    msg: str = f"Unknown POS tag '{tag}'. Cannot normalize to UD POS tag."
    logger.warning(msg)
    raise ValueError(msg)


def is_valid_pos_tag(tag: str, normalize: bool = True) -> bool:
    """
    Check if the given tag is a valid UD part-of-speech tag.

    Args:
        tag (str): The UD POS tag to validate (e.g., "NOUN", "XYZ").

    Returns:
        bool: True if valid, False otherwise.
    """

    if not tag.upper() in UD_POS_TAGS:
        if normalize:
            try:
                tag = normalize_pos_tag(tag)
            except ValueError:
                return False
            if tag.upper() in UD_POS_TAGS:
                return True
        return False
    return True


if __name__ == "__main__":
    # # Example usage
    # print(is_valid_pos_tag("NOUN"))  # True
    # print(is_valid_pos_tag("XYZ"))  # False
    # print(is_valid_pos_tag("N", normalize=False))  # False
    # print(is_valid_pos_tag("N", normalize=True))  # True
    # print(UD_POS_TAGS["NOUN"])  # UDPartOfSpeech object for NOUN
    # print(UD_POS_TAGS["NOUN"].name)  # "noun"
    # print(
    #     UD_POS_TAGS["NOUN"].description
    # )  # "Nouns are a part of speech typically denoting a person, place, thing, animal or idea."
    # print(UD_POS_TAGS["NOUN"].tag)  # "NOUN"

    udpos: UDPartOfSpeechTag = UDPartOfSpeechTag(
        tag="NOUN",
        # name="noun",
        # open_class=True,
    )
    print(udpos)
