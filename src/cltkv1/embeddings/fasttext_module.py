"""Module for accessing pre-trained `fastText word embeddings
<https://fasttext.cc/>`_. Two sets of models are available
from fastText, one being trained only on corpora taken from
Wikipedia (249 languages, `here
<https://fasttext.cc/docs/en/pretrained-vectors.html>`_) and
the other being a combination of Wikipedia and Common Crawl
(157 languages, a subset of the former, `here
<https://fasttext.cc/docs/en/crawl-vectors.html>`_).

TODO: Consider whether to use Gensim for accessing fastText vectors instead.

TODO: Figure out how to test fastText mdoels that (maybe) fail on build server due to insufficient memory.
"""

import io
import os

import fasttext
import requests
from tqdm import tqdm

from cltkv1 import __cltk_data_dir__
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

    >>> from cltkv1.embeddings.fasttext_module import get_fasttext_lang_code
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


def is_vector_for_lang(iso_code: str, training_set: str) -> bool:
    """Check whether a embedding is available for a chosen
    vector type, ``wiki`` or ``common_crawl``.

    >>> is_vector_for_lang(iso_code="lat", training_set="wiki")
    True
    >>> is_vector_for_lang(iso_code="got", training_set="common_crawl")
    False
    >>> is_vector_for_lang(iso_code="xxx", training_set="common_crawl")
    Traceback (most recent call last):
      ...
    cltkv1.core.exceptions.UnknownLanguageError
    >>> is_vector_for_lang(iso_code="lat", training_set="xxx")
    Traceback (most recent call last):
      ...
    cltkv1.core.exceptions.CLTKException: Invalid ``training_set`` 'xxx'. Available: 'wiki', 'common_crawl'.
    """
    get_fasttext_lang_code(iso_code=iso_code)  # does validation for language
    training_sets = ["wiki", "common_crawl"]
    if training_set not in training_sets:
        training_sets_str = "', '".join(training_sets)
        raise CLTKException(
            f"Invalid ``training_set`` '{training_set}'. Available: '{training_sets_str}'."
        )
    available_vectors = list()
    if training_set == "wiki":
        available_vectors = ["arb", "arc", "got", "lat", "pli", "san", "xno"]
    elif training_set == "common_crawl":
        available_vectors = ["arb", "lat", "san"]
    if iso_code in available_vectors:
        return True
    else:
        return False


def _build_fasttext_filepath(iso_code: str, training_set: str, model_type: str):
    """Create filepath at which to save a downloaded
    fasttext model.

    TODO: Do better than check for just name. Try trimming up to user home dir.

    >>> bin_fp = _build_fasttext_filepath(iso_code="lat", training_set="wiki", model_type="bin")
    >>> vec_fp = _build_fasttext_filepath(iso_code="lat", training_set="wiki", model_type="vec")
    >>> os.path.split(bin_fp)[1]
    'wiki.la.bin'
    >>> os.path.split(vec_fp)[1]
    'wiki.la.vec'
    >>> bin_fp = _build_fasttext_filepath(iso_code="lat", training_set="common_crawl", model_type="bin")
    >>> vec_fp = _build_fasttext_filepath(iso_code="lat", training_set="common_crawl", model_type="vec")
    >>> os.path.split(bin_fp)[1]
    'cc.la.300.bin'
    >>> os.path.split(vec_fp)[1]
    'cc.la.300.vec'
    """
    fasttext_code = MAP_LANGS_CLTK_FASTTEXT[iso_code]
    valid_model_types = ["bin", "vec"]
    if model_type not in valid_model_types:
        valid_model_types_str = "', '"
        raise CLTKException(
            f"Invalid model type '{model_type}'. Choose: '{valid_model_types_str}'."
        )
    fp_model = None
    if training_set == "wiki":
        fp_model = os.path.join(
            __cltk_data_dir__,
            iso_code,
            "embeddings",
            "fasttext",
            f"wiki.{fasttext_code}.{model_type}",
        )
    elif training_set == "common_crawl":
        fp_model = os.path.join(
            __cltk_data_dir__,
            iso_code,
            "embeddings",
            "fasttext",
            f"cc.{fasttext_code}.300.{model_type}",
        )
    return fp_model


