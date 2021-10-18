import importlib.machinery
import os

from cltk.lemmatize.naive_lemmatizer import DictionaryRegexLemmatizer
from cltk.ner.spacy_ner import download_prompt
from cltk.utils import CLTK_DATA_DIR


class OldEnglishDictionaryLemmatizer(DictionaryRegexLemmatizer):
    """
    Naive lemmatizer for Old English.

    TODO: Add silent and non-interactive options to this class

    >>> lemmatizer = OldEnglishDictionaryLemmatizer()
    >>> lemmatizer.lemmatize_token('ġesāƿen')
    'geseon'
    >>> lemmatizer.lemmatize_token('ġesāƿen', return_frequencies=True)
    ('geseon', -6.519245611523386)
    >>> lemmatizer.lemmatize_token('ġesāƿen', return_frequencies=True, best_guess=False)
    [('geseon', -6.519245611523386), ('gesaƿan', 0), ('saƿan', 0)]
    >>> lemmatizer.lemmatize(['Same', 'men', 'cweþaþ', 'on', 'Englisc', 'þæt', 'hit', 'sie', 'feaxede', 'steorra', 'forþæm', 'þær', 'stent', 'lang', 'leoma', 'of', 'hwilum', 'on', 'ane', 'healfe', 'hwilum', 'on', 'ælce', 'healfe'], return_frequencies=True, best_guess=False)
    [[('same', -8.534148632065651), ('sum', -5.166852802079177)], [('mann', -6.829400539827225)], [('cweþan', -9.227295812625597)], \
[('an', -5.02260319323463), ('on', -2.210686128731377)], [('englisc', -8.128683523957486)], [('þæt', -2.365584472144866), \
('se', -2.9011463394704973)], [('hit', -4.300042127468392)], [('wesan', -7.435536343397541)], [('feaxede', -9.227295812625597)], \
[('steorra', -8.534148632065651)], [('forðam', -6.282856833459156)], [('þær', -3.964605623720711)], [('standan', -7.617857900191496)], \
[('lang', -6.829400539827225)], [('leoma', -7.841001451505705)], [('of', -3.9440920838876075)], [('hwilum', -6.282856833459156)], \
[('an', -5.02260319323463), ('on', -2.210686128731377)], [('an', -5.02260319323463)], [('healf', -7.841001451505705)], \
[('hwilum', -6.282856833459156)], [('an', -5.02260319323463), ('on', -2.210686128731377)], [('ælc', -7.841001451505705)], \
[('healf', -7.841001451505705)]]

    """

    def _load_forms_and_lemmas(self):
        """Load the dictionary of lemmas and forms from the OE models repository."""

        rel_path = os.path.join(
            CLTK_DATA_DIR,
            "ang",
            "model",
            "ang_models_cltk",
            "data",
            "inverted_lemma_dict.py",
        )
        path = os.path.expanduser(rel_path)
        if not os.path.isfile(path=path):
            dl_msg = f"This part of the CLTK depends upon models from the CLTK project."
            repo_url = "https://github.com/cltk/ang_models_cltk"
            download_prompt(iso_code="ang", message=dl_msg, model_url=repo_url)
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
