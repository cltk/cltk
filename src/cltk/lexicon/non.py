"""Code for querying Old Norse language dictionaries/lexicons."""

import regex
import yaml

from cltk.core.exceptions import CLTKException
from cltk.data.fetch import FetchCorpus
from cltk.utils.file_operations import make_cltk_path
from cltk.utils.utils import query_yes_no

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


class OldNorseZoegaLexicon:
    """Access a digital form of Zoëga's dictionary."""

    def __init__(self, interactive: bool = True):
        self.interactive = interactive
        self.zoega_yaml_fp = make_cltk_path(
            "non", "dictionary", "cltk_non_zoega_dictionary", "dictionary.yaml"
        )
        try:
            self.entries = self._load_entries()
        except FileNotFoundError:
            if self.interactive:
                dl_msg = f"This part of the CLTK depends upon Zoëga's *A Concise Old Norse Dictionary* (1890)."
                print(dl_msg)
                dl_question = "Do you want to download this?"
                do_download = query_yes_no(question=dl_question)
            else:
                do_download = True
            if do_download:
                fetch_corpus = FetchCorpus(language="non")
                fetch_corpus.import_corpus(corpus_name="cltk_non_zoega_dictionary")
            else:
                raise CLTKException(
                    f"File '{self.zoega_yaml_fp}' is not found. It is required for this class."
                )
            self.entries = self._load_entries()

    def lookup(self, lemma: str) -> str:
        """Perform match of a lemma against headwords. This is case sensitive.
        If more than one match, then return the concatenated entries. For example:

        >>> from cltk.lexicon.non import OldNorseZoegaLexicon
        >>> onzl = OldNorseZoegaLexicon(interactive=False)
        >>> onzl.lookup("sonr")
        '(gen. sonar, dat. syni and søni; pl. synir, sønir; ace. sonu and syni), m. son.'
        """
        if not self.entries:
            raise CLTKException(
                "No dictionary entries found in the .yaml file. This should never happen."
            )

        if regex.match(r"^[0-9\.\?,\:;\!\<\>\-]*$", lemma) is not None:
            return ""

        keys = self.entries.keys()
        matches = [key for key in keys if regex.match(rf"^{lemma}[0-9]?$", key)]
        n_matches = len(matches)
        if n_matches > 1:
            return "\n".join([self.entries[key] for key in matches])
        elif n_matches == 1:
            return self.entries[matches[0]]
        else:
            return ""

    def _load_entries(self):
        """Read the yaml file of the lexion."""
        with open(self.zoega_yaml_fp) as file_open:
            entries = yaml.load(file_open, Loader=yaml.Loader)
        return entries
