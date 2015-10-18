"""Functions for retrieving data from text corpora.

TODO: Write function for paragraph matching, do just like sentence matching.
TODO: Write public function(s) for different query types.
"""

import regex


def _regex_span(_regex, _str):
    """Return all matches in an input string.
    :rtype : regex.match.span
    :param _regex: A regular expression pattern.
    :param _str: Text on which to run the pattern.
    """
    comp = regex.compile(_regex, flags=regex.VERSION1)
    matches = comp.finditer(_str)
    for match in matches:
        yield match


def _sentence_context(match, language='latin'):
    """Take one incoming regex match object and return the sentence in which
     the match occurs.

     TODO: Rm trailing whitespace if any.

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

    comp_sent_boundary = regex.compile(language_punct[language])
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

    sentence = snippet_left[last_period:-1] + re_match + snippet_right[0:first_period]

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
    comp_sent_boundary = regex.compile(para_break_pattern)
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

    sentence = snippet_left[last_period:-1] + re_match + snippet_right[0:first_period - 1]

    # Remove any trailing whitespace. Necessary?
    #comp_final_space = regex.compile(r'\s*$')
    #sentence = comp_final_space.sub('', sentence)

    return sentence


def _highlight_match(match, window=100):
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


def match_regex(input_str, pattern, language, context):
    """Take input string and a regex pattern, then yield generator of matches
     in desired format.

    :param input_str:
    :param pattern:
    :param language:
    :param context: Integer or 'sentence' 'paragraph'
    :rtype : str

     TODO: Make case sensitive.
     """
    if type(context) is str:
        contexts = ['sentence', 'paragraph']
        assert context in contexts or type(context) is int, 'Available contexts: {}'.format(contexts)
    else:
        context = int(context)
    for match in _regex_span(pattern, input_str):
        if context == 'sentence':
            yield _sentence_context(match, language)
        elif context == 'paragraph':
            yield _paragraph_context(match)
        else:
            yield _highlight_match(match, context)


if __name__ == '__main__':
    TEXT = """Ita fac, mi Lucili; vindica te tibi.

et tempus, quod adhuc aut auferebatur aut subripiebatur aut excidebat, collige et serva.

Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt.

Turpissima tamen est iactura, quae per neglegentiam fit.

Et si volueris attendere, maxima pars vitae elabitur male agentibus, magna nihil agentibus, tota vita aliud agentibus.
"""
    _matches = match_regex(TEXT, r'scribo', language='latin', context='paragraph')
    for _match in _matches:
        print(_match)
