from __future__ import annotations

import importlib
import inspect
import re
from typing import Any


def test_top_level_api() -> None:
    cltk = importlib.import_module("cltk")
    assert hasattr(cltk, "NLP")
    assert hasattr(cltk, "__version__")


def test_morphosyntax_processes_subclasses_use_glottolog_ids() -> None:
    mod = importlib.import_module("cltk.morphosyntax.processes")
    Base = getattr(mod, "ChatGPTMorphosyntaxProcess")
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
    Base = getattr(mod, "ChatGPTDependencyProcess")
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
        getattr(m, "ChatGPTMorphosyntaxProcess"),
        getattr(dep, "ChatGPTDependencyProcess"),
    ):
        sig = inspect.signature(base.run)
        params = list(sig.parameters.values())
        assert len(params) == 2  # self + input_doc
        assert params[1].name == "input_doc"
