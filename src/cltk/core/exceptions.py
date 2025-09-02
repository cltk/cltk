"""Custom exceptions for the CLTK library."""


class CLTKException(Exception):
    """Base exception class for CLTK.

    >>> from cltk.core.exceptions import CLTKException
    >>> raise CLTKException
    Traceback (most recent call last):
      ...
      File "<doctest cltk.core.exceptions.CLTKException[1]>", line 1, in <module>
        raise CLTKException
    cltk.core.exceptions.CLTKException
    """


class UnimplementedAlgorithmError(CLTKException):
    """Raised when a language is supported but a specific algorithm is missing.

    >>> from cltk.core.exceptions import UnimplementedAlgorithmError
    >>> raise UnimplementedAlgorithmError
    Traceback (most recent call last):
      ...
      File "<doctest cltk.core.exceptions.UnimplementedAlgorithmError[1]>", line 1, in <module>
        raise UnimplementedAlgorithmError
    cltk.core.exceptions.UnimplementedAlgorithmError
    """


class UnknownLanguageError(CLTKException):
    """Raised when a user requests a language unknown or not implemented.

    All known languages at ``cltk.languages.glottolog.py``. Implemented
    languages include those at ``cltk.languages.pipelines`` and some
    miscellaneously implemented throughout the library.

    >>> from cltk.core.exceptions import UnknownLanguageError
    >>> raise UnknownLanguageError
    Traceback (most recent call last):
      ...
      File "<doctest cltk.core.exceptions.UnknownLanguageError[1]>", line 1, in <module>
        raise UnknownLanguageError
    cltk.core.exceptions.UnknownLanguageError
    """


class CorpusImportError(Exception):
    """Raised when something goes wrong importing corpora."""

    pass


class OpenAIInferenceError(CLTKException):
    """Raised when OpenAI inference fails or returns an invalid response."""

    pass