def are_fasttext_models_downloaded(iso_code: str, training_set: str):
    """Check ``.bin` and/or ``.vec`` is present on disk at:
    ``~/cltk_data/lat/embeddings/fasttext/wiki.la.bin`` and
    ``~/cltk_data/lat/embeddings/fasttext/wiki.la.vec``.

    >>> are_fasttext_models_downloaded(iso_code="lat", training_set="wiki")
    True
    >>> are_fasttext_models_downloaded(iso_code="lat", training_set="common_crawl")
    True
    """
    is_fasttext_lang_available(iso_code=iso_code)
    is_vector_for_lang(iso_code=iso_code, training_set=training_set)
    fp_model_bin = _build_fasttext_filepath(
        iso_code=iso_code, training_set=training_set, model_type="bin"
    )
    fp_model_vec = _build_fasttext_filepath(
        iso_code=iso_code, training_set=training_set, model_type="vec"
    )
    if os.path.isfile(fp_model_bin) and os.path.isfile(fp_model_vec):
        return True
    else:
        return False


def _build_fasttext_url(iso_code: str, training_set: str):
    """Make the URL at which the requested model may be
    downloaded.

    >>> bin_url, vec_url = _build_fasttext_url(iso_code="lat", training_set="wiki")
    >>> bin_url
    'https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.la.zip'
    >>> vec_url
    'https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.la.vec'
    >>> bin_url, vec_url = _build_fasttext_url(iso_code="lat", training_set="common_crawl")
    >>> bin_url
    'https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.la.300.bin.gz'
    >>> vec_url
    'https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.la.300.vec.gz'
    """
    fasttext_code = get_fasttext_lang_code(iso_code=iso_code)
    bin_url = None
    vec_url = None
    if training_set == "wiki":
        bin_url = f"https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.{fasttext_code}.zip"
        vec_url = f"https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.{fasttext_code}.vec"
    elif training_set == "common_crawl":
        bin_url = f"https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.{fasttext_code}.300.bin.gz"
        vec_url = f"https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.{fasttext_code}.300.vec.gz"
    return bin_url, vec_url


def _mk_dirs_for_file(filepath):
    """Make all dirs specified for final file.

    >>> _mk_dirs_for_file("~/new-dir/some-file.txt")
    """
    dirs = os.path.split(filepath)[0]
    try:
        os.makedirs(dirs)
    except FileExistsError:
        # TODO: Log INFO level
        pass


