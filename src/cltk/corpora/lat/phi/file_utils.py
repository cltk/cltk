"""Higher-level (i.e., user-friendly) functions for quickly reading
PHI5 data after it has been processed by ``TLGU()``.
"""

import os
from typing import Optional, Union

import regex
from regex import Pattern

from cltk.corpora.lat.phi.phi5_index import (
    MAP_PHI5_AUTHOR_ID_TO_NAME,
    MAP_PHI5_AUTHOR_ID_TO_WORKS_AND_NAME,
)
from cltk.utils.file_operations import make_cltk_path


def phi5_plaintext_cleanup(
    text, rm_punctuation: bool = False, rm_periods: bool = False
) -> str:
    """Remove and substitute post-processing for Latin PHI5 text.
    TODO: Surely more junk to pull out. Please submit bugs!
    TODO: This is a rather slow now, help in speeding up welcome.
    """
    # This works OK, doesn't get some
    # Note: rming all characters between {} and ()
    remove_comp: Pattern[str] = regex.compile(
        r"-\n|«|»|\<|\>|\.\.\.|‘|’|_|{.+?}|\(.+?\)|\(|\)|“|#|%|⚔|&|=|/|\\|〚|†|『|⚖|–|˘|⚕|☾|◌|◄|►|⌐|⌊|⌋|≈|∷|≈|∞|”|[0-9]"
    )
    text = remove_comp.sub("", text)

    new_text: Optional[str] = None
    if rm_punctuation:
        new_text = ""
        punctuation: list[str] = [
            ",",
            ";",
            ":",
            '"',
            "'",
            "?",
            "-",
            "!",
            "*",
            "[",
            "]",
            "{",
            "}",
        ]
        if rm_periods:
            punctuation += ["."]
        for char in text:
            # rm acute combining acute accents made by TLGU
            # Could be caught by regex, tried and failed, not sure why
            if bytes(char, "utf-8") == b"\xcc\x81":
                pass
            # second try at rming some punctuation; merge with above regex
            elif char in punctuation:
                pass
            else:
                new_text += char
    if new_text:
        text = new_text

    # replace line breaks w/ space
    replace_comp: Pattern[str] = regex.compile(r"\n")
    text = replace_comp.sub(" ", text)

    comp_space: Pattern[str] = regex.compile(r"\s+")
    text = comp_space.sub(" ", text)

    return text


def assemble_phi5_author_filepaths() -> list[str]:
    """Reads PHI5 index and builds a list of absolute filepaths."""
    plaintext_dir: str = make_cltk_path("lat/text/phi5/plaintext/")
    filepaths: list[str] = [
        os.path.join(plaintext_dir, x + ".TXT") for x in MAP_PHI5_AUTHOR_ID_TO_NAME
    ]
    return filepaths


def assemble_phi5_works_filepaths() -> list[str]:
    """Reads PHI5 index and builds a list of absolute filepaths."""
    plaintext_dir: str = make_cltk_path("lat/text/phi5/individual_works/")
    all_filepaths: list[str] = list()
    for author_code in MAP_PHI5_AUTHOR_ID_TO_WORKS_AND_NAME:
        author_data: dict[
            str, Union[list[str], str]
        ] = MAP_PHI5_AUTHOR_ID_TO_WORKS_AND_NAME[author_code]
        works: Union[list[str], str] = author_data["works"]
        for work in works:
            filepath: str = os.path.join(
                plaintext_dir, author_code + ".TXT" + "-" + work + ".txt"
            )
            all_filepaths.append(filepath)
    return all_filepaths
