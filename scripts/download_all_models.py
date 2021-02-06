"""Script for provisioning build server.

TODO: add command line params for what langs (all or just one); useful for build server

To get all: ``$ python scripts/download_all_models.py``
For selected languages only: ``$ python scripts/download_all_models.py --languages=grc,lat``
"""

import argparse
import os
from typing import Any, Dict, List

import stanza

from cltk.core.exceptions import CLTKException
from cltk.data.fetch import LANGUAGE_CORPORA as AVAILABLE_CLTK_LANGS
from cltk.data.fetch import FetchCorpus
from cltk.dependency.stanza import (
    map_langs_cltk_stanza as AVAIL_STANZA_LANGS,
)  # type: Dict[str, str]
from cltk.embeddings.embeddings import MAP_LANGS_CLTK_FASTTEXT as AVAIL_FASSTEXT_LANGS
from cltk.embeddings.embeddings import MAP_NLPL_LANG_TO_URL as AVAIL_NLPL_LANGS
from cltk.embeddings.embeddings import FastTextEmbeddings, Word2VecEmbeddings
from cltk.nlp import iso_to_pipeline

PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    "--languages", help="What languages to download. Comma separated, no spaces."
)
ARGS = PARSER.parse_args()
SELECTED_LANGS = list()  # type: List[str]
AVAILABLE_LANGS = list(iso_to_pipeline.keys())  # type: List[str]
if not ARGS.languages:
    SELECTED_LANGS = AVAILABLE_LANGS
else:
    SELECTED_LANGS_SPLIT = ARGS.languages.split(",")
    for LANG in SELECTED_LANGS_SPLIT:
        if LANG not in AVAILABLE_LANGS:
            raise CLTKException(
                f"Unavailable language '{LANG}' chosen. Choose from: {', '.join(AVAILABLE_LANGS)}"
            )


def download_stanza_model(iso_code: str) -> None:
    """Download language models, from the ``stanza`` project,
    that are supported by the CLTK or in scope. More here:
    `<https://stanfordnlp.github.io/stanza/models.html>_.

    TODO: Use CLTK stanza wrapper class to dlk files
    TODO: Re-enable `package` parameter
    """
    all_ud_models_for_cltk = dict(
        cop=["scriptorium"],
        cu=["proiel"],  # OCS
        fro=["srcmf"],  # Old French
        grc=["perseus", "proiel"],
        got=["proiel"],
        la=["ittb", "proiel", "perseus"],
        lzh=["kyoto"],
    )  # type: Dict[str, List[str]]
    if iso_code not in all_ud_models_for_cltk:
        raise CLTKException(f"Language '{iso_code}' not available for Stanza.")
    stanza_dir = os.path.expanduser("~/stanza_resources/")  # type: str
    # for lang_name, model_sources in all_ud_models_for_cltk.items():
    #     for model_source in model_sources:
    if iso_code == "cop":
        # Coptic errors our, for some reason, if we pass the package name ``scriptorium``
        stanza.download(lang=iso_code, dir=stanza_dir)
    else:
        stanza.download(
            lang=iso_code,
            dir=stanza_dir,
            # package=all_ud_models_for_cltk[iso_code]
        )


def download_fasttext_model(
    iso_code: str, model_source: str = "wiki", interactive=False
) -> None:
    """Download fasttext model.

    TODO: Add way to actually get Common Crawl model.
    """
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


def download_cltk_models_repo(iso_code: str) -> None:
    """Download CLTK repos."""
    corpus_downloader = FetchCorpus(language=iso_code)
    corpus_downloader.import_corpus(corpus_name=f"{iso_code}_models_cltk")


def download_nlpl_model(iso_code: str) -> None:
    """Download word2vec model."""
    Word2VecEmbeddings(
        iso_code=iso_code, interactive=False, overwrite=False, silent=True
    )


if __name__ == "__main__":
    print("*** Downloading a basic set of models ... this will take a while.*** \n")
    for LANG in SELECTED_LANGS_SPLIT:
        print(f"Going to download all '{LANG}' models ...", LANG)
        # 1. Check if CLTK model available
        if LANG in AVAILABLE_CLTK_LANGS:
            download_cltk_models_repo(iso_code="lat")
        # 2. Check for Stanza
        if LANG in AVAIL_STANZA_LANGS:
            download_stanza_model(iso_code=LANG)
        # 3. Check fasttext
        if LANG in AVAIL_FASSTEXT_LANGS:
            download_fasttext_model(iso_code=LANG, interactive=False)
        # 4. Check nlpl
        if LANG in AVAIL_NLPL_LANGS:
            download_nlpl_model(iso_code=LANG)
    print("\n *** All done.  Welcome to the CLTK! ***")
