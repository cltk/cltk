"""The normalizer aims to maximally reduce the variation between the orthography of texts written in the Anglo-Norman dialect
to bring it in line with “orthographe commune”. It is heavily inspired by Pope (1956).
Spelling variation is not consistent enough to ensure the highest accuracy; the normalizer in its current format should
therefore be used as a last resort.
The normalizer, word tokenizer, stemmer, lemmatizer, and list of stopwords for OF/MF were developed as part of Google Summer of Code 2017.
A full write-up of this work can be found at : https://gist.github.com/nat1881/6f134617805e2efbe5d275770e26d350
**References :** Pope, M.K. 1956. From Latin to Modern French with Especial Consideration of Anglo-Norman. Manchester: MUP.
Anglo-French spelling variants normalized to "orthographe commune", from M. K. Pope (1956)

- word-final d - e.g. vertud vs vertu
- use of <u> over <ou>
- <eaus> for <eus>, <ceaus> for <ceus>
- triphtongs:
   - <iu> for <ieu>
   - <u> for <eu>
   - <ie> for <iee>
   - <ue> for <uee>
   - <ure> for <eure>
- "epenthetic vowels" - e.g. averai for avrai
- <eo> for <o>
- <iw>, <ew> for <ieux>
- final <a> for <e>
"""

import re
from typing import List

FRO_PATTERNS = [
    ("eaus$", "eus"),
    ("ceaus$", "ceus"),
    ("iu", "ieu"),
    ("((?<!^)|(?<!(e)))u(?!$)", "eu"),
    ("ie$", "iee"),
    ("ue$", "uee"),
    ("ure$", "eure"),
    ("eo$", "o"),
    ("iw$", "ieux"),
    ("ew$", "ieux"),
    ("a$", "e"),
    ("^en", "an"),
    ("d$", ""),
]


def build_match_and_apply_functions(pattern, replace):
    """Assemble regex patterns."""

    def matches_rule(word):
        return re.search(pattern, word)

    def apply_rule(word):
        return re.sub(pattern, replace, word)

    return matches_rule, apply_rule


def normalize_fr(tokens: List[str]) -> List[str]:
    """Normalize Old and Middle French tokens.

    TODO: Make work work again with a tokenizer.
    """
    # from cltk.tokenizers.word import WordTokenizer
    # string = string.lower()
    # word_tokenizer = WordTokenizer("fro")
    # tokens = word_tokenizer.tokenize(string)
    rules = [
        build_match_and_apply_functions(pattern, replace)
        for (pattern, replace) in FRO_PATTERNS
    ]
    normalized_text = []
    for token in tokens:
        for matches_rule, apply_rule in rules:
            if matches_rule(token):
                normalized = apply_rule(token)
                normalized_text.append(normalized)
    return normalized_text
