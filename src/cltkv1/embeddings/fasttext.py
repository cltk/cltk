"""Module for accessing pre-trained `fastText word embeddings
<https://fasttext.cc/>`_. Models available from fastText
languages are at `<https://fasttext.cc/docs/en/pretrained-vectors.html>`_.
Besides those here, other modern language embeddings may in some cases
work for historical forms.
"""

from cltkv1.languages.utils import get_lang


def get_fasttext_code(cltk_code):
    """Input a Glottolog language code (used by the CLTK) and
    return the language code used by fastText.

    >>> from cltkv1.embeddings.fasttext import get_fasttext_code
    >>> get_fasttext_code(cltk_code="xno")
    'ang'
    >>> get_fasttext_code(cltk_code="xxx")
    Traceback (most recent call last):
      ...
    cltkv1.core.exceptions.UnknownLanguageError
    """
    get_lang(cltk_code)
    # add check for valid cltk code
    map_langs_cltk_fasttext = {
        "xno": "ang",  # Anglo-Saxon
        "arc": "arc",  # Aramaic
        "arb": "ar",  # Arabic
        "lat": "la",  # Latin
        "got": "got",  # Gothic
        "pli": "pi",  # Pali
        "san": "sa",  # Sanskrit
    }
    return map_langs_cltk_fasttext[cltk_code]
