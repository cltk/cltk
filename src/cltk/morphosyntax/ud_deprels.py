"""Universal Dependencies (UD) dependency relations.

This module defines the core UD dependency relations (DepRel) and provides
validated data models and helpers for working with them.

References:
    - UD homepage: https://universaldependencies.org/u/dep/index.html

"""

__license__ = "MIT License. See LICENSE."

from typing import Literal, Optional

from pydantic import BaseModel, ValidationInfo, field_validator, model_validator

from cltk.core.cltk_logger import logger

# TODO: This can probably be removed; was used to validate UDDeprel instances
VALID_DEPREL_CATEGORIES: dict[str, tuple[str, Optional[str]]] = {
    "nsubj": ("Nominal", "Core Argument"),
    "obj": ("Nominal", "Core Argument"),
    "iobj": ("Nominal", "Core Argument"),
    "csubj": ("Clause", "Core Argument"),
    "ccomp": ("Clause", "Core Argument"),
    "xcomp": ("Clause", "Core Argument"),
    "obl": ("Nominal", "Non-core Dependent"),
    "vocative": ("Nominal", "Non-core Dependent"),
    "expl": ("Nominal", "Non-core Dependent"),
    "dislocated": ("Nominal", "Non-core Dependent"),
    "advcl": ("Clause", "Non-core Dependent"),
    "advmod": ("Modifier Word", "Non-core Dependent"),
    "discourse": ("Modifier Word", "Non-core Dependent"),
    "aux": ("Function Word", "Non-core Dependent"),
    "cop": ("Function Word", "Non-core Dependent"),
    "mark": ("Function Word", "Non-core Dependent"),
    "nmod": ("Nominal", "Nominal Dependent"),
    "appos": ("Nominal", "Nominal Dependent"),
    "nummod": ("Nominal", "Nominal Dependent"),
    "acl": ("Clause", "Nominal Dependent"),
    "amod": ("Modifier Word", "Nominal Dependent"),
    "det": ("Function Word", "Nominal Dependent"),
    "case": ("Function Word", "Nominal Dependent"),
    "conj": ("Coordination", None),
    "cc": ("Coordination", None),
    "fixed": ("Headless", None),
    "flat": ("Headless", None),
    "list": ("Loose", None),
    "parataxis": ("Loose", None),
    "compound": ("Special", None),
    "orphan": ("Special", None),
    "goeswith": ("Special", None),
    "reparandum": ("Special", None),
    "punct": ("Other", None),
    "root": ("Other", None),
    "dep": ("Other", None),
}


class UDDeprel(BaseModel):
    """Canonical UD dependency relation definition.

    Represents a single UD relation (e.g., ``nsubj``) together with its
    human-readable name, high-level word type, optional syntactic role, and
    other metadata.

    Validation ensures that the combination of ``code``, ``word_type`` and
    ``syntactic_role`` matches the UD taxonomy encoded in
    ``VALID_DEPREL_CATEGORIES``.

    Attributes:
        code: Short UD code (e.g., ``"nsubj"``).
        name: Human-readable name (e.g., ``"nominal subject"``).
        word_type: High-level category describing the head/word type.
        syntactic_role: Optional role such as ``"Core Argument"``.
        subtypes: Optional list of defined UD subtypes for this relation.
        description: Official UD description of the relation.
        is_obsolete: Whether the relation is obsolete or discouraged.

    """

    code: str  # e.g., "nsubj"
    name: str  # Human-readable name, e.g., "nominal subject"
    word_type: Literal[
        "Nominal",
        "Clause",
        "Modifier Word",
        "Function Word",
        "Coordination",
        "Headless",
        "Loose",
        "Special",
        "Other",
    ]
    syntactic_role: Optional[
        Literal["Core Argument", "Non-core Dependent", "Nominal Dependent"]
    ] = None
    subtypes: Optional[list[str]] = None
    description: str  # Official UD description
    is_obsolete: Optional[bool] = False

    @model_validator(mode="after")
    def validate_categories(self) -> "UDDeprel":
        """Validate ``word_type``/``syntactic_role`` for this relation.

        Ensures that the pair ``(word_type, syntactic_role)`` is allowed for the
        given ``code`` according to ``VALID_DEPREL_CATEGORIES``.

        Raises:
            ValueError: If the combination is not allowed for ``code``.

        Returns:
            The validated model instance (self).

        """
        allowed = VALID_DEPREL_CATEGORIES.get(self.code)
        if allowed:
            if (self.word_type, self.syntactic_role) != allowed:
                raise ValueError(
                    f"For DepRel '{self.code}', only word_type='{allowed[0]}' and syntactic_role='{allowed[1]}' are allowed."
                )
        return self


