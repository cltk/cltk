"""Functions for retrieving data from text corpora."""

from cltk.corpus.greek.tlg_index import TLG_INDEX
from cltk.corpus.latin.phi5_index import PHI5_INDEX
from cltk.corpus.utils.formatter import assemble_phi5_author_filepaths
from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths
import os
import regex

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
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


def search_corpus(pattern, corpus, context, case_insensitive=True):
    """Search for pattern in TLG or PHI5.
    TODO: Cleanup hyphenation.
    """

    corpora = ['tlg', 'phi5']
    assert corpus in corpora, "Available corpora: {''}.".format(corpora)

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

    for path in paths:
        with open(path) as file_open:
            text = file_open.read()
        _matches = match_regex(text, pattern, language=lang, context=160, case_insensitive=case_insensitive)
        for _match in _matches:
            _id = os.path.split(path)[1][:-4]
            author = index[_id]
            yield (author, _match)


if __name__ == '__main__':
    for x in search_corpus('ὦ ἄνδρες Ἀθηναῖοι', 'tlg', context='sentence'):
        print(x)
