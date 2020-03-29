"""This module holds the ``Process``es, related to embeddings,
that are called by ``Pipeline``s.
"""

from dataclasses import dataclass
from typing import Callable

import numpy as np
from boltons.cacheutils import cachedproperty

from cltkv1.core.data_types import Doc, Process
from cltkv1.embeddings.embeddings import FastTextEmbeddings


@dataclass
class EmbeddingsProcess(Process):
    """To be inherited for each language's embeddings declarations.

    .. note::
        There can be no ``DefaultEmbeddingsProcess`` because word embeddings are naturally language-specific.

    Example: ``EmbeddingsProcess`` <- ``LatinEmbeddingsProcess``

    >>> from cltkv1.core.data_types import Doc
    >>> from cltkv1.embeddings.processes import EmbeddingsProcess
    >>> from cltkv1.core.data_types import Process
    >>> issubclass(EmbeddingsProcess, Process)
    True
    >>> emb_proc = EmbeddingsProcess(input_doc=Doc(raw="some input data"))
    """

    language: str = None

    @cachedproperty
    def algorithm(self):
        return FastTextEmbeddings(iso_code=self.language)

    def run(self):
        tmp_doc = self.input_doc
        embedding_length = None
        embeddings_obj = self.algorithm
        for index, word_obj in enumerate(tmp_doc.words):
            if not embedding_length:
                embedding_length = embeddings_obj.get_embedding_length()
            word_embedding = embeddings_obj.get_word_vector(word=word_obj.string)
            if not isinstance(word_embedding, np.ndarray):
                word_embedding = np.zeros([embedding_length])
            word_obj.embedding = word_embedding
            tmp_doc.words[index] = word_obj
        self.output_doc = tmp_doc


@dataclass
class ArabicEmbeddingsProcess(EmbeddingsProcess):
    """The default Arabic embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc, Word
    >>> from cltkv1.embeddings.processes import ArabicEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> language = "arb"
    >>> example_text = get_example_text(language)
    >>> tokens = [Word(string=token) for token in example_text.split(" ")]
    >>> a_process = ArabicEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
    >>> a_process.run()
    >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
    True
    """

    description: str = "Default embeddings for Arabic."
    language: str = "arb"


@dataclass
class AramaicEmbeddingsProcess(EmbeddingsProcess):
    """The default Aramaic embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc, Word
    >>> from cltkv1.embeddings.processes import AramaicEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> language = "arc"
    >>> example_text = get_example_text(language)
    >>> tokens = [Word(string=token) for token in example_text.split(" ")]
    >>> a_process = AramaicEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
    >>> a_process.run()
    >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
    True
    """

    description: str = "Default embeddings for Aramaic."
    language: str = "arb"


@dataclass
class GothicEmbeddingsProcess(EmbeddingsProcess):
    """The default Gothic embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc, Word
    >>> from cltkv1.embeddings.processes import GothicEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> language = "got"
    >>> example_text = get_example_text(language)
    >>> tokens = [Word(string=token) for token in example_text.split(" ")]
    >>> a_process = GothicEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
    >>> a_process.run()
    >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
    True
    """

    description: str = "Default embeddings for Gothic."
    language: str = "got"


@dataclass
class LatinEmbeddingsProcess(EmbeddingsProcess):
    """The default Latin embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc, Word
    >>> from cltkv1.embeddings.processes import LatinEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> language = "lat"
    >>> example_text = get_example_text(language)
    >>> tokens = [Word(string=token) for token in example_text.split(" ")]
    >>> a_process = LatinEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
    >>> a_process.run()
    >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
    True
    """

    language: str = "lat"
    description: str = "Default embeddings for Latin."


@dataclass
class OldEnglishEmbeddingsProcess(EmbeddingsProcess):
    """The default Old English embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc, Word
    >>> from cltkv1.embeddings.processes import OldEnglishEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> language = "ang"
    >>> example_text = get_example_text(language)
    >>> tokens = [Word(string=token) for token in example_text.split(" ")]
    >>> a_process = OldEnglishEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
    >>> a_process.run()
    >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
    True
    """

    description: str = "Default embeddings for Old English."
    language: str = "ang"


@dataclass
class PaliEmbeddingsProcess(EmbeddingsProcess):
    """The default Pali embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc, Word
    >>> from cltkv1.embeddings.processes import PaliEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> language = "pli"
    >>> example_text = get_example_text(language)
    >>> tokens = [Word(string=token) for token in example_text.split(" ")]
    >>> a_process = PaliEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
    >>> a_process.run()
    >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
    True
    """

    description: str = "Default embeddings for Pali."
    language: str = "pli"


@dataclass
class SanskritEmbeddingsProcess(EmbeddingsProcess):
    """The default Sanskrit embeddings algorithm.

    >>> from cltkv1.core.data_types import Doc, Word
    >>> from cltkv1.embeddings.processes import SanskritEmbeddingsProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> language = "san"
    >>> example_text = get_example_text(language)
    >>> tokens = [Word(string=token) for token in example_text.split(" ")]
    >>> a_process = SanskritEmbeddingsProcess(input_doc=Doc(raw=get_example_text(language), words=tokens))
    >>> a_process.run()
    >>> isinstance(a_process.output_doc.words[1].embedding, np.ndarray)
    True
    """

    description: str = "Default embeddings for Sanskrit."
    language: str = "san"


if __name__ == "__main__":
    from datetime import datetime

    t0 = datetime.now()
    from boltons.strutils import split_punct_ws
    from cltkv1.core.data_types import Word
    from cltkv1.utils.example_texts import get_example_text

    first_doc = Doc(raw=get_example_text("lat"), language="lat")
    first_doc.words = [Word(string=w) for w in split_punct_ws(first_doc.raw)]
    lat_emb_proc = LatinEmbeddingsProcess(input_doc=first_doc)
    # print(lat_emb_proc.output_doc)
    lat_emb_proc.run()
    # print(lat_emb_proc.output_doc)
    t1 = datetime.now()
    print("Finished processing doc 1, took:", t1 - t0)

    second_text = "Dominus et magister noster Iesus Christus dicendo Penitentiam omnem vitam fidelium penitentiam esse voluit."
    second_doc = Doc(raw=second_text, language="lat")
    second_doc.words = [Word(string=w) for w in split_punct_ws(second_text)]
    lat_emb_proc.input_doc = second_doc
    lat_emb_proc.run()
    # print(lat_emb_proc.output_doc)
    t2 = datetime.now()
    print("Finished processing doc 2, took another:", t2 - t1)
    print("Total time:", t2 - t0)
    # input()
    # print(second_doc.words)

    print("Now going to do OE ...")
    input()
    lang = "ang"
    first_doc = Doc(raw=get_example_text(lang), language=lang)
    first_doc.words = [Word(string=w) for w in split_punct_ws(first_doc.raw)]
    ang_emb_proc = OldEnglishEmbeddingsProcess(input_doc=first_doc)
    print(ang_emb_proc.output_doc)
    ang_emb_proc.run()
    print(ang_emb_proc.output_doc)