class UDDeprelTag(BaseModel):
    """A concrete tag instance referencing a UD relation.

    This model validates that the ``code`` is a known UD relation and, if a
    ``subtype`` is provided, that it is permitted for the given ``code``.

    Attributes:
        code: Short UD code (e.g., ``"nsubj"``).
        name: Human-readable name for display.
        subtype: Optional UD subtype (e.g., ``"outer"``, ``"pass"``).

    """

    code: str  # e.g., "nsubj"
    name: str  # Human-readable name
    subtype: Optional[str] = None  # e.g., "outer", "pass"

    @field_validator("code")
    @classmethod
    def validate_code(cls, deprel_code: str) -> str:
        """Ensure that ``deprel_code`` is one of the known UD relations.

        Args:
            deprel_code: Candidate UD DepRel code.

        Raises:
            ValueError: If ``deprel_code`` is not present in ``UD_DEPRELS``.

        Returns:
            The validated code.

        """
        if deprel_code not in UD_DEPRELS:
            raise ValueError(f"Invalid UD DepRel code: '{deprel_code}'")
        return deprel_code

    @field_validator("subtype")
    @classmethod
    def validate_subtype(
        cls, subtype: Optional[str], values: ValidationInfo
    ) -> Optional[str]:
        """Validate that ``subtype`` is allowed for the given ``code``.

        Uses the already-validated ``code`` value from Pydantic's ``values`` to
        check whether a provided ``subtype`` is among the declared subtypes for
        that relation.

        Args:
            subtype: Optional UD subtype to validate.
            values: Pydantic validation context containing ``code``.

        Raises:
            ValueError: If a non-empty ``subtype`` is not permitted for ``code``.

        Returns:
            The provided ``subtype`` if valid, otherwise ``None``.

        """
        code_any = values.data.get("code")
        code = code_any if isinstance(code_any, str) else None
        if subtype:
            if code is None:
                return subtype
            deprel = UD_DEPRELS.get(code)
            if not deprel or not deprel.subtypes or subtype not in deprel.subtypes:
                raise ValueError(
                    f"DepRel subtype '{subtype}' not available for DepRel '{code}'"
                )
        return subtype

    def __str__(self) -> str:
        """Return a concise, readable representation of the tag."""
        string: str = f'UDDeprelTag(code="{self.code}", name="{self.name}"'
        if self.subtype:
            string += f', subtype="{self.subtype}"'
        string += ")"
        return string

    def __repr__(self) -> str:
        """Alias for ``__str__`` to aid debugging and logging."""
        return self.__str__()


