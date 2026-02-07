"""Tests for scholar-facing export helpers."""

from xml.etree import ElementTree as ET

from cltk.core.data_types import (
    Classification,
    Doc,
    Gloss,
    IPAEnrichment,
    Language,
    LemmaTranslationCandidate,
    Translation,
    UDFeatureTag,
    UDFeatureTagSet,
    Word,
    WordEnrichment,
)
from cltk.exports import (
    doc_to_igt_html,
    doc_to_igt_latex,
    doc_to_readers_guide_html,
    doc_to_tei_xml,
)
from cltk.morphosyntax.ud_deprels import UDDeprelTag
from cltk.morphosyntax.ud_pos import UDPartOfSpeechTag


def _language() -> Language:
    return Language(
        name="TestLang",
        glottolog_id="test1234",
        level="language",
        classification=Classification(level="language"),
    )


def _doc() -> Doc:
    feats = UDFeatureTagSet(
        features=[
            UDFeatureTag(key="Case", value="Nom"),
            UDFeatureTag(key="Number", value="Sing"),
        ]
    )
    words = [
        Word(
            index_sentence=0,
            index_token=0,
            string="Gallia",
            lemma="Gallia",
            upos=UDPartOfSpeechTag(tag="PROPN"),
            features=feats,
            governor=1,
            dependency_relation=UDDeprelTag(code="nsubj", name="nominal subject"),
            enrichment=WordEnrichment(
                gloss=Gloss(context="Gaul"),
                ipa=IPAEnrichment(value="ˈɡal.li.a", mode="attic_5c_bce"),
            ),
        ),
        Word(
            index_sentence=0,
            index_token=1,
            string="est",
            lemma="sum",
            upos=UDPartOfSpeechTag(tag="AUX"),
            features=UDFeatureTagSet(
                features=[UDFeatureTag(key="Tense", value="Pres")]
            ),
            governor=None,
            dependency_relation=UDDeprelTag(code="root", name="root"),
            enrichment=WordEnrichment(
                lemma_translations=[LemmaTranslationCandidate(text="be")]
            ),
        ),
        Word(
            index_sentence=0,
            index_token=2,
            string="omnis",
            lemma="omnis",
            upos=UDPartOfSpeechTag(tag="ADJ"),
            features=UDFeatureTagSet(features=[UDFeatureTag(key="Case", value="Nom")]),
            governor=1,
            dependency_relation=UDDeprelTag(
                code="xcomp", name="open clausal complement"
            ),
        ),
        Word(
            index_sentence=1,
            index_token=0,
            string="divisa",
            lemma="divido",
            upos=UDPartOfSpeechTag(tag="VERB"),
            governor=None,
            dependency_relation=UDDeprelTag(code="root", name="root"),
        ),
        Word(
            index_sentence=1,
            index_token=1,
            string="est",
            lemma="sum",
            upos=UDPartOfSpeechTag(tag="AUX"),
            governor=0,
            dependency_relation=UDDeprelTag(code="aux", name="auxiliary"),
        ),
    ]
    doc = Doc(language=_language(), raw="Gallia est omnis. divisa est.", words=words)
    doc.sentence_translations = {
        0: Translation(text="Gaul is all.", source_lang_id="lat", target_lang_id="en")
    }
    return doc


def test_doc_to_igt_latex_contains_tokens() -> None:
    doc = _doc()
    output = doc_to_igt_latex(doc)
    assert "\\begin{tabular}" in output
    assert "Gallia" in output
    assert "Gaul" in output


def test_doc_to_igt_html_contains_table() -> None:
    doc = _doc()
    output = doc_to_igt_html(doc)
    assert "<table" in output
    assert "Gallia" in output
    assert "Gaul" in output


def test_doc_to_tei_xml_has_standoff() -> None:
    doc = _doc()
    output = doc_to_tei_xml(doc, include_gloss=True)
    root = ET.fromstring(output)
    ns = {
        "tei": "http://www.tei-c.org/ns/1.0",
        "xml": "http://www.w3.org/XML/1998/namespace",
    }
    token = root.find(".//tei:w[@xml:id='s1w1']", ns)
    assert token is not None
    stand_off = root.find(".//tei:standOff", ns)
    assert stand_off is not None
    relation = root.find(".//tei:relation", ns)
    assert relation is not None


def test_doc_to_readers_guide_html_contains_tooltips() -> None:
    doc = _doc()
    output = doc_to_readers_guide_html(doc)
    assert "<html" in output
    assert "<style>" in output
    assert "Gallia" in output
    assert "Gloss: Gaul" in output
