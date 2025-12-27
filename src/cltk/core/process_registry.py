"""Registry for mapping process IDs to concrete Process classes."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, ClassVar

from cltk.core.cltk_logger import logger

if TYPE_CHECKING:  # pragma: no cover - import only for typing
    from cltk.core.data_types import Process


class ProcessRegistry:
    """Central mapping of process_id to Process class."""

    _registry: ClassVar[dict[str, type["Process"]]] = {}
    _loaded_defaults: ClassVar[bool] = False
    _default_modules: ClassVar[tuple[str, ...]] = (
        "cltk.text.processes",
        "cltk.sentence.processes",
        "cltk.morphosyntax.processes",
        "cltk.dependency.processes",
        "cltk.translation.processes",
        "cltk.enrichment.processes",
        "cltk.stanza.processes",
    )

    @classmethod
    def register(cls, process_cls: type["Process"]) -> type["Process"]:
        """Register a Process class by its ``process_id``."""
        process_id = getattr(process_cls, "process_id", None)
        if not process_id or not isinstance(process_id, str):
            raise ValueError(
                f"Process class {process_cls.__name__} must define process_id."
            )
        existing = cls._registry.get(process_id)
        if existing and existing is not process_cls:
            raise ValueError(
                f"process_id '{process_id}' already registered for {existing.__name__}."
            )
        cls._registry[process_id] = process_cls
        logger.debug("Registered process_id '%s' -> %s", process_id, process_cls)
        return process_cls

    @classmethod
    def get_process(cls, process_id: str) -> type["Process"]:
        """Return the registered Process class for ``process_id``."""
        cls._ensure_defaults_loaded()
        try:
            return cls._registry[process_id]
        except KeyError as exc:
            available = ", ".join(sorted(cls._registry))
            raise KeyError(
                f"Unknown process_id '{process_id}'. Available: {available}"
            ) from exc

    @classmethod
    def list_processes(cls) -> dict[str, type["Process"]]:
        """Return a snapshot of registered processes."""
        cls._ensure_defaults_loaded()
        return dict(cls._registry)

    @classmethod
    def _ensure_defaults_loaded(cls) -> None:
        """Import default process modules once to populate the registry."""
        if cls._loaded_defaults:
            return
        for module in cls._default_modules:
            try:
                importlib.import_module(module)
            except Exception:
                continue
        cls._loaded_defaults = True


def register_process(process_cls: type["Process"]) -> type["Process"]:
    """Decorate a Process class to register in the ProcessRegistry."""
    return ProcessRegistry.register(process_cls)
