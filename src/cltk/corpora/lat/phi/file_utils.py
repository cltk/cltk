"""Higher-level (i.e., user-friendly) functions for quickly reading
PHI5 data after it has been processed by ``TLGU()``.
"""

import os

import regex

from cltk.corpora.lat.phi.phi5_index import PHI5_INDEX, PHI5_WORKS_INDEX
from cltk.utils.file_operations import make_cltk_path


def phi5_plaintext_cleanup(text, rm_punctuation=False, rm_periods=False):
    """Remove and substitute post-processing for Latin PHI5 text.
    TODO: Surely more junk to pull out. Please submit bugs!
    TODO: This is a rather slow now, help in speeding up welcome.
    """
    # This works OK, doesn't get some
    # Note: rming all characters between {} and ()
    remove_comp = regex.compile(
        r"-\n|«|»|\<|\>|\.\.\.|‘|’|_|{.+?}|\(.+?\)|\(|\)|“|#|%|⚔|&|=|/|\\|〚|†|『|⚖|–|˘|⚕|☾|◌|◄|►|⌐|⌊|⌋|≈|∷|≈|∞|”|[0-9]"
    )
    text = remove_comp.sub("", text)

    new_text = None
    if rm_punctuation:
        new_text = ""
        punctuation = [",", ";", ":", '"', "'", "?", "-", "!", "*", "[", "]", "{", "}"]
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
    replace_comp = regex.compile(r"\n")
    text = replace_comp.sub(" ", text)

    comp_space = regex.compile(r"\s+")
    text = comp_space.sub(" ", text)

    return text


def assemble_phi5_author_filepaths():
    """Reads PHI5 index and builds a list of absolute filepaths."""
    plaintext_dir = make_cltk_path("lat/text/phi5/plaintext/")
    filepaths = [os.path.join(plaintext_dir, x + ".TXT") for x in PHI5_INDEX]
    return filepaths


def assemble_phi5_works_filepaths():
    """Reads PHI5 index and builds a list of absolute filepaths."""
    plaintext_dir = make_cltk_path("lat/text/phi5/individual_works/")
    all_filepaths = []
    for author_code in PHI5_WORKS_INDEX:
        author_data = PHI5_WORKS_INDEX[author_code]
        works = author_data["works"]
        for work in works:
            f = os.path.join(plaintext_dir, author_code + ".TXT" + "-" + work + ".txt")
            all_filepaths.append(f)
    return all_filepaths
