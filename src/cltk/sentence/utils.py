"""Helpers for dealing with sentences."""

import re
from typing import Literal


def extract_sentences_from_boundaries(
    text: str, boundaries: list[tuple[int, int]]
) -> list[str]:
    """
    Given a text and a list of (start, stop) character index tuples,
    return the list of sentence strings.
    """
    return [text[start:stop] for start, stop in boundaries]


def split_sentences_multilang(
    text: Literal[
        "akk",
        "ang",
        "arc",
        "cop" "grc",
        "hbo",
        "lat",
        "non",
        "pli",
        "san",
        "arb",
        "chu",
        "enm",
        "frm",
        "fro",
        "gmh",
        "goh",
        "got",
        "hin",
        "lzh",
        "pan",
    ],
    iso: str,
) -> list[tuple[int, int]]:
    """
    Split text into sentences for multiple languages using language-specific punctuation.
    Returns a list of (start, stop) character indices for each sentence.

    Args:
        text (str): The input text.
        lang (str): ISO code for the language.

    Returns:
        list[tuple[int, int]]: List of (start, stop) indices for each sentence.
    """
    # Define language-specific sentence-ending regex patterns
    lang_sentence_endings = {
        "grc": r"([;;·.·])",  # Greek question mark, semicolon, ano teleia, middle dot, full stop
        "lat": r"([.!?])",  # Latin: period, exclamation, question
        "san": r"([।॥.!?])",  # Sanskrit: danda, double danda, period, exclamation, question
        "pli": r"([।.!?])",  # Pali: danda, period, exclamation, question
        "hbo": r"([׃.])",  # Hebrew: sof pasuq, full stop
        "arc": r"([׃.?!])",  # Aramaic: sof pasuq (U+05C3), period, question, exclamation
        "cop": r"([⳹.!?])",  # Coptic: punctuation marks
        "non": r"([.:;!?])",  # Old Norse: period, colon, semicolon, exclamation, question
        "ang": r"([.!?])",  # Old English: period, exclamation, question
        "akk": r"([\.!?𒑰])",  # Akkadian: period, exclamation, question, and double wedge (𒑰, U+12370)
        "arb": r"([.!\u061F\u06D4])",  # Arabic: period, exclamation, Arabic question mark (؟), Arabic full stop (۔)
        "chu": r"([.!?])",  # Old Church Slavonic: period, exclamation, question
        "enm": r"([.!?])",  # Middle English: period, exclamation, question
        "frm": r"([.!?])",  # Middle French: period, exclamation, question
        "fro": r"([.!?])",  # Old French: period, exclamation, question
        "gmh": r"([.!?])",  # Middle High German: period, exclamation, question
        "goh": r"([.!?])",  # Old High German: period, exclamation, question
        "got": r"([.!?])",  # Gothic: period, exclamation, question
        "hin": r"([।.!?])",  # Hindi: danda, period, exclamation, question
        "lzh": r"([。！？])",  # Literary Chinese: full stop (。), exclamation (！), question (？)
        "pan": r"([।.!?])",  # Panjabi: danda, period, exclamation, question
    }

    if iso not in lang_sentence_endings:
        raise ValueError(f"Unsupported language code: {iso}")

    sentence_endings = lang_sentence_endings[iso]
    parts = re.split(sentence_endings, text)

    boundaries = []
    idx = 0
    for i in range(0, len(parts) - 1, 2):
        sentence = parts[i].strip() + parts[i + 1]
        if sentence:
            # Find start index (skip leading whitespace)
            while idx < len(text) and text[idx].isspace():
                idx += 1
            start = idx
            stop = start + len(sentence)
            boundaries.append((start, stop))
            idx = stop
    # Handle possible trailing text
    if len(parts) % 2 != 0 and parts[-1].strip():
        sentence = parts[-1].strip()
        if sentence:
            while idx < len(text) and text[idx].isspace():
                idx += 1
            start = idx
            stop = start + len(sentence)
            boundaries.append((start, stop))
            idx = stop

    return boundaries
