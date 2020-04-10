"""Script for provisioning build server.

Use: `$ python cltk/utils/download_misc_dependencies.py`
"""

import os
from typing import Any, Dict, List

# from stanza.utils.resources import download
import stanza

from cltkv1.data.fetch import FetchCorpus
from cltkv1.embeddings.embeddings import FastTextEmbeddings, Word2VecEmbeddings


def get_all_stanza_models() -> None:
    """Download language models, from the ``stanza`` project,
    that are supported by the CLTK or in scope. More here:
    `<https://stanfordnlp.github.io/stanza/models.html>_.
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
    stanford_dir = os.path.expanduser("~/stanza_resources/")  # type: str
    for lang_name, model_sources in all_ud_models_for_cltk.items():
        for model_source in model_sources:
            if lang_name == "cop":
                # Coptic errors our, for some reason, if we pass the package name ``scriptorium``
                stanza.download(lang=lang_name, dir=stanford_dir)
            else:
                stanza.download(lang=lang_name, dir=stanford_dir, package=model_source)


def get_fasttext_models(interactive=True) -> None:
    all_wiki_models = ["ang", "arb", "arc", "got", "lat", "pli", "san"]
    # all_common_crawl_models = ["arb", "lat", "san"]
    for lang in all_wiki_models:
        FastTextEmbeddings(
            iso_code=lang, interactive=interactive, overwrite=False, silent=True
        )


def download_cltk_models(iso_code: str) -> None:

    corpus_downloader = FetchCorpus(language=iso_code)
    # print(corpus_downloader.list_corpora)
    if iso_code == "fro":
        corpus_downloader.import_corpus(corpus_name=f"{iso_code}_data_cltk")
    else:
        corpus_downloader.import_corpus(corpus_name=f"{iso_code}_models_cltk")


def download_nlpl_model(iso_code: str) -> None:
    Word2VecEmbeddings(
        iso_code=iso_code, interactive=False, overwrite=False, silent=True
    )


if __name__ == "__main__":
    # TODO: add command line params for what langs (all or just one); useful for build server
    get_all_stanza_models()
    get_fasttext_models(interactive=False)

    download_nlpl_model(iso_code="grc")

    download_cltk_models(iso_code="lat")
    download_cltk_models(iso_code="grc")
    download_cltk_models(iso_code="fro")
    download_cltk_models(iso_code="san")
    download_cltk_models(iso_code="ang")
    download_cltk_models(iso_code="non")
    download_cltk_models(iso_code="gml")
    download_cltk_models(iso_code="gmh")
