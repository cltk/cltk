"""CLI handler for the ``cltk analyze`` subcommand."""

import argparse
import sys
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
from cltk.core.data_types import CLTKConfig, Doc


def configure_parser(subparsers: argparse._SubParsersAction) -> None:
    """Register the analyze subcommand parser."""
    parser = subparsers.add_parser(
        "analyze",
        help="Run a CLTK pipeline on text and emit a chosen output format.",
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
    parser.add_argument("--input-dir", help="Batch mode: directory of input files.")
    parser.add_argument(
        "--glob",
        default="*.txt",
        help="Glob pattern for --input-dir (default: *.txt).",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output type (raw, conllu, readers-guide, feature-table, json).",
    )
    parser.add_argument(
        "--format",
        help="Format for feature-table (csv, tsv, parquet) or json (pretty, min).",
    )
    parser.add_argument(
        "--out-file",
        help="Write output to this path; defaults to stdout.",
    )
    parser.add_argument(
        "--out-dir",
        help="Output directory for batch mode (--input-dir).",
    )
    parser.add_argument(
        "--config",
        help="JSON string or path to JSON file for backend/pipeline settings.",
    )
    parser.add_argument(
        "--max-sentences",
        type=int,
        help="Cap the number of sentences in output.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Cap the number of tokens per sentence in output.",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue processing batch inputs after errors.",
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
    """Run the analyze command."""
    set_log_level(quiet=args.quiet, verbose=args.verbose)
    if args.max_sentences is not None and args.max_sentences <= 0:
        raise SystemExit("--max-sentences must be a positive integer.")
    if args.max_tokens is not None and args.max_tokens <= 0:
        raise SystemExit("--max-tokens must be a positive integer.")
    config = parse_json_input(args.config) if args.config else None
    pipeline = resolve_pipeline(args.pipeline) if args.pipeline else None
    cltk_config = build_cltk_config(
        language=args.language,
        backend=args.backend,
        config=config,
        pipeline=pipeline,
    )

    if args.input_dir:
        return _run_batch(args, cltk_config)

    if args.out_dir:
        raise SystemExit("--out-dir is only valid with --input-dir.")

    text = load_text(args.text, args.text_file)
    try:
        nlp = NLP(cltk_config=cltk_config, suppress_banner=True)
        doc = nlp.analyze(text)
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
    _emit_output(doc, args, out_path=_resolve_out_path(args.out_file))
    return 0


def _run_batch(args: argparse.Namespace, cltk_config: CLTKConfig) -> int:
    """Run batch analysis over an input directory."""
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        raise SystemExit(f"Input directory not found: {input_dir}")
    if not input_dir.is_dir():
        raise SystemExit(f"Input path is not a directory: {input_dir}")
    if args.text or args.text_file:
        raise SystemExit("Batch mode does not accept --text or --text-file.")
    if not args.out_dir:
        raise SystemExit("Batch mode requires --out-dir.")
    if args.out_file:
        raise SystemExit("Batch mode does not accept --out-file.")

    try:
        fmt = dispatch.resolve_format(args.out, args.format)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    out_dir = Path(args.out_dir)
    pattern = args.glob or "*.txt"
    files = sorted(input_dir.rglob(pattern))
    if not files:
        raise SystemExit(f"No input files matched '{pattern}'.")

    try:
        nlp = NLP(cltk_config=cltk_config, suppress_banner=True)
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
    for path in files:
        if not path.is_file():
            continue
        rel_path = path.relative_to(input_dir)
        out_path = out_dir / rel_path
        out_path = out_path.with_suffix(_output_extension(args.out, fmt))
        try:
            text = path.read_text(encoding="utf-8")
            if not text.strip():
                raise ValueError("Input text is empty.")
            doc = nlp.analyze(text)
            _emit_output(doc, args, out_path=out_path, format_override=fmt)
        except Exception as exc:
            if args.continue_on_error:
                print(f"Error processing {path}: {exc}", file=sys.stderr)
                continue
            raise SystemExit(f"Error processing {path}: {exc}") from exc
    return 0


def _emit_output(
    doc: Doc,
    args: argparse.Namespace,
    *,
    out_path: Optional[Path],
    format_override: Optional[str] = None,
) -> None:
    """Render and write the selected output format."""
    out_name = dispatch.normalize_output_name(args.out)
    try:
        fmt = format_override or dispatch.resolve_format(out_name, args.format)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if out_name == "feature-table" and fmt == "parquet" and out_path is None:
        raise SystemExit("Parquet output requires --out-file or --out-dir.")

    if out_name == "feature-table":
        if fmt == "parquet":
            try:
                require_parquet_deps()
            except RuntimeError as exc:
                raise SystemExit(str(exc)) from exc
        try:
            table = dispatch.render_output(
                doc,
                out_name,
                max_sentences=args.max_sentences,
                max_tokens=args.max_tokens,
            )
        except ImportError as exc:
            raise SystemExit(str(exc)) from exc
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        if fmt == "parquet":
            try:
                assert out_path is not None
                write_feature_table_parquet(table, out_path)
            except RuntimeError as exc:
                raise SystemExit(str(exc)) from exc
            return
        delimiter = "," if fmt == "csv" else "\t"
        write_feature_table_csv(table, out_path=out_path, delimiter=delimiter)
        return

    if out_name == "json":
        try:
            payload = dispatch.render_output(
                doc,
                out_name,
                max_sentences=args.max_sentences,
                max_tokens=args.max_tokens,
            )
            data = dispatch.ensure_json_payload(payload, out_name)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        pretty = fmt != "min"
        write_json_output(data, out_path, pretty=pretty)
        return

    try:
        payload = dispatch.render_output(
            doc,
            out_name,
            max_sentences=args.max_sentences,
            max_tokens=args.max_tokens,
        )
        output = dispatch.ensure_text_payload(payload, out_name)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    write_text_output(output, out_path)


def _resolve_out_path(value: Optional[str]) -> Optional[Path]:
    """Normalize an output path string."""
    if value is None:
        return None
    return Path(value)


def _output_extension(out_name: str, fmt: Optional[str]) -> str:
    """Map output settings to a file extension."""
    out = dispatch.normalize_output_name(out_name)
    if out == "conllu":
        return ".conllu"
    if out == "readers-guide":
        return ".md"
    if out == "json":
        return ".json"
    if out == "feature-table":
        if fmt == "parquet":
            return ".parquet"
        if fmt == "tsv":
            return ".tsv"
        return ".csv"
    return ".txt"
