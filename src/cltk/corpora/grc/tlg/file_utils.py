"""Higher-level (i.e., user-friendly) functions for quickly reading
TLG data after it has been processed by ``TLGU()``.
"""

import os

import regex

from cltk.corpora.grc.tlg.tlg_index import TLG_INDEX, TLG_WORKS_INDEX
from cltk.utils.file_operations import make_cltk_path


def tlg_plaintext_cleanup(text, rm_punctuation=False, rm_periods=False):
    """Remove and substitute post-processing for Greek TLG text.
    TODO: Surely more junk to pull out. Please submit bugs!
    """
    remove_comp = regex.compile(
        r"-\n|[«»<>〈〉\(\)‘’_—:!\?\'\"\*]|{[[:print:][:space:]]+?}|\[[[:print:][:space:]]+?\]|[a-zA-Z0-9]",
        flags=regex.VERSION1,
    )
    text = remove_comp.sub("", text)

    if rm_punctuation:
        punct_comp = regex.compile(r",|·")
        text = punct_comp.sub("", text)

    if rm_periods:
        period_comp = regex.compile(r"\.|;")
        text = period_comp.sub("", text)

    # replace line breaks w/ space
    replace_comp = regex.compile(r"\n")
    text = replace_comp.sub(" ", text)

    comp_space = regex.compile(r"\s+")
    text = comp_space.sub(" ", text)

    return text


def assemble_tlg_author_filepaths():
    """Reads TLG index and builds a list of absolute filepaths."""
    plaintext_dir = make_cltk_path("grc/text/tlg/plaintext/")
    filepaths = [os.path.join(plaintext_dir, x + ".TXT") for x in TLG_INDEX]
    return filepaths


def assemble_tlg_works_filepaths():
    """Reads TLG index and builds a list of absolute filepaths."""
    plaintext_dir = make_cltk_path("grc/text/tlg/individual_works/")
    all_filepaths = []
    for author_code in TLG_WORKS_INDEX:
        author_data = TLG_WORKS_INDEX[author_code]
        works = author_data["works"]
        for work in works:
            f = os.path.join(plaintext_dir, author_code + ".TXT" + "-" + work + ".txt")
            all_filepaths.append(f)
    return all_filepaths
