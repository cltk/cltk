"""Custom exceptions for `cltk` library."""


class UnknownLanguageError(Exception):
    """Exception for when a user requests an NLP method that is not
    supported.

    TODO: Make a `CLTKException(Exception)` and have this inherit from that.
    """
