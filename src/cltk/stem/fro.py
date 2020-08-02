"""Stemmer for Old French."""
import re

__author__ = ["Natasha Voake <natashavoake@gmail.com>"]
__license__ = "MIT License. See LICENSE."

EXCEPTIONS = [
    "mer",
    "certes",
    "mais",
    "vos",
    "onques",
    "nos",
    "talent",
    "omnipotent",
    "jadis",
    "et",
    "je",
    "certes",
    "que",
    "mais",
    "ne",
    "me",
    "de",
    "ce",
    "qui",
    "la",
    "li",
    "le",
    "ma",
    "mon",
    "si",
    "sa",
    "son",
    "chambre",
    "quant",
    "ki",
    "tut",
]


def _matchremove_noun_endings(word: str) -> str:
    """Remove the noun and adverb word endings"""

    was_stemmed = False

    """common and proper noun and adjective word endings sorted by charlen, then alph"""
    noun_endings = [
        "arons",
        "ains",
        "aron",
        "ment",
        "ain",
        "age",
        "on",
        "es",
        "ée",
        "ee",
        "ie",
        "s",
    ]

    for ending in noun_endings:
        """ignore exceptions"""
        if word in EXCEPTIONS:
            word = word
            was_stemmed = True
            break
        if word == ending:
            word = word
            was_stemmed = True
            break
        """removes noun endings"""
        if word.endswith(ending):
            word = re.sub(r"{0}$".format(ending), "", word)
            was_stemmed = True
            break

    return word, was_stemmed


def _matchremove_verb_endings(word: str) -> str:
    """Remove the verb endings"""
    """verb endings sorted by charlen then alph"""
    verb_endings = [
        "issiiens",
        "isseient",
        "issiiez",
        "issons",
        "issent",
        "issant",
        "isseie",
        "isseit",
        "issons",
        "isseiz",
        "assent",
        "issons",
        "isseiz",
        "issent",
        "iiens",
        "eient",
        "issez",
        "oient",
        "istes",
        "ïstes",
        "istes",
        "astes",
        "erent",
        "istes",
        "irent",
        "ustes",
        "urent",
        "âmes",
        "âtes",
        "èrent",
        "asses",
        "isses",
        "issez",
        "ssons",
        "sseiz",
        "ssent",
        "erent",
        "eies",
        "iiez",
        "oies",
        "iens",
        "ions",
        "oint",
        "eret",
        "imes",
        "rent",
        "ümes",
        "ütes",
        "ïmes",
        "imes",
        "asse",
        "isse",
        "usse",
        "ames",
        "imes",
        "umes",
        "asse",
        "isse",
        "sses",
        "ssez",
        "ons",
        "ent",
        "ant",
        "eie",
        "eit",
        "int",
        "ist",
        "eiz",
        "oie",
        "oit",
        "iez",
        "ois",
        "oit",
        "iez",
        "res",
        "ert",
        "ast",
        "ist",
        "sse",
        "mes",
        "er",
        "es",
        "et",
        "ez",
        "is",
        "re",
        "oi",
        "ïs",
        "üs",
        "ai",
        "as",
        "at",
        "is",
        "it",
        "ui",
        "us",
        "ut",
        "st",
        "s",
        "t",
        "e",
        "é",
        "z",
        "u",
        "a",
        "i",
    ]

    for ending in verb_endings:
        if word == ending:
            word = word
            break
        if word.endswith(ending):
            word = re.sub(r"{0}$".format(ending), "", word)
            break

    return word


def stem(word: str) -> str:
    """
    Stem a word of Old French.

    >>> stem('departissent')
    'depart'
    >>> stem('talent')
    'talent'

    """
    word = word.lower()

    """remove the simple endings from the target word"""
    stemmed_word, was_stemmed = _matchremove_noun_endings(word)

    """if word didn't match the simple endings, try verb endings"""
    if not was_stemmed:
        stemmed_word = _matchremove_verb_endings(word)

    return stemmed_word
