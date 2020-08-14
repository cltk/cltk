import os
import importlib.machinery

from cltk.utils import CLTK_DATA_DIR
from cltk.lemmatize.naive_lemmatizer import DictionaryRegexLemmatizer


class OldEnglishDictionaryLemmatizer(DictionaryRegexLemmatizer):
    """
    Naive lemmatizer for Old English.
    """

    def _load_forms_and_lemmas(self):
        """Load the dictionary of lemmas and forms from the OE models repository."""

        rel_path = os.path.join(
            CLTK_DATA_DIR, "ang", "model", "ang_models_cltk", "data", "inverted_lemma_dict.py"
        )
        path = os.path.expanduser(rel_path)
        loader = importlib.machinery.SourceFileLoader("file", path)
        module = loader.load_module()
        return module.inverted_index

    def _load_unigram_counts(self):
        """Load the table of frequency counts of word forms."""

        rel_path = os.path.join(
            CLTK_DATA_DIR, "ang", "model", "ang_models_cltk", "data", "ang_unigrams.txt"
        )
        path = os.path.expanduser(rel_path)

        type_counts = {}

        with open(path, "r") as infile:
            lines = infile.read().splitlines()
            for line in lines:
                count, word = line.split()
                type_counts[word] = int(count)

        return type_counts

    def _specify_regex_rules(self):
        return []

    
