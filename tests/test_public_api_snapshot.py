from __future__ import annotations

import importlib
import importlib.util
import inspect
import json
import re
from pathlib import Path
from typing import Any


def test_top_level_api() -> None:
    cltk = importlib.import_module("cltk")
    assert hasattr(cltk, "NLP")
    assert hasattr(cltk, "__version__")


def test_public_manifest_enforced() -> None:
    manifest_path = Path("api/public_manifest.json")
    data = json.loads(manifest_path.read_text())
    assert data.get("module") == "cltk"
    allowed = set(data.get("exports", []))
    mod = importlib.import_module("cltk")
    names = {n for n in dir(mod) if not (n.startswith("__") and n.endswith("__"))}
    # Allowed names must be present (attribute access, not dir())
    for n in allowed:
        assert hasattr(mod, n)
    # Ignore submodules (namespace exposure is OK for import machinery)
    def is_submodule(n: str) -> bool:
        try:
            spec = importlib.util.find_spec(f"cltk.{n}")
            return spec is not None
        except Exception:
            return False
    extras = {n for n in names if not is_submodule(n) and not n.isupper()}
    # No extras beyond the allowed manifest
    assert extras.issubset(allowed)


def test_morphosyntax_processes_subclasses_use_glottolog_ids() -> None:
    mod = importlib.import_module("cltk.morphosyntax.processes")
    Base = getattr(mod, "GenAIMorphosyntaxProcess")
    subclasses = Base.__subclasses__()
    assert len(subclasses) >= 80

    pat = re.compile(r"^[a-z]{4}\d{4}$")
    for cls in subclasses:
        fld = getattr(cls, "model_fields", {}).get("glottolog_id")
        default_glotto: Any = getattr(fld, "default", None)
        assert isinstance(default_glotto, str) and pat.match(default_glotto), (
            f"{cls.__name__} has non-Glottolog id: {default_glotto!r}"
        )


def test_dependency_processes_subclasses_use_glottolog_ids() -> None:
    mod = importlib.import_module("cltk.dependency.processes")
    Base = getattr(mod, "GenAIDependencyProcess")
    subclasses = Base.__subclasses__()
    assert len(subclasses) >= 80

    pat = re.compile(r"^[a-z]{4}\d{4}$")
    for cls in subclasses:
        fld = getattr(cls, "model_fields", {}).get("glottolog_id")
        default_glotto: Any = getattr(fld, "default", None)
        assert isinstance(default_glotto, str) and pat.match(default_glotto), (
            f"{cls.__name__} has non-Glottolog id: {default_glotto!r}"
        )


def test_process_run_signature() -> None:
    # Morphosyntax run signature
    m = importlib.import_module("cltk.morphosyntax.processes")
    dep = importlib.import_module("cltk.dependency.processes")
    for base in (
        getattr(m, "GenAIMorphosyntaxProcess"),
        getattr(dep, "GenAIDependencyProcess"),
    ):
        sig = inspect.signature(base.run)
        params = list(sig.parameters.values())
        assert len(params) == 2  # self + input_doc
        assert params[1].name == "input_doc"
