"""Universal Dependencies (UD) part‑of‑speech (POS) tags.

This module defines the core UD POS tag inventory and provides small, validated
data models and helpers for working with POS tags in CLTK.

References:
    - UD POS: https://universaldependencies.org/u/pos/index.html

"""

__license__ = "MIT License. See LICENSE."

from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from cltk.core.cltk_logger import logger


class UDPartOfSpeech(BaseModel):
    """Canonical UD POS definition.

    Encapsulates a single UD POS tag together with its human‑readable name,
    brief description, and whether it is considered an open or closed class in
    the UD taxonomy.

    Attributes:
        tag: Short UD tag (e.g., ``"ADJ"``, ``"NOUN"``).
        name: Human‑readable name (e.g., ``"adjective"``).
        description: Official UD description for the POS tag.
        open_class: Whether the POS is an open class (True) or closed (False).

    """

    tag: str  # UD abbreviation, e.g., "ADJ"
    name: str  # Human-readable name
    description: str  # Official UD description
    open_class: bool  # True if open class, False if closed class


class UDPartOfSpeechTag(BaseModel):
    """Concrete tag instance attached to a token.

    Validates that the provided ``tag`` is a known UD POS tag (optionally
    normalizing common variants), and fills in convenience fields like
    ``name`` and ``open_class`` from the canonical registry.

    Attributes:
        tag: UD POS tag abbreviation (e.g., ``"ADJ"``).
        name: Auto‑filled human‑readable name once validated.
        open_class: Auto‑filled open/closed class flag once validated.

    """

    # Use this when instantiating a tagged word
    tag: str  # UD abbreviation, e.g., "ADJ"
    name: Optional[str] = None  # Human-readable name (auto-filled)
    open_class: Optional[bool] = (
        None  # True if open class, False if closed class (auto-filled)
    )

    @staticmethod
    def normalize_ud_pos_tag(tag: str) -> str:
        """Normalize a POS tag to the standard UD tag used in UD_POS_TAGS.

        Handles common LLM and upstream errors, e.g., "CONJ" -> "CCONJ", "SCONJ", etc.

        Args:
            tag (str): The POS tag to normalize (e.g., "CONJ", "N", "V", "PRP").

        Returns:
            str: The normalized UD POS tag (e.g., "NOUN", "VERB").

        Raises:
            ValueError: If the tag cannot be normalized to a known UD POS tag.

        """
        # Common alternate/abbreviated forms
        tag_map = {
            "N": "NOUN",
            "V": "VERB",
            "PRP": "PRON",
            "PROPN": "PROPN",
            "CC": "CCONJ",
            "SC": "SCONJ",
            "CONJ": "CCONJ",  # LLMs often use "CONJ" for "CCONJ"
            "SUBCONJ": "SCONJ",  # Sometimes "SUBCONJ" for "SCONJ"
            "PREP": "ADP",
            "ADJECTIVE": "ADJ",
            # "": "",
        }
        tag_upper = tag.upper().strip()
        if tag_upper in UD_POS_TAGS:
            return tag_upper
        if tag_upper in tag_map:
            return tag_map[tag_upper]
        msg: str = f"Unknown POS tag '{tag}'. Cannot normalize to UD POS tag."
        logger.warning(msg)
        raise ValueError(msg)

    @field_validator("tag")
    @classmethod
    def validate_tag(cls, v: str) -> str:
        """Normalize and validate the UD POS ``tag``.

        Converts common alternates (e.g., ``"CONJ"`` → ``"CCONJ"``) and ensures
        the final value appears in the ``UD_POS_TAGS`` registry.

        Args:
            v: Candidate POS tag value.

        Raises:
            ValueError: If the tag cannot be normalized to a known UD POS tag.

        Returns:
            The validated and normalized POS tag.

        """
        v = v.upper()
        if v not in UD_POS_TAGS:
            logger.info(f"Normalizing UD POS tag: '{v}' ...")
            v = cls.normalize_ud_pos_tag(v)
            if v not in UD_POS_TAGS:
                msg: str = f"Failed to normalize UD POS tag: '{v}'"
                logger.error(msg)
                raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def fill_fields(self) -> "UDPartOfSpeechTag":
        """Populate derived fields from the canonical registry.

        After a successful tag validation, look up the canonical entry in
        ``UD_POS_TAGS`` and set ``name`` and ``open_class`` accordingly.

        Returns:
            The model instance with enriched fields.

        """
        pos = UD_POS_TAGS.get(self.tag)
        if pos:
            object.__setattr__(self, "name", pos.name)
            object.__setattr__(self, "open_class", pos.open_class)
        return self

    def __str__(self) -> str:
        """Return a concise, human‑readable representation of the tag."""
        return f'UDPartOfSpeechTag(tag="{self.tag}", name="{self.name}")'

    def __repr__(self) -> str:
        """Alias for ``__str__`` to aid debugging and logging."""
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


# def normalize_pos_tag(tag: str) -> str:
#     """
#     Normalize a POS tag to the standard UD tag used in UD_POS_TAGS.
#     Extend this mapping as new variants or errors are encountered.

#     Args:
#         tag (str): The POS tag to normalize (e.g., "N", "NOUN", "v", "VERB").

#     Returns:
#         str: The normalized UD POS tag (e.g., "NOUN", "VERB").

#     Raises:
#         ValueError: If the tag cannot be normalized to a known UD POS tag.
#     """
#     tag_map = {
#         # Common alternate/abbreviated forms
#         "N": "NOUN",
#         "V": "VERB",
#         "PRP": "PRON",  # Sometimes used for pronoun
#         "PROPN": "PROPN",
#         "ADP": "ADP",
#         "CC": "CCONJ",
#         "SC": "SCONJ",
#         # Add more as needed
#     }
#     tag_upper = tag.upper()
#     if tag_upper in UD_POS_TAGS:
#         return tag_upper
#     if tag_upper in tag_map:
#         return tag_map[tag_upper]
#     msg: str = f"Unknown POS tag '{tag}'. Cannot normalize to UD POS tag."
#     logger.warning(msg)
#     raise ValueError(msg)


# def is_valid_pos_tag(tag: str, normalize: bool = True) -> bool:
#     """
#     Check if the given tag is a valid UD part-of-speech tag.

#     Args:
#         tag (str): The UD POS tag to validate (e.g., "NOUN", "XYZ").

#     Returns:
#         bool: True if valid, False otherwise.
#     """

#     if not tag.upper() in UD_POS_TAGS:
#         if normalize:
#             try:
#                 tag = normalize_pos_tag(tag)
#             except ValueError:
#                 return False
#             if tag.upper() in UD_POS_TAGS:
#                 return True
#         return False
#     return True


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
