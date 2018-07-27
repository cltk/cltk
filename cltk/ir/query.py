"""Functions for retrieving data from text corpora.

TODO: Add CLTK logging.
TODO: Make different functions for regex versus plaintext query.
TODO: Make public function for searching string.
TODO: Make public function for searching specific texts (passing list of eg, author names, ids, and/or filepaths.)
TODO: Add option of outputting to plaintext file.
TODO: For whatever output, generate statistics on # of matches found, # docs searched.
"""

import os
import string

from cltk.corpus.greek.tlg_index import TLG_INDEX
from cltk.corpus.latin.phi5_index import PHI5_INDEX
from cltk.corpus.utils.formatter import assemble_phi5_author_filepaths
from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths
import regex

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>']
__license__ = 'MIT License. See LICENSE.'


def _regex_span(_regex, _str, case_insensitive=True):
    """Return all matches in an input string.
    :rtype : regex.match.span
    :param _regex: A regular expression pattern.
    :param _str: Text on which to run the pattern.
    """
    if case_insensitive:
        flags = regex.IGNORECASE | regex.FULLCASE | regex.VERSION1
    else:
        flags = regex.VERSION1
    comp = regex.compile(_regex, flags=flags)
    matches = comp.finditer(_str)
    for match in matches:
        yield match


def _sentence_context(match, language='latin', case_insensitive=True):
    """Take one incoming regex match object and return the sentence in which
     the match occurs.

    :rtype : str
    :param match: regex.match
    :param language: str
    """

    language_punct = {'greek': r'\.|;',
                      'latin': r'\.|\?|!'}

    assert language in language_punct.keys(), \
        'Available punctuation schemes: {}'.format(language_punct.keys())

    start = match.start()
    end = match.end()
    window = 1000
    snippet_left = match.string[start - window:start + 1]
    snippet_right = match.string[end:end + window]
    re_match = match.string[match.start():match.end()]

    comp_sent_boundary = regex.compile(language_punct[language], flags=regex.VERSION1)
    # Left
    left_punct = []
    for punct in comp_sent_boundary.finditer(snippet_left):
        end = punct.end()
        left_punct.append(end)
    try:
        last_period = left_punct.pop() + 1
    except IndexError:
        last_period = 0

    # Right
    right_punct = []
    for punct in comp_sent_boundary.finditer(snippet_right):
        end = punct.end()
        right_punct.append(end)
    try:
        first_period = right_punct.pop(0)
    except IndexError:
        first_period = 0

    sentence = snippet_left[last_period:-1] + '*' + re_match + '*' + snippet_right[0:first_period]

    return sentence


def _paragraph_context(match):
    """Take one incoming regex match object and return the paragraph in which
    the match occurs.
    :rtype : str
    :param match: regex.match
    :param language: str
    """
    start = match.start()
    end = match.end()
    window = 100000
    snippet_left = match.string[start - window:start + 1]
    snippet_right = match.string[end:end + window]
    re_match = match.string[match.start():match.end()]

    # (1) Optional any whitespaces, (2) one newline, (3) optional any whitespaces.
    para_break_pattern = r'\s*?\n\s*?'
    comp_sent_boundary = regex.compile(para_break_pattern, flags=regex.VERSION1)
    # Left
    left_punct = []
    for punct in comp_sent_boundary.finditer(snippet_left):
        end = punct.end()
        left_punct.append(end)
    try:
        last_period = left_punct.pop()
    except IndexError:
        last_period = 0

    # Right
    right_punct = []
    for punct in comp_sent_boundary.finditer(snippet_right):
        end = punct.end()
        right_punct.append(end)
    try:
        first_period = right_punct.pop(0)
    except IndexError:
        first_period = 0

    sentence = snippet_left[last_period:-1] + '*' + re_match + '*' + snippet_right[0:first_period - 1]

    # Remove any trailing whitespace. Necessary?
    #comp_final_space = regex.compile(r'\s*$')
    #sentence = comp_final_space.sub('', sentence)

    return sentence


