#encoding: utf-8
import re
from cltk.tokenize.word import WordTokenizer



"""Anglo-French spelling variants normalized to "orthographe commune", from M. K. Pope (1956)

- word-final d - e.g. vertud vs vertu
- use of <u> over <ou>

- persistence of <ei>

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
patterns = [("eaus$", "eus"),
            ("ceaus$", "ceus"),
            ("iu", "ieu"),
            ("(^^|^(eu))u(^$)", "eu"),
            ("ie$", "iee"),
            ("ue$", "uee"),
            ("ure$", "eure"),
            ("eo$", "o"),
            ("iw$", "ieux"),
            ("ew$", "ieux"),
            ("a$", "e"),
            ("^en", "an"),
            ("d$", "")]

def build_match_and_apply_functions(pattern, replace):
    def matches_rule(word):
        return re.search(pattern, word)
    def apply_rule(word):
        return re.sub(pattern, replace, word)
    return (matches_rule, apply_rule)


rules = [build_match_and_apply_functions(pattern, replace)
         for (pattern, replace) in patterns]

def normalize(string):
    string = string.lower()
    word_tokenizer = WordTokenizer('french')
    tokens = word_tokenizer.tokenize(string)
    normalized_text = []
    for token in tokens:
        for matches_rule, apply_rule in rules:
            if matches_rule(token):
                normalized = apply_rule(token)
                normalized_text.append(normalized)
    return normalized_text