# Official UD dependency relations (core set, see UD docs for full list)
UD_DEPRELS: dict[str, UDDeprel] = {
    "acl": UDDeprel(
        code="acl",
        name="clausal modifier of noun",
        word_type="Clause",
        syntactic_role="Nominal Dependent",
        description="Clausal modifier of noun (adnominal clause).",
        subtypes=["relcl"],
    ),
    "advcl": UDDeprel(
        code="advcl",
        name="adverbial clause modifier",
        word_type="Clause",
        syntactic_role="Non-core Dependent",
        description="Adverbial clause modifier.",
        subtypes=["relcl"],
    ),
    "advmod": UDDeprel(
        code="advmod",
        name="adverbial modifier",
        word_type="Modifier Word",
        syntactic_role="Non-core Dependent",
        description="Adverbial modifier.",
        subtypes=["emph", "lmod"],
    ),
    "amod": UDDeprel(
        code="amod",
        name="adjectival modifier",
        word_type="Modifier Word",
        syntactic_role="Nominal Dependent",
        description="Adjectival modifier.",
    ),
    "appos": UDDeprel(
        code="appos",
        name="appositional modifier",
        word_type="Nominal",
        syntactic_role="Nominal Dependent",
        description="Appositional modifier.",
    ),
    "aux": UDDeprel(
        code="aux",
        name="auxiliary",
        word_type="Function Word",
        syntactic_role="Non-core Dependent",
        description="Auxiliary.",
        subtypes=["pass"],
    ),
    "case": UDDeprel(
        code="case",
        name="case marking",
        word_type="Function Word",
        syntactic_role="Nominal Dependent",
        description="Case marking.",
    ),
    "cc": UDDeprel(
        code="cc",
        name="coordinating conjunction",
        word_type="Coordination",
        syntactic_role=None,
        description="Coordinating conjunction.",
        subtypes=["preconj"],
    ),
    "ccomp": UDDeprel(
        code="ccomp",
        name="clausal complement",
        word_type="Clause",
        syntactic_role="Core Argument",
        description="Clausal complement with internal subject.",
    ),
    "clf": UDDeprel(
        code="clf",
        name="classifier",
        word_type="Function Word",
        syntactic_role="Nominal Dependent",
        description="Classifier.",
    ),
    "compound": UDDeprel(
        code="compound",
        name="compound",
        word_type="Special",
        syntactic_role=None,
        description="Compound.",
        subtypes=["lvc", "prt", "redup", "svc"],
    ),
    "conj": UDDeprel(
        code="conj",
        name="conjunct",
        word_type="Coordination",
        syntactic_role=None,
        description="Conjunct.",
    ),
    "cop": UDDeprel(
        code="cop",
        name="copula",
        word_type="Function Word",
        syntactic_role="Non-core Dependent",
        description="Copula.",
    ),
    "csubj": UDDeprel(
        code="csubj",
        name="clausal subject",
        word_type="Clause",
        syntactic_role="Core Argument",
        description="Clausal subject.",
        subtypes=["outer", "pass"],
    ),
    "dep": UDDeprel(
        code="dep",
        name="unspecified dependency",
        word_type="Other",
        syntactic_role=None,
        description="Unspecified dependency.",
    ),
    "det": UDDeprel(
        code="det",
        name="determiner",
        word_type="Function Word",
        syntactic_role="Nominal Dependent",
        description="Determiner.",
        subtypes=["numgov", "nummod", "poss"],
    ),
    "discourse": UDDeprel(
        code="discourse",
        name="discourse element",
        word_type="Modifier Word",
        syntactic_role="Non-core Dependent",
        description="Discourse element.",
    ),
    "dislocated": UDDeprel(
        code="dislocated",
        name="dislocated elements",
        word_type="Nominal",
        syntactic_role="Non-core Dependent",
        description="Dislocated elements.",
    ),
    "expl": UDDeprel(
        code="expl",
        name="expletive",
        word_type="Nominal",
        syntactic_role="Non-core Dependent",
        description="Expletive.",
        subtypes=["impers", "pass", "pv"],
    ),
    "fixed": UDDeprel(
        code="fixed",
        name="fixed multiword expression",
        word_type="Headless",
        syntactic_role=None,
        description="Fixed multiword expression.",
    ),
    "flat": UDDeprel(
        code="flat",
        name="flat multiword expression",
        word_type="Headless",
        syntactic_role=None,
        description="Flat multiword expression.",
        subtypes=["foreign", "name"],
    ),
    "goeswith": UDDeprel(
        code="goeswith",
        name="goes with",
        word_type="Special",
        syntactic_role=None,
        description="Goes with.",
    ),
    "iobj": UDDeprel(
        code="iobj",
        name="indirect object",
        word_type="Nominal",
        syntactic_role="Core Argument",
        description="Indirect object.",
    ),
    "list": UDDeprel(
        code="list",
        name="list",
        word_type="Loose",
        syntactic_role=None,
        description="List.",
    ),
    "mark": UDDeprel(
        code="mark",
        name="marker",
        word_type="Function Word",
        syntactic_role="Non-core Dependent",
        description="Marker.",
    ),
    "nmod": UDDeprel(
        code="nmod",
        name="nominal modifier",
        word_type="Nominal",
        syntactic_role="Nominal Dependent",
        description="Nominal modifier.",
        subtypes=["poss", "tmod"],
    ),
    "nsubj": UDDeprel(
        code="nsubj",
        name="nominal subject",
        word_type="Nominal",
        syntactic_role="Core Argument",
        description="Nominal subject.",
        subtypes=["outer", "pass"],
    ),
    "nummod": UDDeprel(
        code="nummod",
        name="numeric modifier",
        word_type="Nominal",
        syntactic_role="Nominal Dependent",
        description="Numeric modifier.",
        subtypes=["gov"],
    ),
    "obj": UDDeprel(
        code="obj",
        name="object",
        word_type="Nominal",
        syntactic_role="Core Argument",
        description="Object.",
    ),
    "obl": UDDeprel(
        code="obl",
        name="oblique nominal",
        word_type="Nominal",
        syntactic_role="Non-core Dependent",
        description="Oblique nominal.",
        subtypes=["agent", "arg", "lmod", "tmod"],
    ),
    "orphan": UDDeprel(
        code="orphan",
        name="orphan",
        word_type="Special",
        syntactic_role=None,
        description="Orphan.",
    ),
    "parataxis": UDDeprel(
        code="parataxis",
        name="parataxis",
        word_type="Loose",
        syntactic_role=None,
        description="Parataxis.",
    ),
    "punct": UDDeprel(
        code="punct",
        name="punctuation",
        word_type="Other",
        syntactic_role=None,
        description="Punctuation.",
    ),
    "reparandum": UDDeprel(
        code="reparandum",
        name="overridden disfluency",
        word_type="Special",
        syntactic_role=None,
        description="Overridden disfluency.",
    ),
    "root": UDDeprel(
        code="root",
        name="root",
        word_type="Other",
        syntactic_role=None,
        description="Root.",
    ),
    "vocative": UDDeprel(
        code="vocative",
        name="vocative",
        word_type="Nominal",
        syntactic_role="Non-core Dependent",
        description="Vocative.",
    ),
    "xcomp": UDDeprel(
        code="xcomp",
        name="open clausal complement",
        word_type="Clause",
        syntactic_role="Core Argument",
        description="Open clausal complement.",
    ),
}


