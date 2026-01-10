"""CLI handler for the ``cltk export`` subcommand."""

import argparse
from pathlib import Path
from typing import Optional

from cltk import NLP
from cltk.cli import dispatch
from cltk.cli.utils import (
    HelpFormatter,
    build_cltk_config,
    load_text,
    parse_json_input,
    require_parquet_deps,
    resolve_pipeline,
    set_log_level,
    write_feature_table_csv,
    write_feature_table_parquet,
    write_json_output,
    write_text_output,
)


def configure_parser(subparsers: argparse._SubParsersAction) -> None:
    """Register the export subcommand parser."""
    parser = subparsers.add_parser(
        "export",
        help="Run a CLTK pipeline and write multiple outputs in one pass.",
        formatter_class=HelpFormatter,
    )
    parser.add_argument(
        "--lang",
        "--language",
        dest="language",
        required=True,
        help="Glottolog id or CLTK language key.",
    )
    parser.add_argument(
        "--backend",
        default="stanza",
        help="Backend to use (stanza, openai, ollama, mistral, spacy).",
    )
    parser.add_argument("--pipeline", help="Optional pipeline class name to use.")
    parser.add_argument("--text", help="Raw text to analyze.")
    parser.add_argument("--text-file", help="Path to a text file to analyze.")
    parser.add_argument(
        "--config",
        help="JSON string or path to JSON file for backend/pipeline settings.",
    )
    parser.add_argument(
        "--conllu",
        help="Write CoNLL-U output to this path.",
    )
    parser.add_argument(
        "--readers-guide",
        dest="readers_guide",
        help="Write reader's guide Markdown to this path.",
    )
    parser.add_argument(
        "--json",
        dest="json_path",
        help="Write JSON output to this path.",
    )
    parser.add_argument(
        "--csv",
        help="Write feature table CSV to this path.",
    )
    parser.add_argument(
        "--tsv",
        help="Write feature table TSV to this path.",
    )
    parser.add_argument(
        "--parquet",
        help="Write feature table Parquet to this path.",
    )
    parser.add_argument(
        "--raw",
        help="Write raw summary output to this path.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress non-error logs.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable info-level logs.",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    """Run the export command."""
    set_log_level(quiet=args.quiet, verbose=args.verbose)
    config = parse_json_input(args.config) if args.config else None
    pipeline = resolve_pipeline(args.pipeline) if args.pipeline else None
    cltk_config = build_cltk_config(
        language=args.language,
        backend=args.backend,
        config=config,
        pipeline=pipeline,
    )

    targets = _collect_targets(args)
    if not any(targets.values()):
        raise SystemExit("Provide at least one output path (e.g., --conllu).")

    text = load_text(args.text, args.text_file)
    try:
        nlp = NLP(cltk_config=cltk_config, suppress_banner=True)
        doc = nlp.analyze(text)
    except Exception as exc:
        raise SystemExit(str(exc)) from exc

    if targets["parquet"]:
        try:
            require_parquet_deps()
        except RuntimeError as exc:
            raise SystemExit(str(exc)) from exc

    table = None
    if targets["csv"] or targets["tsv"] or targets["parquet"]:
        try:
            table = dispatch.render_output(doc, "feature-table")
        except ImportError as exc:
            raise SystemExit(str(exc)) from exc

    if targets["conllu"]:
        payload = dispatch.render_output(doc, "conllu")
        output = dispatch.ensure_text_payload(payload, "conllu")
        write_text_output(output, targets["conllu"])
    if targets["readers_guide"]:
        payload = dispatch.render_output(doc, "readers-guide")
        output = dispatch.ensure_text_payload(payload, "readers-guide")
        write_text_output(output, targets["readers_guide"])
    if targets["json_path"]:
        payload = dispatch.render_output(doc, "json")
        data = dispatch.ensure_json_payload(payload, "json")
        write_json_output(data, targets["json_path"], pretty=True)
    if targets["raw"]:
        payload = dispatch.render_output(doc, "raw")
        output = dispatch.ensure_text_payload(payload, "raw")
        write_text_output(output, targets["raw"])

    if targets["csv"]:
        write_feature_table_csv(table, out_path=targets["csv"], delimiter=",")
    if targets["tsv"]:
        write_feature_table_csv(table, out_path=targets["tsv"], delimiter="\t")
    if targets["parquet"]:
        try:
            write_feature_table_parquet(table, targets["parquet"])
        except RuntimeError as exc:
            raise SystemExit(str(exc)) from exc

    return 0


def _collect_targets(args: argparse.Namespace) -> dict[str, Optional[Path]]:
    """Collect output target paths from CLI args."""
    return {
        "conllu": _path(args.conllu),
        "readers_guide": _path(args.readers_guide),
        "json_path": _path(args.json_path),
        "csv": _path(args.csv),
        "tsv": _path(args.tsv),
        "parquet": _path(args.parquet),
        "raw": _path(args.raw),
    }


def _path(value: Optional[str]) -> Optional[Path]:
    """Normalize an optional output path value."""
    if value is None:
        return None
    return Path(value)
