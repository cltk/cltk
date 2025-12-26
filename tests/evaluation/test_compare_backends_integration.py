import importlib.util
import os

import pytest

from cltk.evaluation.compare_backends import compare_backends


@pytest.mark.skipif(
    importlib.util.find_spec("stanza") is None,
    reason="Stanza is not installed.",
)
def test_compare_backends_stanza_local() -> None:
    report = compare_backends(
        "lati1261",
        "Gallia est omnis divisa in partes tres.",
        ["stanza"],
        max_sentences=1,
        max_tokens=20,
    )
    assert report["sentences"]