def normalize_deprel(code: str, subtype: Optional[str]) -> tuple[str, Optional[str]]:
    """Normalize a UD deprel pair to a valid combination.

    If ``subtype`` is not one of the allowed subtypes for ``code`` (as declared
    in this module), drop the subtype and log the remapping. This accommodates
    common non‑UD patterns such as case‑coded subtypes (e.g., ``nmod:gen``,
    ``obl:abl``) when morphology is already handled elsewhere.

    Args:
        code: UD deprel code (e.g., ``"obl"``, ``"nmod"``).
        subtype: Optional subtype string.

    Returns:
        A tuple ``(code, normalized_subtype)`` where the subtype may be ``None``
        if it was not allowed for the given ``code``.

    """
    deprel = UD_DEPRELS.get(code)
    if not deprel:
        return code, subtype
    if not subtype:
        return code, None
    allowed = set(deprel.subtypes or [])
    if subtype in allowed:
        return code, subtype
    logger.info(
        "Normalizing UD deprel subtype: '%s:%s' → '%s' (dropping subtype)",
        code,
        subtype,
        code,
    )
    return code, None


def is_valid_deprel(code: str) -> bool:
    """Return whether ``code`` is a known UD relation.

    Args:
        code: Candidate UD DepRel code to check.

    Returns:
        True if ``code`` is defined in ``UD_DEPRELS``; otherwise False.

    """
    return code in UD_DEPRELS


def get_ud_deprel_tag(
    code: str, subtype: Optional[str] = None
) -> Optional[UDDeprelTag]:
    """Build a ``UDDeprelTag`` for a UD relation if available.

    Applies a light normalization step: when the provided ``subtype`` is not
    permitted for ``code``, it is dropped and the remapping is logged.

    Args:
        code: UD DepRel code to look up.
        subtype: Optional UD subtype to attach to the tag.

    Returns:
        A validated ``UDDeprelTag`` for the given ``code``, or ``None`` if the
        code is unknown.

    """
    deprel = UD_DEPRELS.get(code)
    if not deprel:
        logger.warning(f"Unknown UD DepRel code '{code}'.")
        return None
    norm_code, norm_subtype = normalize_deprel(code, subtype)
    tag: UDDeprelTag = UDDeprelTag(
        code=deprel.code,
        name=deprel.name,
        subtype=norm_subtype,
    )
    return tag


if __name__ == "__main__":
    # Example usage
    tag = get_ud_deprel_tag("nsubj")
    print(tag)
    tag2 = get_ud_deprel_tag("obj")
    print(tag2)
    print("")
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
    print("")
    tag = get_ud_deprel_tag("nsubj", subtype="outer")
    print(tag)
    print("")
    try:
        tag = get_ud_deprel_tag("nsubj", subtype="invalid-subtype")
        print(tag)
    except ValueError as e:
        print(e)
