from typing import Iterable, Optional

from cltk.core.cltk_logger import logger
from cltk.core.data_types import Doc, Word
from cltk.core.logging_utils import bind_from_doc
from cltk.morphosyntax.ud_features import (
    UDFeatureTag,
    UDFeatureTagSet,
    convert_pos_features_to_ud,
)
from cltk.morphosyntax.ud_pos import UDPartOfSpeechTag

# Normalization of common UD values from long names to codes
_UD_VALUE_NORMALIZE = {
    # Case
    "nominative": "Nom",
    "accusative": "Acc",
    "genitive": "Gen",
    "dative": "Dat",
    "ablative": "Abl",
    "locative": "Loc",
    "instrumental": "Ins",
    "vocative": "Voc",
    # Number
    "singular": "Sing",
    "plural": "Plur",
    "dual": "Dual",
    # Gender
    "masculine": "Masc",
    "feminine": "Fem",
    "neuter": "Neut",
    # Person
    "first": "1",
    "second": "2",
    "third": "3",
    # NumType
    "ordinal": "Ord",
    "cardinal": "Card",
    "mult": "Mult",
    "sets": "Sets",
    # Tense (keep conservative)
    "present": "Pres",
    "past": "Past",
    "future": "Fut",
    "perfect": "Perf",
    # Degree
    "positive": "Pos",
    "comparative": "Cmp",
    "superlative": "Sup",
}


def _norm_ud_key(k: str) -> str:
    # Best-effort: keep standard capitalization if it matches a typical UD key
    # Otherwise, title-case without spaces.
    known = {
        "Case",
        "Number",
        "Gender",
        "Person",
        "NumType",
        "Tense",
        "Degree",
        "Mood",
        "Voice",
        "Aspect",
        "Polarity",
        "Definite",
        "PronType",
        "Poss",
        "Reflex",
        "VerbForm",
        "Animacy",
        "Clusivity",
    }
    if k in known:
        return k
    return k.strip().replace(" ", "").replace("-", "")


def _norm_ud_val(v: str) -> str:
    s = v.strip()
    if not s:
        return s
    code = _UD_VALUE_NORMALIZE.get(s.lower())
    return code or s


def _iter_ud_pairs_from_set(feats: UDFeatureTagSet) -> list[tuple[str, str]]:
    """Extract (Key, Code) directly from UDFeatureTagSet."""
    try:
        tags = getattr(feats, "features", None)
        if tags is None:
            # Fallback: some callers may pass an iterable of UDFeatureTag
            tags = list(feats)
    except Exception:
        return []
    pairs: list[tuple[str, str]] = []
    for t in tags:
        if isinstance(t, UDFeatureTag):
            k = t.key
            v = t.value  # already a UD code per your model
            if isinstance(k, str) and isinstance(v, str) and k and v:
                pairs.append((k, v))
        else:
            # Very defensive fallback for unexpected shapes
            k_obj = getattr(t, "key", None)
            v_obj = getattr(t, "value", None)
            k_str = k_obj if isinstance(k_obj, str) else None
            v_str = v_obj if isinstance(v_obj, str) else None
            if k_str and v_str:
                pairs.append((k_str, v_str))
    return pairs


def _upos_to_str(upos: Optional[UDPartOfSpeechTag]) -> str:
    if upos is None:
        return "_"
    return getattr(upos, "tag", str(upos)) or "_"


def _feats_to_str(feats: Optional[UDFeatureTagSet]) -> str:
    if feats is None:
        return "_"
    # Prefer registry-backed tags (keys and codes) from UDFeatureTagSet
    if isinstance(feats, UDFeatureTagSet):
        pairs = _iter_ud_pairs_from_set(feats)
        if pairs:
            pairs.sort(key=lambda kv: (kv[0], kv[1]))
            return "|".join(f"{k}={v}" for k, v in pairs)
        return "_"
    # Last resort: accept a string that is already in CoNLL-U format
    if isinstance(feats, str):
        return feats if "=" in feats else "_"
    # Unknown object → try string, otherwise empty
    try:
        s = str(feats)
        return s if "=" in s else "_"
    except Exception:
        return "_"


def _deprel_to_str(dep_obj: Optional[object]) -> str:
    if dep_obj is None:
        return "_"
    if isinstance(dep_obj, str):
        return dep_obj or "_"
    for attr in ("code", "ud", "name", "value"):
        v = getattr(dep_obj, attr, None)
        if isinstance(v, str) and v:
            return v
    try:
        s = str(dep_obj)
        return s if s else "_"
    except Exception:
        return "_"


