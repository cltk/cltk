"""Main entry point for the CLTK CLI."""

import argparse
from typing import Callable, Optional, cast

from cltk.cli import analyze, compare, export
from cltk.cli.utils import HelpFormatter


def build_parser() -> argparse.ArgumentParser:
    """Create the top-level CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="cltk",
        description="Command-line interface for CLTK pipelines and exports.",
        formatter_class=HelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze.configure_parser(subparsers)
    compare.configure_parser(subparsers)
    export.configure_parser(subparsers)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return 2
    return cast(Callable[[argparse.Namespace], int], func)(args)


if __name__ == "__main__":
    raise SystemExit(main())
