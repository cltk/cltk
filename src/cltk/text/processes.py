"""

"""

from copy import deepcopy
from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltk.core import Doc, Process
from cltk.text.non import OldNorsePunctuationRemover


@dataclass
class PunctuationRemovalProcess(Process):
    """"""

    def run(self, input_doc: Doc) -> Doc:
        punctuation_remover = self.algorithm

        output_doc = deepcopy(input_doc)
        output_doc.words = [
            word for word in output_doc.words if not punctuation_remover(word)
        ]
        return output_doc


class DefaultPunctuationRemovalProcess(PunctuationRemovalProcess):

    description = "Default punctuation removal algorithm"

    @cachedproperty
    def algorithm(self):
        return DefaultPunctuationRemover()


DEFAULT_PUNCTUATION = [".", ",", ";", ":", '"', "'", "!", "?"]


class DefaultPunctuationRemover:
    """"""

    def __init__(self):
        pass

    def filter(self, word):
        return word.string in DEFAULT_PUNCTUATION

    def __repr__(self):
        return f"<DefaultPunctuationRemover>"

    def __call__(self, word):
        return self.filter(word)


class OldNorsePunctuationRemovalProcess(PunctuationRemovalProcess):

    description = "Default Old Norse punctuation removal algorithm"

    @cachedproperty
    def algorithm(self):
        return OldNorsePunctuationRemover()
