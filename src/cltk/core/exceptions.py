"""Custom exceptions for ``cltk`` library."""


class CLTKException(Exception):
    """Exception class for the ``cltk`` library.

    >>> from cltk.core.exceptions import CLTKException
    >>> raise CLTKException
    Traceback (most recent call last):
      ...
      File "<doctest cltk.core.exceptions.CLTKException[1]>", line 1, in <module>
        raise CLTKException
    cltk.core.exceptions.CLTKException
    """


class UnimplementedAlgorithmError(CLTKException):
    """Exception for when a language is supported by the CLTK however
    a particular algorithm is not available for that language.

    >>> from cltk.core.exceptions import UnimplementedAlgorithmError
    >>> raise UnimplementedAlgorithmError
    Traceback (most recent call last):
      ...
      File "<doctest cltk.core.exceptions.UnimplementedAlgorithmError[1]>", line 1, in <module>
        raise UnimplementedAlgorithmError
    cltk.core.exceptions.UnimplementedAlgorithmError
    """


class UnknownLanguageError(CLTKException):
    """Exception for when a user requests a language either not
    known to the CLTK or not yet implemented.

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
    """CLTK exception to use when something goes wrong importing corpora"""

    pass
