"""Script for provisioning build server.

Use: `$ python cltk/utils/download_misc_dependencies.py`
"""

import os
from typing import Any, List

from stanfordnlp.utils.resources import download

from cltkv1.embeddings.fasttext import (
    are_fasttext_models_downloaded,
    download_fasttext_models,
)


def get_stanfordnlp_models(force_update: bool = True) -> None:
    """Download language models, from the ``stanfordnlp`` project,
    that are supported by the CLTK or in scope. More here:
    `<https://stanfordnlp.github.io/stanfordnlp/models.html>_.
    """
    ud_models_for_cltk = [
        "grc_perseus",
        "grc_proiel",
        "la_ittb",
        "la_perseus",
        "la_proiel",
        "cu_proiel",  # Old Church Slavonic
        "fro_srcmf",  # Old French
        "got_proiel",
    ]  # type: List[str]

    stanford_dir = os.path.expanduser("~/stanfordnlp_resources/")  # type: str
    if os.path.isdir(stanford_dir) and not force_update:
        return
    for model in ud_models_for_cltk:
        download(
            download_label=model,
            resource_dir=stanford_dir,
            confirm_if_exists=True,
            force=force_update,
        )


def get_fasttext_models(force: bool = True, lang: str = "all"):
    all_wiki_models = ["arb", "arc", "got", "lat", "pli", "san", "xno"]
    all_common_crawl_models = ["arb", "lat", "san"]
    wiki_models = list()
    common_crawl_models = list()
    if lang == "all":
        wiki_models = all_wiki_models
        common_crawl_models = all_common_crawl_models
    else:
        assert (
            lang in all_wiki_models or lang in all_common_crawl_models
        ), f"ISO code '{lang}' either not among valid either 'wiki' or 'common_crawl' models."
        wiki_models = wiki_models.append(lang)
        common_crawl_models = common_crawl_models.append(lang)
    for lang in wiki_models:
        download_fasttext_models(iso_code=lang, vector_type="common_crawl", force=force)
    for lang in common_crawl_models:
        download_fasttext_models(iso_code=lang, vector_type="common_crawl", force=force)


if __name__ == "__main__":
    # TODO: add command line params for what langs (all or just one); useful for build server
    get_stanfordnlp_models(force_update=False)
    get_fasttext_models(force=False, lang="lat")
