"""Universal Dependencies (UD) Dependency Relations (DepRel).

https://universaldependencies.org/u/dep/index.html
"""

from typing import Optional

from pydantic import BaseModel, field_validator

from cltk.core.cltk_logger import logger


class UDDeprel(BaseModel):
    code: str  # e.g., "nsubj"
    name: str  # Human-readable name, e.g., "nominal subject"
    description: str  # Official UD description
    is_obsolete: Optional[bool] = False


class UDDeprelTag(BaseModel):
    code: str  # e.g., "nsubj"
    name: str  # Human-readable name

    @field_validator("code")
    @classmethod
    def validate_code(cls, v):
        if v not in UD_DEPRELS:
            raise ValueError(f"Invalid UD DepRel code: '{v}'")
        return v

    def __str__(self):
        return f'UDDeprelTag(code="{self.code}", name="{self.name}")'

    def __repr__(self):
        return self.__str__()


# Official UD dependency relations (core set, see UD docs for full list)
UD_DEPRELS: dict[str, UDDeprel] = {
    "acl": UDDeprel(
        code="acl",
        name="clausal modifier of noun",
        description="Clausal modifier of noun (adnominal clause).",
    ),
    "advcl": UDDeprel(
        code="advcl",
        name="adverbial clause modifier",
        description="Adverbial clause modifier.",
    ),
    "advmod": UDDeprel(
        code="advmod", name="adverbial modifier", description="Adverbial modifier."
    ),
    "amod": UDDeprel(
        code="amod", name="adjectival modifier", description="Adjectival modifier."
    ),
    "appos": UDDeprel(
        code="appos", name="appositional modifier", description="Appositional modifier."
    ),
    "aux": UDDeprel(code="aux", name="auxiliary", description="Auxiliary."),
    "case": UDDeprel(code="case", name="case marking", description="Case marking."),
    "cc": UDDeprel(
        code="cc",
        name="coordinating conjunction",
        description="Coordinating conjunction.",
    ),
    "ccomp": UDDeprel(
        code="ccomp",
        name="clausal complement",
        description="Clausal complement with internal subject.",
    ),
    "clf": UDDeprel(code="clf", name="classifier", description="Classifier."),
    "compound": UDDeprel(code="compound", name="compound", description="Compound."),
    "conj": UDDeprel(code="conj", name="conjunct", description="Conjunct."),
    "cop": UDDeprel(code="cop", name="copula", description="Copula."),
    "csubj": UDDeprel(
        code="csubj", name="clausal subject", description="Clausal subject."
    ),
    "dep": UDDeprel(
        code="dep", name="unspecified dependency", description="Unspecified dependency."
    ),
    "det": UDDeprel(code="det", name="determiner", description="Determiner."),
    "discourse": UDDeprel(
        code="discourse", name="discourse element", description="Discourse element."
    ),
    "dislocated": UDDeprel(
        code="dislocated",
        name="dislocated elements",
        description="Dislocated elements.",
    ),
    "expl": UDDeprel(code="expl", name="expletive", description="Expletive."),
    "fixed": UDDeprel(
        code="fixed",
        name="fixed multiword expression",
        description="Fixed multiword expression.",
    ),
    "flat": UDDeprel(
        code="flat",
        name="flat multiword expression",
        description="Flat multiword expression.",
    ),
    "goeswith": UDDeprel(code="goeswith", name="goes with", description="Goes with."),
    "iobj": UDDeprel(
        code="iobj", name="indirect object", description="Indirect object."
    ),
    "list": UDDeprel(code="list", name="list", description="List."),
    "mark": UDDeprel(code="mark", name="marker", description="Marker."),
    "nmod": UDDeprel(
        code="nmod", name="nominal modifier", description="Nominal modifier."
    ),
    "nsubj": UDDeprel(
        code="nsubj", name="nominal subject", description="Nominal subject."
    ),
    "nummod": UDDeprel(
        code="nummod", name="numeric modifier", description="Numeric modifier."
    ),
    "obj": UDDeprel(code="obj", name="object", description="Object."),
    "obl": UDDeprel(code="obl", name="oblique nominal", description="Oblique nominal."),
    "orphan": UDDeprel(code="orphan", name="orphan", description="Orphan."),
    "parataxis": UDDeprel(code="parataxis", name="parataxis", description="Parataxis."),
    "punct": UDDeprel(code="punct", name="punctuation", description="Punctuation."),
    "reparandum": UDDeprel(
        code="reparandum",
        name="overridden disfluency",
        description="Overridden disfluency.",
    ),
    "root": UDDeprel(code="root", name="root", description="Root."),
    "vocative": UDDeprel(code="vocative", name="vocative", description="Vocative."),
    "xcomp": UDDeprel(
        code="xcomp",
        name="open clausal complement",
        description="Open clausal complement.",
    ),
    # Add more as needed from the UD documentation
}


def is_valid_deprel(code: str) -> bool:
    """Check if the given code is a valid UD dependency relation."""
    return code in UD_DEPRELS


def get_ud_deprel_tag(code: str) -> Optional[UDDeprelTag]:
    """Return a UDDeprelTag for the given code, or None if not found."""
    deprel = UD_DEPRELS.get(code)
    if not deprel:
        logger.warning(f"Unknown UD DepRel code '{code}'.")
        return None
    return UDDeprelTag(
        code=deprel.code,
        name=deprel.name,
    )


if __name__ == "__main__":
    # Example usage
    tag = get_ud_deprel_tag("nsubj")
    print(tag)
    tag2 = get_ud_deprel_tag("obj")
    print(tag2)

    # Direct instantiation with validation
    try:
        tag3 = UDDeprelTag(code="nsubj", name="nominal subject")
        print(tag3)
    except ValueError as e:
        print(e)
    try:
        tag4 = UDDeprelTag(code="notareal", name="fake")
    except ValueError as e:
        print(e)
