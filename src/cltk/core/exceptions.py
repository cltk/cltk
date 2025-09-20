"""Custom exceptions for the CLTK library."""


class CLTKException(Exception):
    """Base exception class for CLTK.

    Examples:
        ```python
        from cltk.core.exceptions import CLTKException

        raise CLTKException()
        ```

    """


class UnimplementedAlgorithmError(CLTKException):
    """Raised when a language is supported but a specific algorithm is missing.

    Examples:
        ```python
        from cltk.core.exceptions import UnimplementedAlgorithmError

        raise UnimplementedAlgorithmError()
        ```

    """


class UnknownLanguageError(CLTKException):
    """Raised when a user requests a language unknown or not implemented.

    All known languages at ``cltk.languages.glottolog.py``. Implemented
    languages include those at ``cltk.languages.pipelines`` and some
    miscellaneously implemented throughout the library.

    Examples:
        ```python
        from cltk.core.exceptions import UnknownLanguageError

        raise UnknownLanguageError()
        ```

    """


class CorpusImportError(Exception):
    """Raised when something goes wrong importing corpora."""

    pass


class OpenAIInferenceError(CLTKException):
    """Raised when OpenAI inference fails or returns an invalid response."""

    pass
