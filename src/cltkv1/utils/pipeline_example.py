"""An example of a proposed NLP pipeline system. Goals are to allow for:

   1. default NLP pipeline for any given language

   2. users to override default pipeline

   3. users to choose alternative code (classes/methods/functions) w/in the CLTK

   4. users to use their own custom code (inheriting or replacing those w/in CLTK)

   5. flexibility for the I/O for custom code

   6. up-front checking whether I/O is possible given available processed text (e.g., a fn might depend on token str,
   which must be created first)

   7. specify the order in which NLP algos are run

In the following, I propose these new data types:

   - ``Language``: Simple, just a place to hold attributes about a language. Can be referenced within
   ``Operation`` or ``Pipeline`` (e.g., ``LatinPipeline.language == LatinLanguage == True``).

   - ``Operation``: One for each type of NLP algo we cover (e.g., tokenization, sentence splitting, pos tagging,
   dependency, phonetics, prosody, etc.). Each of these is the subclassed for each language (e.g,
   ``TokenizationOperation`` <- ``LatinTokenizationOperation``). Here is defined the code to be used for a given
   operation, plus documenting a bit more about it (I/O, name, description).

   - ``Word``: This holds basic information for each token (start/end character indices, sentence index occurring
   within, raw string) and more advanced info if available (e.g., NER, POS tag, dependency relations).

   - ``Pipeline``: One for each language (e.g., ``Pipeline`` <- ``LatinPipeline``). A field in this is ``algo``,
   which has as value a given field (e.g., ``LatinPipeline.algo == LatinTokenizationOperation == True``.

   - ``Doc``: Returned by the ``NLP`` class (more specifically, by ``NLP().run_pipeline()``). Similar to what spaCy returns, only more transparent (IMHO). To the field ``Doc.tokens`` will be a list
   of ``Word`` (``List[Word]``).

Notes:

    - At the end of the module, see a dummy example of the ``cltk.NLP`` class and a use example (in ``"__main__"``),
    plus output.

    - Reqs Python 3.7

"""

from dataclasses import dataclass
import re
from typing import Any, Callable, List


# #####################################################################################
# #######################START LANGUAGE TYPE###########################################


@dataclass
class Language:
    name: str
    glottocode: str
    latitude: float
    longitude: float
    dates: List[float]
    family_id: str
    parent_id: str
    level: str
    iso639P3code: str
    type: str


LATIN = Language(
    name="Latin",
    glottocode="lati1261",
    latitude=60.2,
    longitude=50.5,
    dates=[200, 400],
    family_id="indo1319",
    parent_id="impe1234",
    level="language",
    iso639P3code="lat",
    type="a",
)


# #########################END LANGUAGE TYPE###########################################
# #####################################################################################


# #####################################################################################
# #######################START OPERATION TYPE##########################################


def dummy_get_token_indices(text: str) -> List[List[int]]:
    """Get the start/stop char indices of word boundaries.

    >>> john_damascus_corinth = "Τοῦτο εἰπὼν, ᾐνίξατο αἰτίους ὄντας"
    >>> indices_words = dummy_get_token_indices(text=john_damascus_corinth)
    >>> indices_words[0:3]
    [[0, 5], [6, 11], [13, 20]]
    """
    indices_words = list()
    pattern_word = re.compile(r"\w+")
    for word_match in pattern_word.finditer(string=text):
        idx_word_start, idx_word_stop = word_match.span()
        indices_words.append([idx_word_start, idx_word_stop])
    return indices_words


@dataclass
class Operation:
    """For each type of NLP operation there needs to be a definition.
    It includes the type of data it expects (``str``, ``List[str]``,
    ``Word``, etc.) and what field withing ``Word`` it will populate.
    This base class is intended to be inherited by NLP operation
    types (e.g., ``TokenizationOperation`` or ``DependencyOperation``).
    """

    name: str
    description: str
    input: Any
    output: Any
    algorithm: Callable
    type: str


@dataclass
class TokenizationOperation(Operation):
    """To be inherited for each language's tokenization declaration.

    Example: ``TokenizationOperation`` <- ``LatinTokenizationOperation``
    """

    type = "tokenization"


@dataclass
class LatinTokenizationOperation(TokenizationOperation):
    """The default (or one of many) Latin tokenization algorithm."""

    name = "CLTK Dummy Latin Tokenizer"
    description = "This is a simple regex which divides on word spaces (``r'\w+)`` for illustrative purposes."
    input = str
    output = List[List[int]]  # e.g., [[0, 4], [6, 11], ...]
    algorithm = dummy_get_token_indices
    language = LATIN


# #######################END OPERATION TYPE############################################
# #####################################################################################


