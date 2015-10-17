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


def sentence_context(match, language='latin'):
    start = match.start()
    end = match.end()
    window = 15
    snippet_left = match.string[start - window:start]
    snippet_right = match.string[end:end + window]
    comp_sent_boundary = regex.compile(r'\.|\?|!')
    # Get the right-most final punct of the left snippet
    sentence_start = 0
    try:
        l = []
        for punct_match in comp_sent_boundary.finditer(snippet_left):
            sentence_start = punct_match.start()
            l.append(sentence_start)
        sentence_start = l.pop()
    except IndexError:
        sentence_start = 0
    # Get the left-most final punct of the right snippet
    sentence_end = 0
    try:
        l = []
        for punct_match in comp_sent_boundary.finditer(snippet_right):
            sentence_end = punct_match.end() - 1
            l.append(sentence_end)
        sentence_end = l.pop(0)
    except IndexError:
        sentence_end = -1
    print(snippet_left[sentence_start:-1], match.string[match.start():match.end()], snippet_right[0:sentence_end])
    #print(match.string[match.start():match.end()])
    #print(dir(match))
    print()

if __name__ == '__main__':
    TEXT = """Stubb was the second mate. He and . another p. was a native of Cape Cod; and hence, according to local usage, was called a Cape-Cod-man. A happy-go-lucky; neither craven nor valiant; taking perils as they came with an indifferent air; and while engaged in the most imminent crisis of the chase, toiling away, calm and collected as a journeyman joiner engaged for the year. Good-humored, easy, and careless, he presided over his whaleboat as if the most deadly encounter were but a dinner, and his crew all invited guests. He was as particular about the comfortable arrangements of his part of the boat, as an old stage-driver is about the snugness of his box. When close to the whale, in the very death-lock of the fight, he handled his unpitying lance coolly and off-handedly, as a whistling tinker his hammer. He would hum over his old rigadig tunes while flank and flank with the most exasperated monster. Long usage had, for this Stubb, converted the jaws of death into an easy chair. What he thought of death itself, there is no telling. Whether he ever thought of it at all, might be a question; but, if he ever did chance to cast his mind that way after a comfortable dinner, no doubt, like a good sailor, he took it to be a sort of call of the watch to tumble aloft, and bestir themselves there, about something which he would find out when he obeyed the order, and not sooner. What, perhaps, with other things, made Stubb such an easy-going, unfearing man, so cheerily trudging off with the burden of life in a world fail of grave peddlers, all bowed to the ground with their packs; what helped to bring about that almost impious good-humor of his; that thing must have been his pipe. For, like his nose, his short, black little pipe was one of the regular features of his face. You would almost as soon have expected him to turn out of his bunk without his nose as without his pipe. He kept a whole row of pipes there ready loaded, stuck in a rack, within easy reach of his hand; and, whenever he turned in, he smoked them all out in succession, lighting one from the other to the end of the chapter; then loading them again to be in readiness anew. For, when Stubb dressed, instead of first putting his legs into his trowsers, he put his pipe into his mouth."""
    _matches = _regex_span(r'and', TEXT)
    for _match in _matches:
        sentence_context(_match)
