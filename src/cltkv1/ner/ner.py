"""Named entity recognition (NER)."""

import importlib.machinery
import os
from typing import List

from cltk.tokenize.word import WordTokenizer

from cltkv1.core.exceptions import UnimplementedLanguageError
from cltkv1.data.fetch import FetchCorpus
from cltkv1.languages.utils import get_lang
from cltkv1.utils import CLTK_DATA_DIR

__author__ = ["Natasha Voake <natashavoake@gmail.com>"]

NER_DICT = {
    "grc": os.path.join(
        CLTK_DATA_DIR, "grc/model/grc_models_cltk/ner/proper_names.txt"
    ),
    "lat": os.path.join(
        CLTK_DATA_DIR, "lat/model/lat_models_cltk/ner/proper_names.txt"
    ),
}


class NamedEntityReplacer(object):
    def __init__(self):

        self.entities = self._load_necessary_data()

    def _load_necessary_data(self):
        rel_path = os.path.join(
            CLTK_DATA_DIR, "french", "text", "french_data_cltk", "named_entities_fr.py"
        )
        path = os.path.expanduser(rel_path)
        # logger.info('Loading entries. This may take a minute.')
        loader = importlib.machinery.SourceFileLoader("entities", path)
        module = loader.load_module()
        entities = module.entities
        return entities

    def tag_ner_fr(self, input_text, output_type=list):
        """tags named entities in a string and outputs a list of tuples in the following format:
        (name, "entity", kind_of_entity)"""

        entities = self.entities

        for entity in entities:
            (name, kind) = entity

        word_tokenizer = WordTokenizer("french")
        tokenized_text = word_tokenizer.tokenize(input_text)
        ner_tuple_list = []

        match = False
        for word in tokenized_text:
            for name, kind in entities:
                if word == name:
                    named_things = [(name, "entity", kind)]
                    ner_tuple_list.append(named_things)
                    match = True
                    break
            else:
                ner_tuple_list.append((word,))
        return ner_tuple_list


def tag_ner(iso_code: str, input_tokens: List[str]) -> List[bool]:
    """Run NER for chosen language.

    >>> from cltkv1.ner.ner import tag_ner
    >>> from cltkv1.utils.example_texts import get_example_text
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
    """

    get_lang(iso_code=iso_code)
    if iso_code not in NER_DICT:
        msg = f"NER unavailable for language ``{iso_code}``."
        raise UnimplementedLanguageError(msg)

    ner_file_path = os.path.expanduser(NER_DICT[iso_code])
    with open(ner_file_path) as file_open:
        ner_str = file_open.read()
    ner_list = ner_str.split("\n")

    is_entity_list = []  # type: List[bool]
    for word_token in input_tokens:
        if word_token in ner_list:
            is_entity_list.append(True)
        else:
            is_entity_list.append(False)
    return is_entity_list