def _get_file_with_progress_bar(url: str, filepath: str):
    """Download file with a progress bar.

    Source: https://stackoverflow.com/a/37573701

    TODO: Look at "Download Large Files with Tqdm Progress Bar" here: https://medium.com/better-programming/python-progress-bars-with-tqdm-by-example-ce98dbbc9697
    TODO: Confirm everything saves right
    TODO: Add tests
    """
    _mk_dirs_for_file(filepath=filepath)
    req_obj = requests.get(url=url, stream=True)
    total_size = int(req_obj.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
    with open(filepath, "wb") as file_open:
        for data in req_obj.iter_content(block_size):
            progress_bar.update(len(data))
            file_open.write(data)
    progress_bar.close()
    if total_size != 0 and progress_bar.n != total_size:
        print("ERROR, something went wrong")


def download_fasttext_models(iso_code: str, training_set: str, force=False):
    """Perform complete download of fastText models and save
    them in appropriate ``cltk_data`` dir.

    TODO: Add tests
    """
    is_fasttext_lang_available(iso_code=iso_code)
    is_vector_for_lang(iso_code=iso_code, training_set=training_set)
    if (
        not are_fasttext_models_downloaded(iso_code=iso_code, training_set=training_set)
        or force
    ):
        bin_url, vec_url = _build_fasttext_url(
            iso_code=iso_code, training_set=training_set
        )
        bin_fp = _build_fasttext_filepath(
            iso_code=iso_code, training_set=training_set, model_type="bin"
        )
        vec_fp = _build_fasttext_filepath(
            iso_code=iso_code, training_set=training_set, model_type="vec"
        )
        _get_file_with_progress_bar(url=bin_url, filepath=bin_fp)
        _get_file_with_progress_bar(url=vec_url, filepath=vec_fp)
    else:
        return None


def load_fasttext_model(iso_code: str, training_set: str, model_type: str):
    """Load fastText a model into memory and gracefully handle
    failure. ``.bin`` models contain all information necessary
    to retrain (parameters and dictionary) while the ``.vec``
    is much smaller and only has the word vectors.

    TODO: Add exceptions for loading problems due to FT not being installed
    TODO: Check all 4 types of model reading on cpu w/ enough memory

    >>> ft_model = load_fasttext_model(iso_code="lat", training_set="wiki", model_type="bin") # doctest: +SKIP
    >>> type(ft_model) # doctest: +SKIP
    <class 'fasttext.FastText._FastText'>
    """
    is_fasttext_lang_available(iso_code=iso_code)
    is_vector_for_lang(iso_code=iso_code, training_set=training_set)
    fp_model = _build_fasttext_filepath(
        iso_code=iso_code, training_set=training_set, model_type=model_type
    )
    if not os.path.isfile(fp_model):
        # TODO: Give instructions how to install
        raise FileNotFoundError(
            f"``fastText`` model expected at ``{fp_model}`` and not found."
        )
    model = fasttext.load_model(fp_model)
    return model

    # wv = "/Users/kyle.p.johnson/cltk_data/lat/embeddings/fasttext/wiki.la.vec"
    # print(fp_model == wv)
    # if model_type == "vec":
    #     fin = io.open(fp_model, 'r', encoding='utf-8', newline='\n', errors='ignore')
    #     n, d = map(int, fin.readline().split())
    #     data = {}
    #     for line in fin:
    #         tokens = line.rstrip().split(' ')
    #         data[tokens[0]] = map(float, tokens[1:])
    #     return data
    # elif model_type == "bin":
    #     # TODO: read bin ft files
    #     raise NotImplementedError("Cannot load bin files yet")
    # else:
    #     raise ValueError(f"Invalid '{model_type}'.")


def get_fasttext_embedding(word: str, model: "fasttext.FastText._FastText"):
    """Get embedding for a word.

    >>> from cltkv1.embeddings.fasttext_module import load_fasttext_model
    >>> ft_model = load_fasttext_model(iso_code="lat", training_set="wiki", model_type="bin") # doctest: +SKIP
    >>> ft_embedding = get_fasttext_embedding(word="arma", model=ft_model) # doctest: +SKIP
    >>> type(ft_embedding) # doctest: +SKIP
    <class 'numpy.ndarray'>
    >>> type(ft_embedding[0]) # doctest: +SKIP
    <class 'numpy.float32'>
    """
    fasttext_vector = model.get_word_vector(word)
    return fasttext_vector


def get_fasttext_sentence_embedding(word: str, model: "fasttext.FastText._FastText"):
    """Get embedding for a word.

    >>> from cltkv1.embeddings.fasttext_module import load_fasttext_model
    >>> ft_model = load_fasttext_model(iso_code="lat", training_set="wiki", model_type="bin") # doctest: +SKIP
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> latin_text_str = get_example_text("lat")[:50]
    >>> ft_sent_embedding = get_fasttext_sentence_embedding(word=latin_text_str, model=ft_model) # doctest: +SKIP
    >>> type(ft_sent_embedding) # doctest: +SKIP
    <class 'numpy.ndarray'>
    >>> type(ft_sent_embedding[0]) # doctest: +SKIP
    <class 'numpy.float32'>
    """
    fasttext_vector = model.get_sentence_vector(word)
    return fasttext_vector


def fasttext_example():
    """
    https://fasttext.cc/docs/en/python-module.html
    """

    la_bin = _build_fasttext_filepath(
        iso_code="lat", training_set="wiki", model_type="bin"
    )
    print(os.path.isfile(la_bin), la_bin)
    la_vec = _build_fasttext_filepath(
        iso_code="lat", training_set="wiki", model_type="vec"
    )
    print(os.path.isfile(la_vec), la_vec)

    fasttext.load_model(la_vec)

    # la_vec = "/Users/kyle/Downloads/wiki.la/wiki.la.vec"
    # print(dir(fasttext))
    # model = fasttext.load_model(la_bin)
    # print(dir(model))
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


if __name__ == "__main__":
    # are_fasttext_models_downloaded(iso_code="lat", training_set="wiki")
    # _build_fasttext_filepath(iso_code="lat", training_set="common_crawl", model_type="vec")
    # download_fasttext_models(iso_code="lat", training_set="wiki")
    # download_fasttext_models(iso_code="lat", training_set="common_crawl")

    # x = load_ft_model(iso_code="lat", training_set="wiki", model_type="vec")
    # print(x)

    fasttext_example()
