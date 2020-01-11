"""Module for accessing pre-trained `fastText word embeddings
<https://fasttext.cc/>`_. Two sets of models are available
from fastText, one being trained only on corpora taken from
Wikipedia (249 languages, `here
<https://fasttext.cc/docs/en/pretrained-vectors.html>`_) and
the other being a combination of Wikipedia and Common Crawl
(157 languages, a subset of the former, `here
<https://fasttext.cc/docs/en/crawl-vectors.html>`_).
"""

from cltkv1.core.exceptions import CLTKException
from cltkv1.languages.utils import get_lang

MAP_LANGS_CLTK_FASTTEXT = {
    "arb": "ar",  # Arabic
    "arc": "arc",  # Aramaic
    "got": "got",  # Gothic
    "lat": "la",  # Latin
    "pli": "pi",  # Pali
    "san": "sa",  # Sanskrit
    "xno": "ang",  # Anglo-Saxon
}


def is_fasttext_lang_available(iso_code: str) -> bool:
    """Returns whether any vectors are available, for
    fastText, for the input language. This is not comprehensive
    of all fastText embeddings, only those added into the CLTK.

    >>> is_fasttext_lang_available(iso_code="lat")
    True
    >>> is_fasttext_lang_available(iso_code="ave")
    False
    >>> is_fasttext_lang_available(iso_code="xxx")
    Traceback (most recent call last):
      ..
    cltkv1.core.exceptions.UnknownLanguageError
    """
    get_lang(iso_code=iso_code)
    if iso_code not in MAP_LANGS_CLTK_FASTTEXT:
        return False
    else:
        return True


def get_fasttext_lang_code(iso_code: str) -> str:
    """Input an ISO language code (used by the CLTK) and
    return the language code used by fastText.

    >>> from cltkv1.embeddings.fasttext import get_fasttext_lang_code
    >>> get_fasttext_lang_code(iso_code="xno")
    'ang'
    >>> get_fasttext_lang_code(iso_code="ave")
    Traceback (most recent call last):
      ...
    cltkv1.core.exceptions.CLTKException: fastText does not have embeddings for language 'ave'.
    >>> get_fasttext_lang_code(iso_code="xxx")
    Traceback (most recent call last):
      ...
    cltkv1.core.exceptions.UnknownLanguageError
    """
    is_available = is_fasttext_lang_available(iso_code=iso_code)
    if not is_available:
        raise CLTKException(
            f"fastText does not have embeddings for language '{iso_code}'."
        )
    return MAP_LANGS_CLTK_FASTTEXT[iso_code]


def is_vector_for_lang(iso_code: str, vector_type: str) -> bool:
    """Check whether a embedding is available for a chosen
    vector type, ``wiki`` or ``wiki_common_crawl``.

    >>> is_vector_for_lang(iso_code="lat", vector_type="wiki")
    True
    >>> is_vector_for_lang(iso_code="got", vector_type="wiki_common_crawl")
    False
    >>> is_vector_for_lang(iso_code="xxx", vector_type="wiki_common_crawl")
    Traceback (most recent call last):
      ...
    cltkv1.core.exceptions.UnknownLanguageError
    >>> is_vector_for_lang(iso_code="lat", vector_type="xxx")
    Traceback (most recent call last):
      ...
    cltkv1.core.exceptions.CLTKException: Invalid ``vector_type`` 'xxx'. Available: 'wiki', 'wiki_common_crawl'.
    """
    get_fasttext_lang_code(iso_code=iso_code)  # does validation for language
    vector_types = ["wiki", "wiki_common_crawl"]
    if vector_type not in vector_types:
        vector_types_str = "', '".join(vector_types)
        raise CLTKException(
            f"Invalid ``vector_type`` '{vector_type}'. Available: '{vector_types_str}'."
        )
    available_vectors = list()
    if vector_type == "wiki":
        available_vectors = ["arb", "arc", "got", "lat", "pli", "san", "xno"]
    elif vector_type == "wiki_common_crawl":
        available_vectors = ["arb", "lat", "san"]
    if iso_code in available_vectors:
        return True
    else:
        return False
