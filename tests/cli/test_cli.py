"""CLI parser and output handling tests."""

from pathlib import Path

import pytest

from cltk.cli import dispatch
from cltk.cli.main import build_parser
from cltk.cli.utils import require_parquet_deps, write_feature_table_csv
from cltk.core.data_types import Classification, Doc, Language, Word
from cltk.morphosyntax.ud_pos import UDPartOfSpeechTag
from cltk.utils.file_outputs import doc_to_conllu


def _language() -> Language:
    """Return a minimal Language stub."""
    return Language(
        name="TestLang",
        glottolog_id="test1234",
        level="language",
        classification=Classification(level="language"),
    )


def _doc() -> Doc:
    """Return a minimal Doc stub with one token."""
    word = Word(
        index_sentence=0,
        index_token=0,
        string="A",
        lemma="a",
        upos=UDPartOfSpeechTag(tag="NOUN"),
    )
    doc = Doc(language=_language(), raw="A", words=[word])
    doc.backend = "stanza"
    return doc


def test_parse_analyze_smoke() -> None:
    """Parse analyze CLI arguments."""
    parser = build_parser()
    args = parser.parse_args(
        [
            "analyze",
            "--lang",
            "lati1261",
            "--backend",
            "stanza",
            "--out",
            "raw",
            "--text",
            "Salve",
        ]
    )
    assert args.command == "analyze"
    assert args.out == "raw"


def test_parse_compare_smoke() -> None:
    """Parse compare CLI arguments."""
    parser = build_parser()
    args = parser.parse_args(
        [
            "compare",
            "--lang",
            "grc",
            "--text",
            "Salve",
            "--backends",
            "stanza,openai",
        ]
    )
    assert args.command == "compare"
    assert args.format == "md"


def test_parse_export_smoke() -> None:
    """Parse export CLI arguments."""
    parser = build_parser()
    args = parser.parse_args(
        [
            "export",
            "--lang",
            "grc",
            "--backend",
            "stanza",
            "--text",
            "Salve",
            "--conllu",
            "out.conllu",
        ]
    )
    assert args.command == "export"
    assert args.conllu == "out.conllu"


def test_parse_pipeline_describe_smoke() -> None:
    """Parse pipeline describe CLI arguments."""
    parser = build_parser()
    args = parser.parse_args(
        [
            "pipeline",
            "describe",
            "--toml",
            "pipeline.toml",
        ]
    )
    assert args.command == "pipeline"
    assert args.pipeline_command == "describe"


def test_dispatch_conllu_mapping() -> None:
    """Map dispatch output to CoNLL-U."""
    doc = _doc()
    assert dispatch.render_output(doc, "conllu") == doc_to_conllu(doc)


def test_feature_table_csv_tsv_writing(tmp_path: Path) -> None:
    """Write feature tables to CSV and TSV outputs."""

    class StubTable:
        column_names = ["token", "lemma"]

        def to_pylist(self):
            return [
                {"token": "A", "lemma": "a"},
                {"token": "B", "lemma": "b"},
            ]

    table = StubTable()
    csv_path = tmp_path / "table.csv"
    tsv_path = tmp_path / "table.tsv"

    write_feature_table_csv(table, out_path=csv_path, delimiter=",")
    write_feature_table_csv(table, out_path=tsv_path, delimiter="\t")

    assert csv_path.read_text(encoding="utf-8").splitlines()[0] == "token,lemma"
    assert tsv_path.read_text(encoding="utf-8").splitlines()[0] == "token\tlemma"


def test_parquet_requires_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    """Raise when parquet dependencies are missing."""
    monkeypatch.setattr("cltk.cli.utils._module_available", lambda _: False)
    with pytest.raises(
        RuntimeError, match="Parquet export requires pandas and pyarrow"
    ):
        require_parquet_deps()
