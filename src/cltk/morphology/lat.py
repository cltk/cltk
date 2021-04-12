""" This modules provides Decliner for Latin. Given a lemma, the Decliner will provide each grammatically valid forms

This work is based on the lexical and linguistic data built for and by the Collatinus Team ( https://github.com/biblissima/collatinus ).
This module hence inherit the license from the original project. The objective of this module is to port part of Collatinus to CLTK.

"""

__author__ = ["Thibault Clerice"]
# credits also to "Yves Ouvrard" and "Philippe Verkerk"
__license__ = "GPL v3"


import json
import os
import re
from typing import Dict, List, Tuple

from cltk.core.exceptions import CLTKException
from cltk.utils import CLTK_DATA_DIR


class CollatinusDecliner:
    """Latin Decliner based on Collatinus data and approach to declining words for Latin

    .. code-block:: python

       # Ensure you have downloaded the corpus latin_models_cltk before running this
       from cltk.stem.lat.declension import CollatinusDecliner

       decliner = CollatinusDecliner()
       print(decliner.decline("via"))

        [
            ('via', '--s----n-'), ('via', '--s----v-'), ('viam', '--s----a-'), ('viae', '--s----g-'),
            ('viae', '--s----d-'), ('via', '--s----b-'), ('viae', '--p----n-'), ('viae', '--p----v-'),
            ('vias', '--p----a-'), ('viarum', '--p----g-'), ('viis', '--p----d-'), ('viis', '--p----b-')
        ]



    """

    _dism = re.compile(r"(\d+)")

    def __init__(self):
        path = os.path.join(
            CLTK_DATA_DIR, "lat/model/lat_models_cltk/lemmata/collatinus/collected.json"
        )
        path = os.path.expanduser(path)
        with open(path) as data_file:
            self._data = json.load(data_file)

        self._models = self._data["models"]
        self._lemmas = self._data["lemmas"]
        self._mapped = self._data["maps"]

    def __getPOS(self, key):
        """Get POS tag for key

        :param key: Key Index of Collatinus Morphos
        :return: Part-Of-Speech tag
        """
        return self._data["pos"][str(key)]

    def _remove_disambiguation(self, root):
        """Remove disambiguation index from lemma root

        :param root: Root in Collatinus
        :return: Cleaned root
        """
        return CollatinusDecliner._dism.sub("", root)

    def _getRoots(self, lemma, model):
        """Retrieve the known roots of a lemma

        :param lemma: Canonical form of the word (lemma)
        :type lemma: str
        :param model: Model data from the loaded self.__data__. Can be passed by decline()
        :type model: dict
        :return: Dictionary of roots with their root identifier as key
        :rtype: dict
        """

        if lemma not in self._lemmas:
            raise CLTKException("%s is unknown" % lemma)

        ROOT_IDS = {"K": "lemma", "1": "geninf", "2": "perf"}

        lemma_entry = self._lemmas[lemma]
        if "quantity" in lemma_entry and lemma_entry["quantity"]:
            lemma_in_lemma_entry = lemma_entry["quantity"]
        else:
            lemma_in_lemma_entry = self._remove_disambiguation(lemma_entry["lemma"])

        original_roots = {
            root_id: lemma_entry[root_name].split(",")
            for root_id, root_name in ROOT_IDS.items()
            if root_id != "K" and lemma_entry[root_name]
        }
        returned_roots = {}

        if not model:
            model = self._models[lemma_entry["model"]]

        # For each registered root in the model,
        for model_root_id, model_root_data in model["R"].items():

            # If we have K, it's equivalent to canonical form
            if model_root_data[0] == "K":
                returned_roots[model_root_id] = lemma_in_lemma_entry.split(",")
            # Otherwise we have deletion number and addition char
            else:
                deletion, addition = int(model_root_data[0]), model_root_data[1] or ""

                # If a the root is declared already,
                # we retrieve the information
                if model_root_id != "1" and model_root_id in returned_roots:
                    lemma_roots = returned_roots[model_root_id]
                else:
                    lemma_roots = lemma_in_lemma_entry.split(",")
                # We construct the roots
                returned_roots[model_root_id] = [
                    lemma_root[:-deletion] + addition for lemma_root in lemma_roots
                ]

            if model_root_id in original_roots:
                returned_roots[model_root_id].extend(original_roots[model_root_id])
            returned_roots[model_root_id] = list(set(returned_roots[model_root_id]))
        original_roots.update(returned_roots)

        return original_roots

    def decline(
        self, lemma: str, flatten: bool = False, collatinus_dict: bool = False
    ) -> List[Tuple[str, str]]:
        """ Decline a lemma

        .. warning:: POS are incomplete as we do not detect the type outside of verbs, participle and adjective.

        :raise CLTKException: When the lemma is unknown to our data

        :param lemma: Lemma (Canonical form) to decline
        :type lemma: str
        :param flatten: If set to True, returns a list of forms without natural language information about them
        :type flatten: bool
        :param collatinus_dict: If sets to True, Dictionary of grammatically valid forms, including variants, with keys\
         corresponding to morpho informations.
        :type collatinus_dict: bool
        :return: List of tuple where first value is the form and second the pos, ie [("sum", "v1ppip---")]
        :rtype: list or dict

        """

        if lemma in self._lemmas:
            # Get data information
            lemma_entry = self._lemmas[lemma]
        elif lemma in self._mapped and self._mapped[lemma] in self._lemmas:
            # Get data information
            lemma = self._mapped[lemma]
            lemma_entry = self._lemmas[self._mapped[lemma]]
        else:
            raise CLTKException("%s is unknown" % lemma)
        model = self._models[lemma_entry["model"]]

        # Get the roots
        roots = self._getRoots(lemma, model=model)
        # Get the known forms in order
        keys = sorted([int(key) for key in model["des"].keys()])
        forms_data = [(key, model["des"][str(key)]) for key in keys]

        # Generate the return dict
        forms = {key: [] for key in keys}
        for key, form_list in forms_data:
            for form in form_list:
                root_id, endings = tuple(form)
                for root in roots[root_id]:
                    for ending in endings:
                        forms[key].append(root + ending)

        # sufd means we have the original forms of the parent but we add a suffix
        if len(model["sufd"]):
            # For each constant form1
            for key, iter_forms in forms.items():
                new_forms = []
                # We add the constant suffix
                for sufd in model["sufd"]:
                    new_forms += [form + sufd for form in iter_forms]
                forms[key] = new_forms

        # If we need a secure version of the forms. For example, if we have variants
        if len(model["suf"]):
            cached_forms = {
                k: v + [] for k, v in forms.items()
            }  # Making cache without using copy

            # For each suffix
            # The format is [suffix characters, [modified forms]]
            for suffixes in model["suf"]:
                suffix, modified_forms = suffixes[0], suffixes[1]
                for modified_form in modified_forms:
                    forms[modified_form] += [
                        f + suffix for f in cached_forms[modified_form]
                    ]
            # We update with the new roots

        # If some form do not exist, we delete them prehentively
        if len(model["abs"]):
            for abs_form in model["abs"]:
                if abs_form in forms:
                    del forms[abs_form]

        if flatten:
            return list([form for case_forms in forms.values() for form in case_forms])
        elif collatinus_dict:
            return forms
        else:
            return list(
                [
                    (form, self.__getPOS(key))
                    for key, case_forms in forms.items()
                    for form in case_forms
                ]
            )

    @property
    def lemmas(self) -> Dict[str, Dict[str, str]]:
        return self._lemmas
