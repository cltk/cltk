"""Module for sentence tokenizers.
"""


from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core import CLTKException
from cltk.core.data_types import Doc, Process
from cltk.sentence.non import OldNorseRegexSentenceTokenizer
from cltk.sentence.sentence import SentenceTokenizer

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


@dataclass
class SentenceTokenizationProcess(Process):
    """To be inherited for each language's tokenization declarations.

    Example: ``SentenceTokenizationProcess`` -> ``OldNorseTokenizationProcess``

    >>> from cltk.tokenizers.processes import TokenizationProcess
    >>> from cltk.core.data_types import Process
    >>> issubclass(SentenceTokenizationProcess, Process)
    True
    >>> tok = SentenceTokenizationProcess()

    """

    model: object = None

    @cachedproperty
    def algorithm(self):
        raise CLTKException(
            f"No sentence tokenization algorithm for language '{self.language}'."
        )

    def run(self, input_doc: Doc) -> Doc:
        output_doc = deepcopy(input_doc)
        sentence_tokenizer = self.algorithm
        if not isinstance(sentence_tokenizer, SentenceTokenizer):
            raise CLTKException(
                "Algorithm must be an instance of SentenceTokenizer subclass"
            )

        sentences = sentence_tokenizer.tokenize(output_doc.raw, self.model)
        sentence_indices = []
        for i, sentence in enumerate(sentences):
            if i >= 1:
                sentence_indices.append(sentence_indices[-1] + len(sentences[i]))
            else:
                sentence_indices.append(len(sentence))
        sentence_index = 0
        for j, word in enumerate(output_doc.words):
            if sentence_indices[
                sentence_index
            ] < word.index_char_stop and sentence_index + 1 < len(sentence_indices):
                sentence_index += 1
            word.index_sentence = sentence_index
        return output_doc


@dataclass
class OldNorseSentenceTokenizationProcess(SentenceTokenizationProcess):
    """
    The default Old Norse sentence tokenization algorithm.

    >>> from cltk.core.data_types import Process, Pipeline
    >>> from cltk.sentence.processes import OldNorseSentenceTokenizationProcess
    >>> from cltk.tokenizers import OldNorseTokenizationProcess
    >>> from cltk.languages.utils import get_lang
    >>> from cltk.languages.example_texts import get_example_text

    >>> from cltk.nlp import NLP
    >>> pipe = Pipeline(description="A custom Old Norse pipeline", \
    processes=[OldNorseTokenizationProcess, OldNorseSentenceTokenizationProcess], \
    language=get_lang("non"))
    >>> nlp = NLP(language='non', custom_pipeline=pipe, suppress_banner=True)
    >>> output_doc = nlp.analyze(get_example_text("non"))
    >>> len(output_doc.sentences_strings)
    7
    """

    @cachedproperty
    def algorithm(self):
        return OldNorseRegexSentenceTokenizer()
