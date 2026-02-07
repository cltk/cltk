from cltk.core.data_types import (
    Classification,
    Doc,
    Language,
    UDFeatureTag,
    UDFeatureTagSet,
    Word,
)
from cltk.evaluation.compare_backends import (
    _align_tokens,
    _compare_docs,
    _normalize_doc,
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


def test_normalize_doc_features_and_sentences() -> None:
    words = [
        Word(
            index_sentence=0,
            index_token=0,
            string="A",
            lemma="a",
            upos=UDPartOfSpeechTag(tag="NOUN"),
            features=UDFeatureTagSet(features=[UDFeatureTag(key="Case", value="Nom")]),
            dependency_relation=UDDeprelTag(code="nsubj", name="nominal subject"),
            governor=1,
        ),
        Word(
            index_sentence=0,
            index_token=1,
            string="B",
            lemma="b",
            upos=UDPartOfSpeechTag(tag="VERB"),
            features=UDFeatureTagSet(
                features=[UDFeatureTag(key="Tense", value="Pres")]
            ),
            dependency_relation=UDDeprelTag(code="root", name="root"),
            governor=0,
        ),
        Word(
            index_sentence=1,
            index_token=0,
            string="C",
            lemma="c",
            upos=UDPartOfSpeechTag(tag="NOUN"),
        ),
    ]
    doc = Doc(language=_language(), raw="A B. C", words=words)
    normalized = _normalize_doc(
        doc=doc, language="test1234", max_sentences=None, max_tokens=None
    )
    assert len(normalized) == 2
    assert normalized[0].tokens[0].feats == "Case=Nom"
    assert normalized[0].tokens[1].upos == "VERB"
    assert normalized[0].tokens[0].deprel == "nsubj"


def test_align_tokens_dp_insert() -> None:
    alignment = _align_tokens(["A", "B"], ["A", "X", "B"])
    ops = [op.op for op in alignment.ops]
    assert alignment.strategy == "dp"
    assert "insert" in ops


def test_compare_docs_confusion_upos() -> None:
    lang = _language()
    doc_a = Doc(
        language=lang,
        raw="A B",
        words=[
            Word(
                index_sentence=0,
                index_token=0,
                string="A",
                upos=UDPartOfSpeechTag(tag="NOUN"),
            ),
            Word(
                index_sentence=0,
                index_token=1,
                string="B",
                upos=UDPartOfSpeechTag(tag="VERB"),
            ),
        ],
    )
    doc_b = Doc(
        language=lang,
        raw="A B",
        words=[
            Word(
                index_sentence=0,
                index_token=0,
                string="A",
                upos=UDPartOfSpeechTag(tag="NOUN"),
            ),
            Word(
                index_sentence=0,
                index_token=1,
                string="B",
                upos=UDPartOfSpeechTag(tag="NOUN"),
            ),
        ],
    )
    report = _compare_docs(
        language="test1234",
        text="A B",
        backends=["a", "b"],
        docs_by_backend={"a": doc_a, "b": doc_b},
        backend_meta={"a": {}, "b": {}},
        max_sentences=None,
        max_tokens=None,
        top_n=None,
    )
    confusion = report["summary"]["confusion"]["upos"]
    assert confusion["a vs b"]["VERB"]["NOUN"] == 1
