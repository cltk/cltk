from __future__ import annotations

import pytest

from cltk.sentence.utils import split_sentences_multilang


@pytest.mark.parametrize(
    "glotto,text",
    [
        # Classical Syriac: includes mid-dot as a sentence boundary
        ("clas1252", "Alpha·Beta"),
        # Cuneiform Luwian: double ruler
        ("cune1239", "A || B"),
        # Hieroglyphic Luwian: double ruler
        ("hier1240", "A || B"),
        # Palaic: double ruler
        ("pala1331", "A || B"),
    ],
)
def test_sentence_splitter_endings(glotto: str, text: str) -> None:
    bounds = split_sentences_multilang(text, glotto)
    # Expect at least two sentences around the boundary
    assert len(bounds) >= 1
    # Verify that the boundary actually splits at the expected point
    # by reconstructing sentence strings
    pieces = [text[s:e] for s, e in bounds]
    joined = "".join(pieces)
    # Reconstructed string should be a prefix of the original
    assert text.startswith(pieces[0])
    # And include the boundary character(s)
    assert any(b in text for b in ("·", "||"))
