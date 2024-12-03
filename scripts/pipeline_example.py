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
   ``Process`` or ``Pipeline`` (e.g., ``LatinPipeline.language == LatinLanguage == True``).

   - ``Process``: One for each type of NLP algo we cover (e.g., tokenization, sentences splitting, pos tagging,
   dependency, phonetics, prosody, etc.). Each of these is the subclassed for each language (e.g,
   ``TokenizationProcess`` <- ``LatinTokenizationOperation``). Here is defined the code to be used for a given
   operation, plus documenting a bit more about it (I/O, description, description).

   - ``Word``: This holds basic information for each token (start/end character indices, sentences index occurring
   within, raw string) and more advanced info if available (e.g., NER, POS tag, dependency relations).

   - ``Pipeline``: One for each language (e.g., ``Pipeline`` <- ``LatinPipeline``). A field in this is ``algo``,
   which has as value a given field (e.g., ``LatinPipeline.algo == LatinTokenizationOperation == True``.

   - ``Doc``: Returned by the ``NLP`` class (more specifically, by ``NLP().run_pipeline()``). Similar to what spaCy returns, only more transparent (IMHO). To the field ``Doc.words`` will be a list
   of ``Word`` (``list[Word]``).

Notes:

    - At the end of the module, see a dummy example of the ``cltk.NLP`` class and a use example (in ``"__main__"``),
    plus op_output.

    - Reqs Python 3.7

"""

import re
from dataclasses import dataclass
from typing import List, Callable
import inspect

# Mock classes
class Word:
    def __init__(self, text):
        self.text = text

class Operation:
    def __init__(self, name):
        self.name = name

    def execute(self, data):
        return data

class Process:
    def __init__(self, name):
        self.name = name

    def run(self, data):
        return data

# Mock LANGUAGES
LANGUAGES = {
    "lat": "Latin"
}

# Mock NLP class
class NLP:
    def __init__(self, language):
        self.language = language
        self.pipeline = LatinPipeline()

    def run_pipeline(self, text):
        # Simulated processing
        return Doc(self.pipeline, text)

# Mock Doc class
class Doc:
    def __init__(self, pipeline, text):
        self.pipeline = pipeline
        self.tokens = [Word(text[i:i+1]) for i in range(len(text))]  # Apply tokenizer (mocked)
        self.indices_tokens = pipeline.word_tokenizer.algorithm(text)  # Assuming tokens are indices for this mock

# #####################################################################################
# #######################START OPERATION TYPE##########################################


def dummy_get_token_indices(text: str) -> List[List[int]]:
    """Get the start/stop char indices of word boundaries.

    >>> john_damascus_corinth = "Τοῦτο εἰπὼν, ᾐνίξατο αἰτίους ὄντας"
    >>> indices_words = dummy_get_token_indices(text=john_damascus_corinth)
    >>> indices_words[0:3]
    [[0, 5], [6, 11], [13, 20]]
    """
    indices_words = []
    pattern_word = re.compile(r"\w+")
    for word_match in pattern_word.finditer(string=text):
        idx_word_start, idx_word_stop = word_match.span()
        indices_words.append([text[idx_word_start:idx_word_stop]])  # Extract actual token
    return indices_words


@dataclass
class TokenizationOperation(Operation):
    """To be inherited for each language's tokenization declaration.

    Example: ``TokenizationProcess`` <- ``LatinTokenizationOperation``
    """

    type = "tokenization"


@dataclass
class LatinTokenizationOperation(TokenizationOperation):
    """The default (or one of many) Latin tokenization algorithm."""

    name: str
    description: str
    input: type
    output: List[List[int]]
    algorithm: Callable[[str], List[List[int]]]
    language: str


# #######################END OPERATION TYPE############################################
# #####################################################################################


# #####################################################################################
# #######################START PIPELINE TYPE###########################################


@dataclass
class Pipeline:
    sentence_splitter: Callable[[str], List[List[int]]] = None
    word_tokenizer: LatinTokenizationOperation = None
    dependency: str = None
    pos: str = None
    scansion: Callable[[str], str] = None


@dataclass
class LatinPipeline(Pipeline):
    def __init__(self):
        self.word_tokenizer = LatinTokenizationOperation(
            name="CLTK Dummy Latin Tokenizer",
            description="Simple regex tokenizer",
            input=str,
            output=[],
            algorithm=dummy_get_token_indices,
            language=LANGUAGES["lat"]
        )

def get_process_subclasses():
    subclasses = []
    for name, obj in inspect.getmembers(__import__('__main__')):
        if inspect.isclass(obj) and issubclass(obj, Process) and obj is not Process:
            subclass_name = obj.__name__
            subclass_str = subclass_name.lower()
            subclasses.append((subclass_name, subclass_str))
    return subclasses


# #######################END PIPELINE TYPE#############################################
# #####################################################################################


if __name__ == "__main__":
    LAT = "Your placeholder text or data here"

    cltk_nlp = NLP(language="lat")
    doc_germanica = cltk_nlp.run_pipeline(LAT)

    print("")
    print("``Doc``:", doc_germanica)
    print("")
    print("``Doc.pipeline``:", doc_germanica.pipeline)
    print("")
    print(
        "``Doc.pipeline.word_tokenizer.description``:",
        doc_germanica.pipeline.word_tokenizer.name,
    )
    print("")
    print(
        "``Doc.pipeline.word_tokenizer.description``:",
        doc_germanica.pipeline.word_tokenizer.description,
    )
    print("")
    print("``Doc.pipeline.words[:10]``:", doc_germanica.tokens[:10])
    print("")
    print("``Doc.pipeline.indices_tokens[:10]``:", doc_germanica.indices_tokens[:10])
    print("")

    subclasses = get_process_subclasses()
    print("List of Process Subclasses:")
    print(subclasses)