# #####################################################################################
# #######################START WORD TYPE###############################################


@dataclass
class Word:
    """Contains attributes of each processed word in a list of tokens. To be used most often in the ``Doc.tokens``
    dataclass. """

    index_char_start: int = None
    index_char_stop: int = None
    index_token: int = None
    index_sentence: int = None
    string: str = None
    pos: str = None
    scansion: str = None


# #####################################################################################
# #######################END WORD TYPE#################################################


# #####################################################################################
# #######################START PIPELINE TYPE###########################################


@dataclass
class Pipeline:
    sentence_splitter: Callable[[str], List[List[int]]] = None
    word_tokenizer: Callable[[str], List[Word]] = None
    dependency: str = None
    pos: str = None
    scansion: Callable[[str], str] = None


@dataclass
class LatinPipeline(Pipeline):
    # sentence_splitter = LatinSplitter().dummy_get_indices
    word_tokenizer = LatinTokenizationOperation
    language = LATIN


# #######################END PIPELINE TYPE#############################################
# #####################################################################################


# #####################################################################################
# #######################START DOC TYPE################################################


@dataclass
class Doc:
    """The object returned to the user from the ``NLP()`` class. Contains overall attributes of submitted texts,
    plus most importantly the processed tokenized text ``tokens``, being a list of ``Word`` types.. """

    indices_sentences: List[List[int]] = None
    indices_tokens: List[List[int]] = None
    language: str = None
    tokens: List[Word] = None
    pipeline: Any = None
    raw: str = None
    ner: List[List[int]] = None


# #######################END DOC TYPE##################################################
# #####################################################################################


# #####################################################################################
# #######################START NLP CLASS###############################################


class NLP:
    """A dummy example of the primary entry-point class."""

    def __init__(self, language: str) -> None:
        self.language = language
        if self.language == "latin":
            self.pipeline = LatinPipeline
        else:
            raise NotImplementedError(
                f"Pipeline not available for language '{self.language}'."
            )

    def run_pipeline(self, text: str) -> Doc:
        """Take a raw unprocessed text string, then return a ``Doc`` object
        containing all available processed information.
        """
        # Get token indices
        token_indices = self.pipeline.word_tokenizer.algorithm(text=text)

        # Populate a ``Word`` object for each token in the submitted text
        all_word_tokens = list()
        for token_count, token_index in enumerate(token_indices):
            token_start = token_index[0]
            token_end = token_index[1]
            token_str = text[token_start:token_end]

            # index_char_start: int = None
            # index_char_stop: int = None
            # index_token: int = None
            # index_sentence: int = None
            # string: str = None
            # pos: str = None
            # scansion: str = None

            word = Word(
                index_char_start=token_start,
                index_char_stop=token_end,
                index_token=token_count,
                string=token_str,
            )
            all_word_tokens.append(word)

        doc = Doc(
            indices_tokens=token_indices,
            language=self.language,
            pipeline=self.pipeline,
            tokens=all_word_tokens,
            raw=text,
        )

        return doc


# #######################END NLP CLASS#################################################
# #####################################################################################


if __name__ == "__main__":
    tacitus_germanica = (
        "Germania omnis a Gallis Raetisque et Pannoniis Rheno et Danuvio fluminibus, a Sarmatis "
        "Dacisque mutuo metu aut montibus separatur: cetera Oceanus ambit, latos sinus et insularum "
        "inmensa spatia complectens, nuper cognitis quibusdam gentibus ac regibus, quos bellum "
        "aperuit. Rhenus, Raeticarum Alpium inaccesso ac praecipiti vertice ortus, modico flexu in "
        "occidentem versus septentrionali Oceano miscetur. Danuvius molli et clementer edito montis "
        "Abnobae iugo effusus pluris populos adit, donec in Ponticum mare sex meatibus erumpat: "
        "septimum os paludibus hauritur. "
    )
    cltk_nlp = NLP(language="latin")
    doc_germanica = cltk_nlp.run_pipeline(tacitus_germanica)

    print("")
    print("``Doc``:", doc_germanica)
    print("")
    print("``Doc.pipeline``:", doc_germanica.pipeline)
    print("")
    print(
        "``Doc.pipeline.word_tokenizer.name``:",
        doc_germanica.pipeline.word_tokenizer.name,
    )
    print("")
    print(
        "``Doc.pipeline.word_tokenizer.description``:",
        doc_germanica.pipeline.word_tokenizer.description,
    )
    print("")
    print("``Doc.pipeline.tokens[:10]``:", doc_germanica.tokens[:10])
    print("")
    print("``Doc.pipeline.indices_tokens[:10]``:", doc_germanica.indices_tokens[:10])
    print("")
