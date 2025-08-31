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
    text: str,
    glottolog_id: str,
) -> list[tuple[int, int]]:
    """
    Split text into sentences for multiple languages using language-specific punctuation.
    Returns a list of (start, stop) character indices for each sentence.

    Args:
        text (str): The input text.
        glottolog_id (str): Glottolog languoid code for the language.

    Returns:
        list[tuple[int, int]]: List of (start, stop) indices for each sentence.
    """
    # Define language-specific sentence-ending regex patterns
    lang_sentence_endings = {
        "anci1242": r"([;;·.·])",
        "lati1261": r"([.!?])",
        "sans1269": r"([।॥.!?])",  # Sanskrit: danda, double danda, period, exclamation, question
        "pali1273": r"([।॥!?])",  # Pali: danda, period, exclamation, question
        "anci1244": r"([׃.])",  # Biblical Hebrew: sof pasuq, full stop
        "impe1235": r"([׃.?!])",  # Aramaic: sof pasuq (U+05C3), period, question, exclamation
        "copt1239": r"([⳹.!?])",  # Coptic: punctuation marks
        "oldn1244": r"([.:;!?])",  # Old Norse: period, colon, semicolon, exclamation, question
        "olde1238": r"([.!?])",  # Old English: period, exclamation, question
        "akka1240": r"([\.!?𒑰])",  # Akkadian: period, exclamation, question, and double wedge (𒑰, U+12370)
        "clas1259": r"([.!\u061F\u06D4])",  # Arabic: period, exclamation, Arabic question mark (؟), Arabic full stop (۔)
        "chur1257": r"([.!?])",  # Old Church Slavonic: period, exclamation, question
        "midd1317": r"([.!?])",  # Middle English: period, exclamation, question
        "midd1316": r"([.!?])",  # Middle French: period, exclamation, question
        "oldf1239": r"([.!?])",  # Old French: period, exclamation, question
        "midd1343": r"([.!?])",  # Middle High German: period, exclamation, question
        "oldh1241": r"([.!?])",  # Old High German: period, exclamation, question
        "goth1244": r"([.!?])",  # Gothic: period, exclamation, question
        "hin": r"([।.!?])",  # Hindi: danda, period, exclamation, question
        "lite1248": r"([。！？])",  # Literary Chinese: full stop (。), exclamation (！), question (？)
        "pan": r"([।.!?])",  # Panjabi: danda, period, exclamation, question
        "demo1234": r"([.!?])",  # Demotic Egyptian: period, exclamation, question (adjust if you have more info)
        "clas1252": r"(r[܀܁܂܃܄܆܇·])",  # Classical Syriac
        "hit1242": r"([\.!?𒑰])",  # Hittite: generic (Akkadian-like) punctuation + 𒑰
        "toch1238": r"([।॥.!?])",  # Tocharian A: Brahmi danda family
        "toch1237": r"([।॥.!?])",  # Tocharian B: Brahmi danda family
        "aves1237": r"([.!?])",  # Avestan: generic punctuation
        "oldp1254": r"([.!?])",  # Old Persian: generic punctuation
        "oldi1245": r"([.!?])",  # Early Irish: Latin punctuation
        "ugar1238": r"([𒑰])",  # Ugaritic: generic punctuation
        "phoe1239": r"([𐤟])",  # Phoenician: generic punctuation
        "geez1241": r"([፡።፨])",  # Geez: generic punctuation
        "midd1369": r"([𓏛])",  # Middle Egyptian: generic punctuation
        "olde1242": r"([𓏛])",  # Old Egyptian: generic punctuation
        "late1256": r"([𓏛])",  # Late Egyptian: generic punctuation
        "clas1254": r"([།༎༏])",  # Classical Tibetan: shad, nyis shad, tsheg shad
        "pahl1241": r"([:⁘·.;:])",  # Middle Persian
        "part1239": r"([·:⁘.;:])",  # Parthian
        "aves1237": r"([·:⁘.;:])",  # Avestan
        "bact1239": r"([·:⁘.;:])",  # Bactrian
        "sogd1245": r"([·:܃⁘.;:])",  # Sogdian
        "khot1251": r"([।॥.])",  # Khotanese
        "tums1237": r"([।॥.])",  # Tumshuqese
        "oldw1239": r"([·.!?])",  # Old Welsh
        "bret1244": r"([∴.!?])",  # Old-Middle Breton
        "corn1251": r"([:.!?])",  # Cornish
        "prus1238": r"([.!?·:;])",  # Old Prussian: period, exclamation, question, middle dot, colon, semicolon
        "lith1251": r"([.!?])",  # Lithuanian: period, exclamation, question
        "latv1249": r"([.!?])",  # Latvian: period, exclamation, question
        "gheg1238": r"([.!?])",  # Albanian: period, exclamation, question
        "clas1256": r"([։՞,!;])",  # Classical Armenian: period, exclamation, question
        "midd1364": r"([։՞,!;])",  # Middle Armenian: period, exclamation, question
        "cune1239": r"(.?!:;?:\|\||§|\n+)",  # Cuneiform Luwian: double ruling, section mark, or explicit line break
        "hier1240": r"(.!;?:\|\||•|·|\n+)",  # Hieroglyphic Luwian: double ruling (sentence/section), bullet or mid-dot used in some editions, or line break
    }
    if glottolog_id not in lang_sentence_endings:
        raise ValueError(f"Unsupported language code: {glottolog_id}")

    sentence_endings = lang_sentence_endings[glottolog_id]
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
