"""Lightweight package init exposing the public API.

Goals:
- Avoid importing heavy dependencies or performing I/O at import time.
- Re-export only stable, leaf-level names.
- Define ``__all__`` to the exact public surface.
"""

from typing import TYPE_CHECKING

# Public surface: only "NLP" for normal users
__all__ = ["NLP"]

if TYPE_CHECKING:
    # For type checkers without importing heavy runtime deps
    from .nlp import NLP as NLP  # noqa: F401


def __getattr__(name: str) -> object:  # PEP 562 lazy attribute loading
    if name == "NLP":
        # Import lazily to avoid pulling heavy deps at import time
        from .nlp import NLP as _NLP

        return _NLP
    if name == "__version__":
        # Compute lazily to avoid metadata I/O at import time
        from importlib import metadata as _metadata

        try:
            return _metadata.version("cltk")
        except _metadata.PackageNotFoundError:  # during editable installs
            return "0"
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
