"""Functions for retrieving data from text corpora."""

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

    # Save this for highlight-matching
    #snippet = snippet_left + '*' + match.string[match.start():match.end()] + '*' + snippet_right
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


if __name__ == '__main__':
    TEXT = """Ita fac, mi Lucili; vindica te tibi, et tempus, quod adhuc aut auferebatur aut subripiebatur aut excidebat, collige et serva. Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt. Turpissima tamen est iactura, quae per neglegentiam fit. Et si volueris attendere, maxima pars vitae elabitur male agentibus, magna nihil agentibus, tota vita aliud agentibus."""
    _matches = _regex_span(r'scribo', TEXT)
    for _match in _matches:
        s = _sentence_context(_match)
    print(s == 'Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt.')
