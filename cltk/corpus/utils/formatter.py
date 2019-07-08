"""Process downloaded or local corpora from one format into another.
Some formatting can happen here, or invoke language-specific formatters in
other files.
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>', 'Stephen Margheim <stephen.margheim@gmail.com>',
              'Natasha Voake <natashavoake@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

from builtins import bytes
from cltk.corpus.greek.tlg_index import TLG_INDEX
from cltk.corpus.greek.tlg_index import TLG_WORKS_INDEX
from cltk.corpus.latin.phi5_index import PHI5_INDEX
from cltk.corpus.latin.phi5_index import PHI5_WORKS_INDEX
from cltk.utils.cltk_logger import logger
from unicodedata import normalize
from cltk.tokenize.word import WordTokenizer
import re
import os
import regex


# research how to build regex values for regex.compile() from this dict
TLG_PHI_REPLACEMENTS = {
    'newline_hyphen': '-\n',
    'newline': '\n',  # you probably want to substitute this with an empty space ' '
    'within_pointed_brackets': '{.+?}',
    'chevrons': '«|»',
    'ellipsis': ' ... ',
    'latin_09': '[a-zA-Z0-9]',
    'within_parentheses': '\(.+?\)',
    'pointed_brackets': '\<|\>',
    'curled_single_quotes': '‘|’',
    'underscore': '_',
}


TONOS_OXIA = {
    "ά": "ά",
    "έ": "έ",
    "ή": "ή",
    "ί": "ί",
    "ό": "ό",
    "ύ": "ύ",
    "ώ": "ώ",
}


def tonos_oxia_converter(text, reverse=False):
    """For the Ancient Greek language. Converts characters accented with the
      tonos (meant for Modern Greek) into the oxia equivalent. Without this
      normalization, string comparisons will fail."""
    for char_tonos, char_oxia in TONOS_OXIA.items():
        if not reverse:        
            text = text.replace(char_tonos, char_oxia)
        else:
            text = text.replace(char_oxia, char_tonos)
    return text


def remove_non_ascii(input_string):
    """Remove non-ascii characters
    Source: http://stackoverflow.com/a/1342373
    """
    no_ascii = "".join(i for i in input_string if ord(i) < 128)
    return no_ascii


def remove_non_latin(input_string, also_keep=None):
    """Remove non-Latin characters.
    `also_keep` should be a list which will add chars (e.g. punctuation)
    that will not be filtered.
    """
    if also_keep:
        also_keep += [' ']
    else:
        also_keep = [' ']
    latin_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    latin_chars += latin_chars.lower()
    latin_chars += ''.join(also_keep)
    no_latin = "".join([char for char in input_string if char in latin_chars])
    return no_latin


def tlg_plaintext_cleanup(text, rm_punctuation=False, rm_periods=False):
    """Remove and substitute post-processing for Greek TLG text.
    TODO: Surely more junk to pull out. Please submit bugs!
    TODO: {.+?}|\(.+?\) working?
    TODO: This is a rather slow now, help in speeding up welcome.
    """
    remove_comp = regex.compile(r'-\n|«|»|<|>|\.\.\.|‘|’|_|{.+?}|\(.+?\)|[a-zA-Z0-9]', flags=regex.VERSION1)
    text = remove_comp.sub('', text)

    new_text = None
    if rm_punctuation:
        new_text = ''
        punctuation = [',', '·', ':', '"', "'", '?', '-', '!', '*', '[', ']', '{', '}']
        if rm_periods:
            punctuation += ['.', ';']
        for char in text:
            # second try at rming some punctuation; merge with above regex
            if char in punctuation:
                pass
            else:
                new_text += char
    if new_text:
        text = new_text

    # replace line breaks w/ space
    replace_comp = regex.compile(r'\n')
    text = replace_comp.sub(' ', text)

    comp_space = regex.compile(r'\s+')
    text = comp_space.sub(' ', text)

    return text


def cltk_normalize(text, compatibility=True):
    if compatibility:
        return normalize('NFKC', text)
    else:
        return normalize('NFC', text)


def phi5_plaintext_cleanup(text, rm_punctuation=False, rm_periods=False):
    """Remove and substitute post-processing for Greek PHI5 text.
    TODO: Surely more junk to pull out. Please submit bugs!
    TODO: This is a rather slow now, help in speeding up welcome.
    """
    # This works OK, doesn't get some
    # Note: rming all characters between {} and ()
    remove_comp = regex.compile(r'-\n|«|»|\<|\>|\.\.\.|‘|’|_|{.+?}|\(.+?\)|\(|\)|“|#|%|⚔|&|=|/|\\|〚|†|『|⚖|–|˘|⚕|☾|◌|◄|►|⌐|⌊|⌋|≈|∷|≈|∞|”|[0-9]')
    text = remove_comp.sub('', text)

    new_text = None
    if rm_punctuation:
        new_text = ''
        punctuation = [',', ';', ':', '"', "'", '?', '-', '!', '*', '[', ']', '{', '}']
        if rm_periods:
            punctuation += ['.']
        for char in text:
            # rm acute combining acute accents made by TLGU
            # Could be caught by regex, tried and failed, not sure why
            if bytes(char, 'utf-8') == b'\xcc\x81':
                pass
            # second try at rming some punctuation; merge with above regex
            elif char in punctuation:
                pass
            else:
                new_text += char
    if new_text:
        text = new_text

    # replace line breaks w/ space
    replace_comp = regex.compile(r'\n')
    text = replace_comp.sub(' ', text)

    comp_space = regex.compile(r'\s+')
    text = comp_space.sub(' ', text)

    return text


def assemble_tlg_author_filepaths():
    """Reads TLG index and builds a list of absolute filepaths."""
    plaintext_dir_rel = get_cltk_data_dir() + '/greek/text/tlg/plaintext/'
    plaintext_dir = os.path.expanduser(plaintext_dir_rel)
    filepaths = [os.path.join(plaintext_dir, x + '.TXT') for x in TLG_INDEX]
    return filepaths


def assemble_phi5_author_filepaths():
    """Reads PHI5 index and builds a list of absolute filepaths.
    """
    plaintext_dir_rel = get_cltk_data_dir() + '/latin/text/phi5/plaintext/'
    plaintext_dir = os.path.expanduser(plaintext_dir_rel)
    filepaths = [os.path.join(plaintext_dir, x + '.TXT') for x in PHI5_INDEX]
    return filepaths


def assemble_tlg_works_filepaths():
    """Reads TLG index and builds a list of absolute filepaths."""
    plaintext_dir_rel = get_cltk_data_dir() + '/greek/text/tlg/individual_works/'
    plaintext_dir = os.path.expanduser(plaintext_dir_rel)
    all_filepaths = []
    for author_code in TLG_WORKS_INDEX:
        author_data = TLG_WORKS_INDEX[author_code]
        works = author_data['works']
        for work in works:
            f = os.path.join(plaintext_dir, author_code + '.TXT' + '-' + work + '.txt')
            all_filepaths.append(f)
    return all_filepaths


def assemble_phi5_works_filepaths():
    """Reads PHI5 index and builds a list of absolute filepaths."""
    plaintext_dir_rel = get_cltk_data_dir() + '/latin/text/phi5/individual_works/'
    plaintext_dir = os.path.expanduser(plaintext_dir_rel)
    all_filepaths = []
    for author_code in PHI5_WORKS_INDEX:
        author_data = PHI5_WORKS_INDEX[author_code]
        works = author_data['works']
        for work in works:
            f = os.path.join(plaintext_dir, author_code + '.TXT' + '-' + work + '.txt')
            all_filepaths.append(f)
    return all_filepaths

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

patterns = [("eaus$", "eus"),
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
            ("d$", "")]

def build_match_and_apply_functions(pattern, replace):
    def matches_rule(word):
        return re.search(pattern, word)
    def apply_rule(word):
        return re.sub(pattern, replace, word)
    return (matches_rule, apply_rule)


rules = [build_match_and_apply_functions(pattern, replace)
         for (pattern, replace) in patterns]

def normalize_fr(string):
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