def _window_match(match, window=100):
    """Take incoming match and highlight in context.
    :rtype : str
    :param match: Regex match.
    :param window: Characters on each side of match to return.
    :type window: int
    """
    window = int(window)
    start = match.start()
    end = match.end()
    snippet_left = match.string[start - window:start]
    snippet_match = match.string[match.start():match.end()]
    snippet_right = match.string[end:end + window]

    snippet = snippet_left + '*' + snippet_match + '*' + snippet_right

    return snippet


def match_regex(input_str, pattern, language, context, case_insensitive=True):
    """Take input string and a regex pattern, then yield generator of matches
     in desired format.

     TODO: Rename this `match_pattern` and incorporate the keyword expansion
      code currently in search_corpus.

    :param input_str:
    :param pattern:
    :param language:
    :param context: Integer or 'sentence' 'paragraph'
    :rtype : str
    """
    if type(context) is str:
        contexts = ['sentence', 'paragraph']
        assert context in contexts or type(context) is int, 'Available contexts: {}'.format(contexts)
    else:
        context = int(context)
    for match in _regex_span(pattern, input_str, case_insensitive=case_insensitive):
        if context == 'sentence':
            yield _sentence_context(match, language)
        elif context == 'paragraph':
            yield _paragraph_context(match)
        else:
            yield _window_match(match, context)


def search_corpus(pattern, corpus, context, case_insensitive=True, expand_keyword=False, lemmatized=False, threshold=0.70):
    """Search for pattern in TLG or PHI5.
    TODO: Cleanup hyphenation.
    """

    corpora = ['tlg', 'phi5']
    assert corpus in corpora, "Available corpora: '{}'.".format(corpora)

    if type(context) is str:
        contexts = ['sentence', 'paragraph']
        assert context in contexts or type(context) is int, 'Available contexts: {}'.format(contexts)
    else:
        context = int(context)

    if corpus == 'phi5':
        lang = 'latin'
        index = PHI5_INDEX
        paths = assemble_phi5_author_filepaths()
    elif corpus == 'tlg':
        index = TLG_INDEX
        lang = 'greek'
        paths = assemble_tlg_author_filepaths()

    if expand_keyword:
        # Strip off all regex characters from pattern for Word2Vec lookup
        # First rm escaped chars
        # TODO: Add '\u', '\U', '\x' to this list
        escapes_list = [r'\a', r'\b', r'\f', r'\n', r'\r', r'\t', r'\v', r'\\']
        escapes_str = '|'.join(escapes_list)
        comp_escapes = regex.compile(escapes_str, flags=regex.VERSION1)
        pattern = comp_escapes.sub('', pattern)
        # Second rm remaining punctuation
        punctuation = set(string.punctuation)
        pattern = ''.join(ch for ch in pattern if ch not in punctuation)
        similar_vectors = _keyword_expander(pattern, lang, lemmatized=lemmatized, threshold=threshold)
        print("The following similar terms will be added to the '{0}' query: '{1}'.".format(pattern, similar_vectors))
        pattern = [pattern]
        if similar_vectors:
            pattern += similar_vectors
        else:
            pattern = pattern

    for path in paths:
        with open(path) as file_open:
            text = file_open.read()
        for one_pattern in pattern:
            _matches = match_regex(text, one_pattern, language=lang, context=context, case_insensitive=case_insensitive)
            for _match in _matches:
                _id = os.path.split(path)[1][:-4]
                author = index[_id]
                yield (author, _match)


def _keyword_expander(word, language, lemmatized=False, threshold=0.70):
    """Find similar terms in Word2Vec models. Accepts string and returns a
     list of terms of n similarity.
    :rtype : list
     """
    try:
        from cltk.vector.word2vec import get_sims
    except ImportError as imp_err:
        print(imp_err)
        raise
    similar_vectors = get_sims(word, language, lemmatized=lemmatized, threshold=threshold)

    return similar_vectors


if __name__ == '__main__':
    for x in search_corpus('\namicitia.*+?', 'phi5', context='sentence', case_insensitive=True, expand_keyword=True, lemmatized=False, threshold=0.7):
        print(x)
    #print(_keyword_expander('iubeo', 'latin', lemmatized=True, threshold=0.00))
