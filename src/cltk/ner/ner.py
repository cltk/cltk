"""Named entity recognition (NER)."""

import importlib.machinery
import os
from typing import List, Union

from cltk.core.exceptions import UnimplementedAlgorithmError
from cltk.languages.utils import get_lang
from cltk.utils import CLTK_DATA_DIR

__author__ = ["Natasha Voake <natashavoake@gmail.com>"]

NER_DICT = {
    "fro": os.path.join(CLTK_DATA_DIR, "fro/text/fro_data_cltk/named_entities_fr.py"),
    "grc": os.path.join(
        CLTK_DATA_DIR, "grc/model/grc_models_cltk/ner/proper_names.txt"
    ),
    "lat": os.path.join(
        CLTK_DATA_DIR, "lat/model/lat_models_cltk/ner/proper_names.txt"
    ),
}


def tag_ner(iso_code: str, input_tokens: List[str]) -> List[Union[bool, str]]:
    """Run NER for chosen language. Some languages return boolean True/False,
    others give string of entity type (e.g., ``LOC``).

    >>> from cltk.ner.ner import tag_ner
    >>> from cltk.languages.example_texts import get_example_text
    >>> from boltons.strutils import split_punct_ws
    >>> tokens = split_punct_ws(get_example_text(iso_code="lat"))
    >>> are_words_entities = tag_ner(iso_code="lat", input_tokens=tokens)
    >>> tokens[:5]
    ['Gallia', 'est', 'omnis', 'divisa', 'in']
    >>> are_words_entities[:5]
    [True, False, False, False, False]

    >>> text = "ἐπὶ δ᾽ οὖν τοῖς πρώτοις τοῖσδε Περικλῆς ὁ Ξανθίππου ᾑρέθη λέγειν. καὶ ἐπειδὴ καιρὸς ἐλάμβανε, προελθὼν ἀπὸ τοῦ σήματος ἐπὶ βῆμα ὑψηλὸν πεποιημένον, ὅπως ἀκούοιτο ὡς ἐπὶ πλεῖστον τοῦ ὁμίλου, ἔλεγε τοιάδε."
    >>> tokens = split_punct_ws(text)
    >>> are_words_entities = tag_ner(iso_code="grc", input_tokens=tokens)
    >>> tokens[:9]
    ['ἐπὶ', 'δ᾽', 'οὖν', 'τοῖς', 'πρώτοις', 'τοῖσδε', 'Περικλῆς', 'ὁ', 'Ξανθίππου']
    >>> are_words_entities[:9]
    [False, False, False, False, False, False, True, False, True]

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
