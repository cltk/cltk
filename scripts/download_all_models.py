"""Script for provisioning build server.

TODO: add command line params for what langs (all or just one); useful for build server

To get all: ``$ python scripts/download_all_models.py``
For selected languages only: ``$ python scripts/download_all_models.py --languages=grc,lat``
"""

import argparse

# import subprocess
import time

import spacy

from cltk.core.exceptions import CLTKException, CorpusImportError
from cltk.data.fetch import LANGUAGE_CORPORA as AVAILABLE_CLTK_LANGS
from cltk.data.fetch import FetchCorpus
from cltk.dependency.spacy_wrapper import MAP_LANGS_CLTK_SPACY as AVAIL_SPACY_LANGS
from cltk.dependency.spacy_wrapper import SpacyWrapper
from cltk.dependency.stanza_wrapper import (
    MAP_LANGS_CLTK_STANZA as AVAIL_STANZA_LANGS,  # pylint: disable=syntax-error
)
from cltk.dependency.stanza_wrapper import (
    StanzaWrapper,
)
from cltk.embeddings.embeddings import MAP_LANGS_CLTK_FASTTEXT as AVAIL_FASSTEXT_LANGS
from cltk.embeddings.embeddings import MAP_NLPL_LANG_TO_URL as AVAIL_NLPL_LANGS
from cltk.embeddings.embeddings import FastTextEmbeddings, Word2VecEmbeddings
from cltk.nlp import iso_to_pipeline

# from git import GitCommandError


T0 = time.time()

PARSER: argparse.ArgumentParser = argparse.ArgumentParser()
PARSER.add_argument(
    "--languages", help="What languages to download. Comma separated, no spaces."
)
ARGS: argparse.Namespace = PARSER.parse_args()
SELECTED_LANGS: list[str] = list()
ALL_AVAILABLE_LANGS: list[str] = list(iso_to_pipeline.keys())
if not ARGS.languages:
    SELECTED_LANGS = ALL_AVAILABLE_LANGS
else:
    SELECTED_LANGS_SPLIT = ARGS.languages.split(",")
    for LANG in SELECTED_LANGS_SPLIT:
        if LANG not in ALL_AVAILABLE_LANGS:
            raise CLTKException(
                f"Unavailable language '{LANG}' chosen. Choose from: {', '.join(ALL_AVAILABLE_LANGS)}"
            )
    SELECTED_LANGS = SELECTED_LANGS_SPLIT


def download_stanza_model(iso_code: str) -> None:
    """Download language models, from the ``stanza`` project,
    that are supported by the CLTK or in scope. More here:
    `<https://stanfordnlp.github.io/stanza/models.html>_.

    TODO: Re-enable `treebank` parameter
    """
    print(f"Going to download Stanza model for '{iso_code}'.")
    if iso_code not in AVAIL_STANZA_LANGS:
        raise CLTKException(f"Language '{iso_code}' not available for Stanza.")
    StanzaWrapper(language=iso_code, interactive=False, silent=False)
    print(f"Finished downloading Stanza for '{iso_code}'.")


def download_fasttext_model(
    iso_code: str, model_source: str = "wiki", interactive=False
) -> None:
    """Download fasttext model.

    TODO: Add way to specify a Common Crawl model.
    """
    print(f"Going to download fasttext model for '{iso_code}'.")
    avail_sources = ["wiki", "common_crawl"]
    assert (
        model_source in avail_sources
    ), f"Invalid `model_source`. Choose from: {', '.join(avail_sources)}."
    all_wiki_models = ["ang", "arb", "arc", "got", "lat", "pli", "san"]
    if model_source == "wiki" and iso_code not in all_wiki_models:
        raise CLTKException(
            f"Language '{iso_code}' not available for `model_source` '{model_source}'. Choose from: {', '.join(all_wiki_models)}."
        )
    all_common_crawl_models = ["arb", "lat", "san"]
    if model_source == "common_crawl" and iso_code not in all_common_crawl_models:
        raise CLTKException(
            f"Language '{iso_code}' not available for `model_source` '{model_source}'. Choose from: {', '.join(all_common_crawl_models)}."
        )
    FastTextEmbeddings(
        iso_code=iso_code, interactive=interactive, overwrite=False, silent=False
    )
    print(f"Finished downloading fasttext for '{iso_code}'.")


def download_cltk_models_repo(iso_code: str, default_branch: str = "master") -> None:
    """Download CLTK repos."""
    print(f"Going to download CLTK models for '{iso_code}'.")
    corpus_downloader = FetchCorpus(language=iso_code)
    try:
        corpus_downloader.import_corpus(
            corpus_name=f"{iso_code}_models_cltk", branch=default_branch
        )
    except CorpusImportError as e:
        print(e)
    if iso_code == "lat":
        corpus_downloader.import_corpus(corpus_name="cltk_lat_lewis_elementary_lexicon")
    elif iso_code == "non":
        corpus_downloader.import_corpus(corpus_name="cltk_non_zoega_dictionary")
    print(f"Finished downloading CLTK models for '{iso_code}'.")


def download_nlpl_model(iso_code: str) -> None:
    """Download word2vec model."""
    print(f"Going to download NLPL model for '{iso_code}'.")
    Word2VecEmbeddings(
        iso_code=iso_code, interactive=False, overwrite=False, silent=True
    )
    print(f"Finished downloading NLPL model for '{iso_code}'.")


def download_spacy_models(iso_code: str) -> None:
    """Download language models, from the ``spaCy`` project,
    that are supported by the CLTK or in scope.
    """
    print(f"Going to download spaCy model for '{iso_code}'.")
    if iso_code not in AVAIL_SPACY_LANGS:
        raise CLTKException(f"Language '{iso_code}' not available for spaCy.")
    if not spacy.util.is_package("la_core_web_lg"):
        print("Spacy Latin model not found. Going to download it ...")
        spacy_wrapper: SpacyWrapper = SpacyWrapper(
            language="lat", interactive=False, silent=False
        )
        # subprocess.check_call(
        #     [
        #         "pip",
        #         "install",
        #         "https://huggingface.co/latincy/la_core_web_lg/resolve/main/la_core_web_lg-any-py3-none-any.whl",
        #     ]
        # )
        print("Spacy downloaded?", spacy_wrapper._is_model_present())
    print(f"Finished downloading spaCy for '{iso_code}'.")


if __name__ == "__main__":
    print(f"Module loaded. Total elapsed time: {time.time() - T0}")
    print("*** Downloading a basic set of models ... this will take a while.*** \n")
    for LANG in SELECTED_LANGS:
        print(f"Going to download all '{LANG}' models ...")
        # 1. Check if CLTK model available
        if LANG in AVAILABLE_CLTK_LANGS:
            download_cltk_models_repo(iso_code=LANG)
        # 2. Check for Stanza
        if LANG in AVAIL_STANZA_LANGS:
            download_stanza_model(iso_code=LANG)
        # 3. Check fasttext
        if LANG in AVAIL_FASSTEXT_LANGS:
            download_fasttext_model(iso_code=LANG, interactive=False)
        # 4. Check nlpl
        if LANG in AVAIL_NLPL_LANGS:
            download_nlpl_model(iso_code=LANG)
        # 5. Check spaCy
        # TODO: Re-enable if we use Spacy again
        # Download works locally but failed on build server (Nov 2024)
        # if LANG in AVAIL_SPACY_LANGS:
        #     download_spacy_models(iso_code=LANG)
        print(
            f"All models fetched for '{LANG}'. Total elapsed time: {time.time() - T0}"
        )
    print("*** All done.  Welcome to the CLTK! ***")
