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


def fasttext_example():
    """
    https://fasttext.cc/docs/en/python-module.html
    """
    import fasttext

    la_bin = "/Users/kyle/Downloads/wiki.la/wiki.la.bin"
    la_vec = "/Users/kyle/Downloads/wiki.la/wiki.la.vec"
    model = fasttext.load_model(la_bin)
    # dir(model)
    """
    ['__class__',
     '__contains__',
     '__delattr__',
     '__dict__',
     '__dir__',
     '__doc__',
     '__eq__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__getitem__',
     '__gt__',
     '__hash__',
     '__init__',
     '__init_subclass__',
     '__le__',
     '__lt__',
     '__module__',
     '__ne__',
     '__new__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__subclasshook__',
     '__weakref__',
     '_labels',
     '_words',
     'f',
     'get_dimension',
     'get_input_matrix',
     'get_input_vector',
     'get_labels',
     'get_line',
     'get_output_matrix',
     'get_sentence_vector',
     'get_subword_id',
     'get_subwords',
     'get_word_id',
     'get_word_vector',
     'get_words',
     'is_quantized',
     'labels',
     'predict',
     'quantize',
     'save_model',
     'test',
     'test_label',
     'words']
    """
    # print(model.words)
    """['pyrenaeo',
        'scholae',
        'sententia',
        'bowell',
        'intra',
        'un',
        'don',
        'roman',
        'africa',
        'septentrionali']
    """

    # model.get_word_vector("africa")
    # array([ 8.37695077e-02,  3.22437644e-01, ... ])

    # model.get_sentence_vector()  # Given a string, get a single vector represenation
    # model.get_sentence_vector("Germania omnis a Gallis Raetisque et Pannoni is Rheno et Danuvio fluminibus, a Sarmatis Dacisque mutuo metu aut montibus separatur")
    # array([ 1.47141377e-02, -2.64546536e-02,  1.44908112e-02, ... ])

    # model.labels[900:905]
    # ['pyrenaeo', 'scholae', 'sententia', 'bowell', 'intra']

    # model.get_dimension()
    # 300

    # model.get_word_id("africa")
    # 908

    # dir(model.predict)
    # Given a string, get a list of labels and a list of
    #     corresponding probabilities. k controls the number
    #     of returned labels. A choice of 5, will return the 5
    #     most probable labels. By default this returns only
    #     the most likely label and probability. threshold filters
    #     the returned labels by a threshold on probability. A
    #     choice of 0.5 will return labels with at least 0.5
    #     probability. k and threshold will be applied together to
    #     determine the returned labels.

    # model.predict(text="Nec Agricola licenter, more iuvenum qui militiam in lasciviam vertunt, neque segniter ad voluptates et commeatus titulum tribunatus et inscitiam rettulit")
    # ValueError: Model needs to be supervised for prediction!

    # model.get_subwords("africa")
    """
    (['africa',
      '<af',
      '<afr',
      '<afri',
      '<afric',
      'afr',
      'afri',
      'afric',
      'africa',
      'fri',
      'fric',
      'frica',
      'frica>',
      'ric',
      'rica',
      'rica>',
      'ica',
      'ica>',
      'ca>'],
     array([    908, 1238006,  482492, 1473779, 1365024,  252994,  192341,
             516954, 1038213, 1839910, 1097615, 1325774,  181928, 1319379,
             559322, 1786308,  595754,  471252, 1529907]))
    """

    # model.get_subword_id("ric")
    # 1319379

    return
