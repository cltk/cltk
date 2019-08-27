"""Functions for working with stopword lists."""


def get_available_stoplists():
    """Look up within the ``stopwords`` submodule for which languages the CLTK has a stopword list."""
    return []


def filter_stops(language, tokens, stops=None):
    """Take input list of tokens and remove tokens found in a given language's stopword list. Uses the CLTK's list unless a custom list is provided."""
    return []


def index_stops(language, tokens, stops=None):
    """Build a list of tokens, only each item is a ?set with attributes about each token. For this one, info added about ``stop=True|False``.

    TODO: Decide upon this (following universal NLP word token type?).
    """
    return []
