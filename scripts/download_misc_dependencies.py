"""Script for provisioning build server.

Use: `$ python cltk/utils/download_misc_dependencies.py`
"""

import os
from typing import Any, List

from stanfordnlp.utils.resources import download

from cltkv1.embeddings.embeddings import FastTextEmbeddings


def get_stanfordnlp_models(force_update: bool = True, lang: str = "all") -> None:
    """Download language models, from the ``stanfordnlp`` project,
    that are supported by the CLTK or in scope. More here:
    `<https://stanfordnlp.github.io/stanfordnlp/models.html>_.
    """
    all_ud_models_for_cltk = [
        "grc_perseus",
        "grc_proiel",
        "la_ittb",
        "la_perseus",
        "la_proiel",
        "cu_proiel",  # Old Church Slavonic
        "fro_srcmf",  # Old French
        "got_proiel",
    ]  # type: List[str]
    ud_models_for_dl = list()
    if lang == "all":
        ud_models_for_dl = all_ud_models_for_cltk
    elif lang == "chu":
        ud_models_for_dl = ud_models_for_dl + ["cu_proiel"]
    elif lang == "fro":
        ud_models_for_dl = ud_models_for_dl + ["fro_srcmf"]
    elif lang == "got_proiel":
        ud_models_for_dl = ud_models_for_dl + ["got_proiel"]
    elif lang == "grc":
        ud_models_for_dl = ud_models_for_dl + ["grc_perseus", "grc_proiel"]
    elif lang == "lat":
        ud_models_for_dl = ud_models_for_dl + ["la_ittb", "la_perseus", "la_proiel"]
    else:
        raise ValueError(f"No models for lang  '{lang}'.")
    # TODO: rm this check
    stanford_dir = os.path.expanduser("~/stanfordnlp_resources/")  # type: str
    for model in ud_models_for_dl:
        download(
            download_label=model,
            resource_dir=stanford_dir,
            confirm_if_exists=True,
            force=force_update,
        )


def get_fasttext_models(interactive=True):
    all_wiki_models = ["ang", "arb", "arc", "got", "lat", "pli", "san"]
    # all_common_crawl_models = ["arb", "lat", "san"]
    for lang in all_wiki_models:
        FastTextEmbeddings(
            iso_code=lang, interactive=interactive, overwrite=False, silent=True
        )


if __name__ == "__main__":
    # TODO: add command line params for what langs (all or just one); useful for build server
    get_stanfordnlp_models(force_update=True, lang="all")
    get_fasttext_models(interactive=False)
