"""Shared helpers for CLTK CLI commands."""

import argparse
import csv
import importlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Optional

from cltk.core.cltk_logger import logger
from cltk.core.data_types import CLTKConfig, Pipeline

BACKEND_CHOICES: set[str] = {
    "stanza",
    "openai",
    "ollama",
    "ollama-cloud",
    "mistral",
    "spacy",
}


def set_log_level(*, quiet: bool, verbose: bool) -> None:
    """Adjust CLTK logger verbosity based on CLI flags."""
    if quiet and verbose:
        raise SystemExit("Use --quiet or --verbose, not both.")
    if quiet:
        logger.setLevel("ERROR")
    elif verbose:
        logger.setLevel("INFO")


def parse_json_input(value: str) -> dict[str, Any]:
    """Parse a JSON string or JSON file path into a dict."""
    raw = value.strip()
    try:
        if raw.startswith("{") or raw.startswith("["):
            parsed = json.loads(raw)
        else:
            parsed = json.loads(Path(raw).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Config file not found: {value}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in config: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit("Config JSON must be an object (mapping).")
    return parsed


def load_text(text: Optional[str], text_file: Optional[str]) -> str:
    """Load input text from flags or stdin."""
    if text and text_file:
        raise SystemExit("Provide either --text or --text-file, not both.")
    if text_file:
        try:
            text_value = Path(text_file).read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise SystemExit(f"Text file not found: {text_file}") from exc
    elif text:
        text_value = text
    elif not sys.stdin.isatty():
        text_value = sys.stdin.read()
    else:
        raise SystemExit("Provide --text, --text-file, or pipe text to stdin.")
    if not text_value.strip():
        raise SystemExit("Input text is empty.")
    return text_value


def parse_backends(value: str) -> list[str]:
    """Parse comma-separated backend list."""
    parts = [part.strip() for part in value.split(",") if part.strip()]
    if not parts:
        raise SystemExit("No backends provided.")
    return [normalize_backend(part) for part in parts]


def normalize_backend(backend: str) -> str:
    """Normalize and validate backend name."""
    value = backend.strip().lower()
    if value not in BACKEND_CHOICES:
        allowed = ", ".join(sorted(BACKEND_CHOICES))
        raise SystemExit(f"Unsupported backend '{value}'. Choose from: {allowed}.")
    return value


def resolve_pipeline(name: str) -> Pipeline:
    """Resolve a pipeline class name from ``cltk.languages.pipelines``."""
    from cltk.languages import pipelines

    candidate = getattr(pipelines, name, None)
    if candidate is None:
        raise SystemExit(f"Unknown pipeline '{name}'.")
    if not isinstance(candidate, type) or not issubclass(candidate, Pipeline):
        raise SystemExit(f"'{name}' is not a Pipeline class.")
    return candidate()


def build_cltk_config(
    *,
    language: str,
    backend: str,
    config: Optional[dict[str, Any]],
    pipeline: Optional[Pipeline],
) -> CLTKConfig:
    """Construct a ``CLTKConfig`` from CLI args and optional overrides."""
    normalized_backend = normalize_backend(backend)
    data: dict[str, Any] = {}
    if config:
        config_keys = {
            "language_code",
            "backend",
            "model",
            "custom_pipeline",
            "suppress_banner",
            "stanza",
            "openai",
            "mistral",
            "ollama",
        }
        if config_keys.intersection(config.keys()):
            data.update(config)
        else:
            data[normalized_backend] = config
    data["language_code"] = language
    data["backend"] = normalized_backend
    data["suppress_banner"] = True
    if pipeline is not None:
        data["custom_pipeline"] = pipeline
    try:
        return CLTKConfig(**data)
    except Exception as exc:
        raise SystemExit(str(exc)) from exc


def feature_table_rows(table: Any) -> tuple[list[str], list[dict[str, Any]]]:
    """Return column names and rows for a pyarrow-style table."""
    rows = table.to_pylist() if hasattr(table, "to_pylist") else None
    if rows is None or not isinstance(rows, list):
        raise SystemExit("Unsupported feature table object; expected pyarrow.Table.")
    columns = getattr(table, "column_names", None)
    if not columns:
        columns = sorted({key for row in rows for key in row.keys()})
    return list(columns), rows


def write_text_output(text: str, out_path: Optional[Path]) -> None:
    """Write text to a file or stdout."""
    if out_path is None:
        sys.stdout.write(text)
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")


def write_json_output(
    data: dict[str, Any],
    out_path: Optional[Path],
    *,
    pretty: bool,
) -> None:
    """Write JSON to a file or stdout."""
    if pretty:
        payload = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
    else:
        payload = json.dumps(
            data,
            separators=(",", ":"),
            sort_keys=True,
            ensure_ascii=False,
        )
    payload += "\n"
    write_text_output(payload, out_path)


def write_feature_table_csv(
    table: Any,
    *,
    out_path: Optional[Path],
    delimiter: str,
) -> None:
    """Write a feature table to CSV/TSV using stdlib csv."""
    columns, rows = feature_table_rows(table)
    if out_path is None:
        writer = csv.DictWriter(sys.stdout, fieldnames=columns, delimiter=delimiter)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, delimiter=delimiter)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _module_available(name: str) -> bool:
    """Return whether a module can be imported."""
    return importlib.util.find_spec(name) is not None


def require_parquet_deps() -> tuple[Any, Any]:
    """Return pandas and pyarrow modules or raise a clear error."""
    if not _module_available("pandas") or not _module_available("pyarrow"):
        raise RuntimeError("Parquet export requires pandas and pyarrow.")
    pandas = importlib.import_module("pandas")
    pyarrow = importlib.import_module("pyarrow")
    return pandas, pyarrow


def write_feature_table_parquet(table: Any, out_path: Path) -> None:
    """Write a feature table to parquet using pandas + pyarrow."""
    pandas, _ = require_parquet_deps()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not hasattr(table, "to_pandas"):
        raise SystemExit(
            "Feature table export expected a pyarrow.Table; got unsupported object."
        )
    df = table.to_pandas()
    df.to_parquet(out_path, index=False)


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Help formatter with raw description support."""

    pass
