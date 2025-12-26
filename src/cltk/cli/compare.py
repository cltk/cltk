"""CLI handler for the ``cltk compare`` subcommand."""

import argparse
import json
from pathlib import Path
from typing import Any, Optional

from cltk.cli.utils import (
    HelpFormatter,
    load_text,
    normalize_backend,
    parse_backends,
    parse_json_input,
    set_log_level,
)
from cltk.evaluation.compare_backends import compare_backends, report_to_markdown


def configure_parser(subparsers: argparse._SubParsersAction) -> None:
    """Register the compare subcommand parser."""
    parser = subparsers.add_parser(
        "compare",
        help="Compare multiple CLTK backends on the same text.",
        formatter_class=HelpFormatter,
    )
    parser.add_argument(
        "--lang",
        "--language",
        dest="language",
        required=True,
        help="Glottolog language id.",
    )
    parser.add_argument("--text", help="Raw text to analyze.")
    parser.add_argument("--text-file", help="Path to a text file to analyze.")
    parser.add_argument(
        "--backends",
        required=True,
        help="Comma-separated backend list (e.g., stanza,openai,ollama).",
    )
    parser.add_argument(
        "--configs",
        help="JSON string or path to JSON file with per-backend overrides.",
    )
    parser.add_argument("--out-dir", help="Directory for report outputs.")
    parser.add_argument(
        "--basename",
        default="compare_backends",
        help="Base filename for outputs (default: compare_backends).",
    )
    parser.add_argument(
        "--format",
        choices=["md", "json", "both"],
        default="md",
        help="Output format (md, json, both).",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Number of top disagreements to include.",
    )
    parser.add_argument(
        "--max-sentences",
        type=int,
        help="Cap the number of sentences compared.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Cap the number of tokens per sentence.",
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
    """Run the compare command."""
    set_log_level(quiet=args.quiet, verbose=args.verbose)
    _validate_limits(args)
    if args.top_n <= 0:
        raise SystemExit("--top-n must be a positive integer.")
    text = load_text(args.text, args.text_file)
    backends = parse_backends(args.backends)
    configs = _parse_configs(args.configs)

    try:
        report = compare_backends(
            args.language,
            text,
            backends,
            configs=configs or None,
            max_sentences=args.max_sentences,
            max_tokens=args.max_tokens,
            top_n=args.top_n,
        )
    except Exception as exc:
        raise SystemExit(str(exc)) from exc

    if args.out_dir:
        _write_reports(report, args.out_dir, args.basename, args.format)
        return 0

    if args.format == "both":
        raise SystemExit("--format both requires --out-dir.")
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report_to_markdown(report))
    return 0


def _parse_configs(value: Optional[str]) -> Optional[dict[str, Any]]:
    """Parse backend overrides from JSON input."""
    if not value:
        return None
    parsed = parse_json_input(value)
    normalized: dict[str, Any] = {}
    for backend, overrides in parsed.items():
        if not isinstance(overrides, dict):
            raise SystemExit(
                f"Overrides for backend '{backend}' must be a JSON object."
            )
        normalized[normalize_backend(backend)] = overrides
    return normalized


def _write_reports(
    report: dict[str, Any],
    out_dir: str,
    basename: str,
    fmt: str,
) -> None:
    """Write report outputs in the selected formats."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    if fmt in ("json", "both"):
        json_path = out_path / f"{basename}.json"
        json_path.write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
    if fmt in ("md", "both"):
        md_path = out_path / f"{basename}.md"
        md_path.write_text(report_to_markdown(report), encoding="utf-8")


def _validate_limits(args: argparse.Namespace) -> None:
    """Validate sentence and token limits."""
    if args.max_sentences is not None and args.max_sentences <= 0:
        raise SystemExit("--max-sentences must be a positive integer.")
    if args.max_tokens is not None and args.max_tokens <= 0:
        raise SystemExit("--max-tokens must be a positive integer.")
