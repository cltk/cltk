"""CLI handler for the ``cltk pipeline`` subcommand."""

import argparse

from cltk.cli.utils import HelpFormatter
from cltk.core.process_registry import ProcessRegistry
from cltk.pipeline.compiler import compile_pipeline
from cltk.pipeline.presets import list_presets
from cltk.pipeline.spec_io import load_pipeline_spec


def configure_parser(subparsers: argparse._SubParsersAction) -> None:
    """Register the pipeline subcommand parser."""
    parser = subparsers.add_parser(
        "pipeline",
        help="Inspect and validate declarative pipeline specs.",
        formatter_class=HelpFormatter,
    )
    nested = parser.add_subparsers(dest="pipeline_command", required=True)

    describe = nested.add_parser(
        "describe",
        help="Describe the steps in a pipeline spec.",
        formatter_class=HelpFormatter,
    )
    describe.add_argument("--toml", required=True, help="Path to pipeline TOML.")
    describe.set_defaults(func=_describe)

    validate = nested.add_parser(
        "validate",
        help="Validate a pipeline spec.",
        formatter_class=HelpFormatter,
    )
    validate.add_argument("--toml", required=True, help="Path to pipeline TOML.")
    validate.set_defaults(func=_validate)

    presets = nested.add_parser(
        "presets",
        help="List available pipeline presets.",
        formatter_class=HelpFormatter,
    )
    presets.set_defaults(func=_list_presets)


def _describe(args: argparse.Namespace) -> int:
    """Print a human-friendly description of the pipeline spec."""
    spec = load_pipeline_spec(args.toml)
    pipeline = compile_pipeline(spec)
    for line in pipeline.describe():
        print(line)
    return 0


def _validate(args: argparse.Namespace) -> int:
    """Validate that all steps in a spec are registered processes."""
    spec = load_pipeline_spec(args.toml)
    steps = spec.steps or []
    missing = [
        step.id for step in steps if step.id not in ProcessRegistry.list_processes()
    ]
    if missing:
        available = ", ".join(sorted(ProcessRegistry.list_processes()))
        raise SystemExit(
            f"Unknown process_id(s): {', '.join(missing)}. Available: {available}"
        )
    return 0


def _list_presets(_: argparse.Namespace) -> int:
    """Print available pipeline preset names."""
    for preset in list_presets():
        print(preset)
    return 0