def words_to_conllu(words: Iterable[Word]) -> str:
    """Serialize a flat list of Words to a single-sentence CoNLL-U string."""
    lines: list[str] = []
    for i, w in enumerate(words, start=1):
        form = getattr(w, "string", None) or "_"
        lemma = getattr(w, "lemma", None) or "_"
        upos_str = _upos_to_str(getattr(w, "upos", None))
        feats_str = _feats_to_str(getattr(w, "features", None))

        # HEAD
        head_val = None
        for cand in ("head", "head_index", "governor", "head_id"):
            head_val = getattr(w, cand, None)
            if head_val is not None:
                break
        try:
            head = str(int(head_val)) if head_val is not None else "_"
        except Exception:
            head = "_"

        # DEPREL
        dep_obj = None
        for cand in (
            "deprel",
            "dep_rel",
            "dependency_relation",
            "relation",
            "ud_relation",
            "dependency_label",
            "dep_label",
        ):
            dep_obj = getattr(w, cand, None)
            if dep_obj:
                break
        deprel_str = _deprel_to_str(dep_obj)

        cols = [
            str(i),  # ID
            form,  # FORM
            lemma,  # LEMMA
            upos_str,  # UPOS
            "_",  # XPOS
            feats_str,  # FEATS
            head,  # HEAD
            deprel_str,  # DEPREL
            "_",  # DEPS
            "_",  # MISC
        ]
        lines.append("\t".join(cols))
    return "\n".join(lines) + ("\n" if lines else "")


def doc_to_conllu(doc: Doc) -> str:
    """Serialize Doc.words to a single-sentence CoNLL-U string."""
    log = bind_from_doc(doc)
    words = getattr(doc, "words", []) or []
    log.debug("Serializing %s tokens to CoNLL-U", len(words))
    return words_to_conllu(words)


def conllu_to_words(conllu: str) -> list[Word]:
    """Parse a CoNLL-U string (single or multiple sentences) into a flat list[Word].

    - Ignores comment lines (#).
    - Skips multiword tokens (e.g., '3-4') and empty nodes (e.g., '5.1').
    - Maps FEATS using convert_pos_features_to_ud when possible.
    - Sets Word.index_token as 0-based (ID-1).
    """
    out: list[Word] = []
    for raw_line in conllu.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) < 10:
            logger.debug("Skipping malformed CoNLL-U line (expected 10 cols): %r", line)
            continue

        (
            tid,
            form,
            lemma,
            upos_raw,
            xpos,
            feats_raw,
            head_raw,
            deprel_raw,
            deps,
            misc,
        ) = cols[:10]

        # Skip multiword tokens and empty nodes
        if "-" in tid or "." in tid:
            continue
        try:
            tid_i = int(tid)
        except Exception:
            logger.debug("Skipping non-integer token ID: %r", tid)
            continue

        # UPOS
        upos_obj: Optional[UDPartOfSpeechTag] = None
        if upos_raw and upos_raw != "_":
            try:
                upos_obj = UDPartOfSpeechTag(tag=upos_raw)
            except Exception as e:
                logger.debug("Could not build UDPartOfSpeechTag(%r): %s", upos_raw, e)
                upos_obj = None

        # FEATS
        feats_obj: Optional[UDFeatureTagSet] = None
        if feats_raw and feats_raw != "_":
            try:
                feats_obj = convert_pos_features_to_ud(feats_raw=feats_raw)
            except Exception as e:
                logger.debug("Could not parse FEATS %r: %s", feats_raw, e)

        # Build Word (index_token 0-based)
        try:
            w = Word(
                string=None if form == "_" else form,
                index_token=tid_i - 1,
                lemma=None if lemma == "_" else lemma,
                upos=upos_obj,
            )
        except Exception:
            # Fallback minimal constructor
            w = Word(string=None if form == "_" else form, index_token=tid_i - 1)
            # Try to assign upos if dataclass allows attribute setting
            try:
                setattr(w, "upos", upos_obj)
            except Exception:
                pass

        # Assign features if possible
        try:
            setattr(w, "features", feats_obj)
        except Exception:
            pass

        # Optional dependency info
        # HEAD
        head_val: Optional[int] = None
        if head_raw and head_raw != "_":
            try:
                head_val = int(head_raw)
            except Exception:
                head_val = None
        for cand in ("head", "head_index", "governor", "head_id"):
            try:
                setattr(w, cand, head_val)
                break
            except Exception:
                continue
        # DEPREL
        if deprel_raw and deprel_raw != "_":
            try:
                setattr(w, "deprel", deprel_raw)
            except Exception:
                pass

        out.append(w)

    return out
