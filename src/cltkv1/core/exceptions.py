"""Custom exceptions for ``cltk`` library."""


class CLTKException(Exception):
    """Exception class for the ``cltkv1`` library.

    >>> from cltkv1.core.exceptions import CLTKException
    >>> raise CLTKException
    Traceback (most recent call last):
      ...
      File "<doctest cltkv1.core.exceptions.CLTKException[1]>", line 1, in <module>
        raise CLTKException
    cltkv1.core.exceptions.CLTKException
    """


class UnimplementedAlgorithmError(CLTKException):
    """Exception for when a language is supported by the CLTK however
    a particular algorithm is not available for that language.

    >>> from cltkv1.core.exceptions import UnimplementedAlgorithmError
    >>> raise UnimplementedAlgorithmError
    Traceback (most recent call last):
      ...
      File "<doctest cltkv1.core.exceptions.UnimplementedAlgorithmError[1]>", line 1, in <module>
        raise UnimplementedAlgorithmError
    cltkv1.core.exceptions.UnimplementedAlgorithmError
    """


class UnknownLanguageError(CLTKException):
    """Exception for when a user requests a language either not
    known to the CLTK or not yet implemented.

    All known languages at ``cltkv1.languages.glottolog.py``. Implemented
    languages include those at ``cltkv1.languages.pipelines`` and some
    miscellaneously implemented throughout the library.

    >>> from cltkv1.core.exceptions import UnknownLanguageError
    >>> raise UnknownLanguageError
    Traceback (most recent call last):
      ...
      File "<doctest cltkv1.core.exceptions.UnknownLanguageError[1]>", line 1, in <module>
        raise UnknownLanguageError
    cltkv1.core.exceptions.UnknownLanguageError
    """


class CorpusImportError(Exception):
    """CLTK exception to use when something goes wrong importing corpora"""

    pass
