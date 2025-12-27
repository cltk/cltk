"""Example of a custom Pipeline scanning Ancient Greek iambic trimeter."""

import re
import unicodedata
from typing import ClassVar

from cltk import NLP
from cltk.core.data_types import Doc, Pipeline, Process
from cltk.core.process_registry import register_process

_IAMBIC_TEMPLATE = ["x", "-", "u", "-", "x", "-", "u", "-", "x", "-", "u", "-"]
_VOWEL_RE = re.compile(r"[αεηιουω]+")
_DIPHTHONGS = ("αι", "ει", "οι", "υι", "αυ", "ευ", "ου", "ηυ", "ωυ")
_GREEK_GLOTTOLOG_IDS = {"anci1242"}


def _strip_diacritics(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def _normalize_greek(text: str) -> str:
    text = _strip_diacritics(text).lower()
    text = re.sub(r"[0-9]", "", text)
    return re.sub(r"[^\w\s]", "", text)


def _scan_line(line: str) -> str:
    cleaned = _normalize_greek(line)
    syllables = _VOWEL_RE.findall(cleaned)
    quantities: list[str] = []
    for syl in syllables:
        long_by_vowel = "η" in syl or "ω" in syl
        long_by_diphthong = any(diph in syl for diph in _DIPHTHONGS)
        quantities.append("-" if long_by_vowel or long_by_diphthong else "u")
    quantities = quantities[: len(_IAMBIC_TEMPLATE)]
    pattern = [
        quantities[i] if i < len(quantities) else _IAMBIC_TEMPLATE[i]
        for i in range(len(_IAMBIC_TEMPLATE))
    ]
    return " ".join(pattern)


@register_process
class GreekIambicTrimeterProcess(Process):
    process_id: ClassVar[str] = "prosody.iambic_trimeter"
    glottolog_id: str | None = None
    output_key: str = "scansion"

    def run(self, input_doc: Doc) -> Doc:
        lang = input_doc.language
        iso = getattr(lang, "iso", None) or getattr(lang, "iso_set", {}).get("639-3")
        if lang.glottolog_id not in _GREEK_GLOTTOLOG_IDS and iso != "grc":
            raise ValueError("Iambic trimeter scanner is Ancient Greek only.")
        lines = [line.strip() for line in (input_doc.raw or "").splitlines() if line]
        scans = [_scan_line(line) for line in lines]
        input_doc.metadata.setdefault(self.output_key, scans)
        return input_doc


TEXT = """Εἴθ᾽ ὤφελ᾽ Ἀργοῦς μὴ διαπτάσθαι σκάφος
Κόλχων ἐς αἶαν κυανέας Συμπληγάδας,
μηδ᾽ ἐν νάπαισι Πηλίου πεσεῖν ποτε
τμηθεῖσα πεύκη, μηδ᾽ ἐρετμῶσαι χέρας
5ἀνδρῶν ἀριστέων οἳ τὸ πάγχρυσον δέρος
Πελίᾳ μετῆλθον."""

pipeline = Pipeline.from_toml("examples/pipeline_greek_iambic.toml")
nlp = NLP(language_code="anci1242", custom_pipeline=pipeline)
doc = nlp.analyze(TEXT)

for line, scan in zip(TEXT.splitlines(), doc.metadata["scansion"]):
    print(line)
    print(scan)
