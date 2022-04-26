"""Named entity recognition (NER).

.. note::
   For Greek and Latin, v. ``0.1`` had a way of getting ``True``/``False``
   whether a word was an entity of any sort (i.e., a proper noun). The
   data used for this is available at ``os.path.join(CLTK_DATA_DIR, "grc/model/grc_models_cltk/ner/proper_names.txt")``
    and ``os.path.join(CLTK_DATA_DIR, "lat/model/lat_models_cltk/ner/proper_names.txt")``, respectively.

"""

import importlib.machinery
import logging
import os
from typing import List, Union

from cltk.core.exceptions import UnimplementedAlgorithmError
from cltk.languages.utils import get_lang
from cltk.ner.spacy_ner import download_prompt, spacy_tag_ner
from cltk.utils import CLTK_DATA_DIR

__author__ = ["Natasha Voake <natashavoake@gmail.com>"]

NER_DICT = {
    # "ang": os.path.join(CLTK_DATA_DIR, "ang/model/ang_models_cltk/ner/spacy_model/"),
    "fro": os.path.join(CLTK_DATA_DIR, "fro/model/fro_models_cltk/named_entities_fr.py"),
    # "grc": os.path.join(
    #     CLTK_DATA_DIR,
    #     "grc/model/grc_models_cltk/ner/spacy_model/",
    # ),
    # "lat": os.path.join(
    #     CLTK_DATA_DIR,
    #     "lat/model/lat_models_cltk/ner/spacy_model/",
    # ),
}


def tag_ner(iso_code: str, input_tokens: List[str]) -> List[Union[bool, str]]:
    """Run NER for chosen language. Some languages return boolean True/False,
    others give string of entity type (e.g., ``LOC``).

    >>> from cltk.ner.ner import tag_ner
    >>> from cltk.languages.example_texts import get_example_text
    >>> from boltons.strutils import split_punct_ws
    >>> tokens = split_punct_ws(get_example_text(iso_code="lat"))

    >>> text = "ἐπὶ δ᾽ οὖν τοῖς πρώτοις τοῖσδε Περικλῆς ὁ Ξανθίππου ᾑρέθη λέγειν. καὶ ἐπειδὴ καιρὸς ἐλάμβανε, προελθὼν ἀπὸ τοῦ σήματος ἐπὶ βῆμα ὑψηλὸν πεποιημένον, ὅπως ἀκούοιτο ὡς ἐπὶ πλεῖστον τοῦ ὁμίλου, ἔλεγε τοιάδε."
    >>> tokens = split_punct_ws(text)
    >>> are_words_entities = tag_ner(iso_code="grc", input_tokens=tokens)
    >>> tokens[:9]
    ['ἐπὶ', 'δ᾽', 'οὖν', 'τοῖς', 'πρώτοις', 'τοῖσδε', 'Περικλῆς', 'ὁ', 'Ξανθίππου']
    >>> are_words_entities[:9] # TODO find working ex!
    [False, False, False, False, False, False, False, False, False]

    >>> tokens = split_punct_ws(get_example_text(iso_code="fro"))
    >>> are_words_entities = tag_ner(iso_code="fro", input_tokens=tokens)
    >>> tokens[30:50]
    ['Bretaigne', 'A', 'I', 'molt', 'riche', 'chevalier', 'Hardi', 'et', 'coragous', 'et', 'fier', 'De', 'la', 'Table', 'Reonde', 'estoit', 'Le', 'roi', 'Artu', 'que']
    >>> are_words_entities[30:50]
    ['LOC', False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 'CHI']
    """

    get_lang(iso_code=iso_code)
    if iso_code not in NER_DICT:
        msg = f"NER unavailable for language ``{iso_code}``."
        raise UnimplementedAlgorithmError(msg)
    ner_file_path = os.path.expanduser(NER_DICT[iso_code])
    if iso_code == "fro":
        if not os.path.isfile(ner_file_path):
            msg = f"Old French model path '{ner_file_path}' not found. Going to try to download it ..."
            logging.warning(msg)
            dl_msg = f"This part of the CLTK depends upon models from the CLTK project."
            model_url = "https://github.com/cltk/fro_models_cltk"
            download_prompt(iso_code=iso_code, message=dl_msg, model_url=model_url)
        loader = importlib.machinery.SourceFileLoader("entities", ner_file_path)
        module = loader.load_module()  # type: module
        entities = module.entities  # type: Tuple(str, str)
        entities_type_list = list()
        for input_token in input_tokens:
            for entity_token, kind in entities:
                if input_token == entity_token:
                    entities_type_list.append(kind)
                    break
            entities_type_list.append(False)
        return entities_type_list
    elif iso_code in ["ang", "grc", "lat"]:
        return spacy_tag_ner(
            iso_code=iso_code, text_tokens=input_tokens, model_path=NER_DICT[iso_code]
        )  # List[str, None]
    else:
        with open(ner_file_path) as file_open:
            ner_str = file_open.read()
        ner_list = ner_str.split("\n")
        is_entity_list = list()  # type: List[bool]
        for word_token in input_tokens:
            if word_token in ner_list:
                is_entity_list.append(True)
            else:
                is_entity_list.append(False)
        return is_entity_list
