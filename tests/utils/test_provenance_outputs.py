import pytest

from cltk.core.data_types import Classification, Doc, Language, Word
from cltk.core.provenance import add_provenance_record, build_provenance_record
from cltk.morphosyntax.ud_pos import UDPartOfSpeechTag
from cltk.utils.file_outputs import (
    doc_to_conllu,
    doc_to_feature_table,
    format_readers_guide,
)


def _language() -> Language:
    return Language(
        name="TestLang",
        glottolog_id="test1234",
        level="language",
        classification=Classification(level="language"),
    )


def _doc_with_provenance() -> tuple[Doc, str]:
    word = Word(
        index_sentence=0,
        index_token=0,
        string="A",
        lemma="a",
        upos=UDPartOfSpeechTag(tag="NOUN"),
    )
    doc = Doc(language=_language(), raw="A", words=[word])
    record = build_provenance_record(
        language="test1234",
        backend="stanza",
        process="TestProcess",
        model="stanza",
    )
    prov_id = add_provenance_record(doc, record, set_default=True)
    word.annotation_sources["lemma"] = prov_id
    word.confidence["lemma"] = 0.9
    return doc, prov_id


def test_conllu_includes_provenance_and_confidence() -> None:
    doc, prov_id = _doc_with_provenance()
    conllu = doc_to_conllu(doc, include_provenance=True, include_confidence=True)
    lines = [line for line in conllu.splitlines() if line]
    assert f"# cltk_provenance_default={prov_id}" in lines[0]
    assert any(line.startswith(f"# cltk_prov.{prov_id}=") for line in lines)
    token_line = next(line for line in lines if not line.startswith("#"))
    misc = token_line.split("\t")[9]
    assert f"SrcLemma={prov_id}" in misc
    assert "ConfLemma=0.9" in misc


def test_readers_guide_includes_provenance_and_confidence() -> None:
    doc, _ = _doc_with_provenance()
    guide = format_readers_guide(doc, include_provenance=True, include_confidence=True)
    assert "## Provenance" in guide
    assert "**Confidence:**" in guide


def test_feature_table_includes_provenance_columns() -> None:
    pytest.importorskip("pyarrow")
    doc, prov_id = _doc_with_provenance()
    table = doc_to_feature_table(doc, include_provenance=True, include_confidence=True)
    assert "prov_lemma" in table.column_names
    assert "conf_lemma" in table.column_names
    prov_values = table["prov_lemma"].to_pylist()
    assert prov_id in prov_values
