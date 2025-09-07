from __future__ import annotations

import importlib
import inspect
import re
from typing import Any


def test_top_level_api() -> None:
    cltk = importlib.import_module("cltk")
    assert hasattr(cltk, "NLP")
    assert hasattr(cltk, "__version__")


def test_gpt_process_hierarchy() -> None:
    processes = importlib.import_module("cltk.genai.processes")
    GPTProcess = getattr(processes, "GPTProcess")
    LocalGPTProcess = getattr(processes, "LocalGPTProcess")

    # Types must exist and form the expected hierarchy
    from cltk.core.data_types import Process as CLTKProcess

    assert issubclass(GPTProcess, CLTKProcess)
    assert issubclass(LocalGPTProcess, GPTProcess)


def test_gpt_process_has_no_required_contract_beyond_base() -> None:
    processes = importlib.import_module("cltk.genai.processes")
    GPTProcess = getattr(processes, "GPTProcess")
    # At minimum, the class should be instantiable with defaults (pydantic BaseModel semantics)
    # and provide a .run method or allow subclasses to implement it.
    # Here we simply assert the attribute exists on the class MRO (may be inherited).
    assert hasattr(GPTProcess, "run")


def test_genai_processes_module_surface() -> None:
    processes = importlib.import_module("cltk.genai.processes")
    # Ensure the minimal public surface is present
    assert hasattr(processes, "GPTProcess")
    assert hasattr(processes, "LocalGPTProcess")
