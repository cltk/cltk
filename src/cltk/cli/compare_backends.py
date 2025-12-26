"""CLI for comparing CLTK backends on the same text."""

import argparse
from pathlib import Path
from typing import Any, Optional

from cltk.evaluation.compare_backends import (
    compare_backends,
    report_to_markdown,
    write_report,
)


def main(argv: Optional[list[str]] = None) -> int:
    """Run the compare-backends CLI."""
    args = _parse_args(argv)
    text = _load_text(args)
    backends = _parse_backends(args.backends)
    _validate_limits(args)
    configs: dict[str, dict[str, Any]] = {}
    if args.seed is not None:
        configs = _seed_overrides(backends, args.seed)

    report = compare_backends(
        args.language,
        text,
        backends,
        configs=configs or None,
        max_sentences=args.max_sentences,
        max_tokens=args.max_tokens,
    )

    if args.out_dir:
        write_report(report, args.out_dir)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report_to_markdown(report))
    if not args.out and not args.out_dir:
        print(report_to_markdown(report))
    return 0


def _parse_args(argv: Optional[list[str]]) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        prog="cltk.compare_backends",
        description="Compare CLTK NLP backends on the same text.",
    )
    parser.add_argument("--language", required=True, help="Glottolog language id.")
    parser.add_argument(
        "--text",
        help="Raw text to analyze.",
    )
    parser.add_argument(
        "--text-file",
        help="Path to a text file to analyze.",
    )
    parser.add_argument(
        "--backends",
        required=True,
        help="Comma-separated backend list (e.g., stanza,openai,ollama).",
    )
    parser.add_argument("--out", help="Write Markdown report to this path.")
    parser.add_argument(
        "--out-dir",
        help="Write JSON, Markdown, and CSV reports to this directory.",
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
        "--seed",
        type=int,
        help="Deterministic seed for backends that support it.",
    )
    return parser.parse_args(argv)


def _load_text(args: argparse.Namespace) -> str:
    """Load input text from args or file."""
    if args.text and args.text_file:
        raise SystemExit("Provide either --text or --text-file, not both.")
    if args.text_file:
        text = Path(args.text_file).read_text()
    elif args.text:
        text = args.text
    else:
        raise SystemExit("Provide --text or --text-file.")
    if not text.strip():
        raise SystemExit("Input text is empty.")
    return text


def _parse_backends(value: str) -> list[str]:
    """Parse comma-separated backend list."""
    backends = [part.strip() for part in value.split(",") if part.strip()]
    if not backends:
        raise SystemExit("No backends provided.")
    return backends


def _validate_limits(args: argparse.Namespace) -> None:
    """Validate max-sentences and max-tokens settings."""
    if args.max_sentences is not None and args.max_sentences <= 0:
        raise SystemExit("--max-sentences must be a positive integer.")
    if args.max_tokens is not None and args.max_tokens <= 0:
        raise SystemExit("--max-tokens must be a positive integer.")


def _seed_overrides(backends: list[str], seed: int) -> dict[str, dict[str, Any]]:
    """Build per-backend seed overrides."""
    configs: dict[str, dict[str, Any]] = {}
    for backend in backends:
        if backend == "mistral":
            configs.setdefault(backend, {})["random_seed"] = seed
        elif backend in ("ollama", "ollama-cloud"):
            cfg = configs.setdefault(backend, {})
            options = cfg.get("options")
            if not isinstance(options, dict):
                options = {}
                cfg["options"] = options
            options.setdefault("seed", seed)
    return configs


if __name__ == "__main__":
    raise SystemExit(main())
