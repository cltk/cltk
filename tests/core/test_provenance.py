from cltk.core.data_types import Classification, Doc, Language, Sentence, Word
from cltk.core.provenance import (
    add_provenance_record,
    build_provenance_record,
    get_sentence_provenance,
    get_token_provenance,
)
from cltk.morphosyntax.ud_pos import UDPartOfSpeechTag


def _language() -> Language:
    return Language(
        name="TestLang",
        glottolog_id="test1234",
        level="language",
        classification=Classification(level="language"),
    )


def test_provenance_storage_and_helpers() -> None:
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

    assert doc.default_provenance_id == prov_id
    assert get_token_provenance(word, "lemma", doc=doc).id == prov_id
    word._doc = doc
    assert get_token_provenance(word, "lemma").id == prov_id

    sentence = Sentence(words=[word], index=0, annotation_sources={"translation": prov_id})
    assert get_sentence_provenance(sentence, "translation", doc=doc).id == prov_id

    dumped = doc.model_dump()
    restored = Doc.model_validate(dumped)
    assert prov_id in restored.provenance
    assert restored.words[0].annotation_sources["lemma"] == prov_id
    assert restored.words[0].confidence["lemma"] == 0.9
