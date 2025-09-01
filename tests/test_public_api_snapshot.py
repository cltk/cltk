from __future__ import annotations

import importlib
import inspect
from typing import Any


def _collect_public_api() -> dict[str, Any]:
    # Top-level cltk exposure
    cltk = importlib.import_module("cltk")

    top = {
        "has_NLP": hasattr(cltk, "NLP"),
        "has___version__": hasattr(cltk, "__version__"),
    }

    # ChatGPT process surface and subclasses
    processes = importlib.import_module("cltk.genai.processes")
    ChatGPTProcess = getattr(processes, "ChatGPTProcess")

    # Lock the field names and the run() signature
    fields = sorted(getattr(ChatGPTProcess, "model_fields").keys())
    run_sig = str(inspect.signature(ChatGPTProcess.run))

    # Lock the set of subclasses and their default glottolog_id values
    subclasses_info = []
    for cls in sorted(ChatGPTProcess.__subclasses__(), key=lambda c: c.__name__):
        fld = getattr(cls, "model_fields", {}).get("glottolog_id")
        default_glotto = getattr(fld, "default", None)
        subclasses_info.append({
            "name": cls.__name__,
            "glottolog_id": default_glotto,
        })

    return {
        "top_level": top,
        "ChatGPTProcess": {
            "fields": fields,
            "run_signature": run_sig,
            "subclasses": subclasses_info,
        },
    }


def test_public_api_snapshot(snapshot):  # type: ignore[no-untyped-def]
    data = _collect_public_api()
    assert data == snapshot
