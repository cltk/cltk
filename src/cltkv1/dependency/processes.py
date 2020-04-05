from dataclasses import dataclass

from boltons.cacheutils import cachedproperty

from cltkv1.core.data_types import Doc, Process, Word
from cltkv1.dependency.stanford import StanfordNLPWrapper
from cltkv1.dependency.tree import DependencyTree


@dataclass
class StanfordNLPProcess(Process):
    """A ``Process`` type to capture everything
    that the ``stanfordnlp`` project can do for a
    given language.


    .. note::
        ``stanfordnlp`` has only partial functionality available for some languages.


    >>> from cltkv1.dependency.processes import StanfordNLPProcess
    >>> from cltkv1.utils.example_texts import get_example_text
    >>> process_stanford = StanfordNLPProcess(input_doc=Doc(raw=get_example_text("lat")), language="lat")
    >>> isinstance(process_stanford, StanfordNLPProcess)
    True
    >>> from stanfordnlp.pipeline.doc import Document
    >>> process_stanford.run()
    >>> isinstance(process_stanford.output_doc.stanfordnlp_doc, Document)
    True
    """

    language: str = None

    @cachedproperty
    def algorithm(self):
        return StanfordNLPWrapper.get_nlp(language=self.language)

    def run(self):
        tmp_doc = self.input_doc
        stanfordnlp_wrapper = self.algorithm
        stanfordnlp_doc = stanfordnlp_wrapper.parse(tmp_doc.raw)
        cltk_words = self.stanfordnlp_to_cltk_word_type(stanfordnlp_doc)
        tmp_doc.words = cltk_words
        tmp_doc.stanfordnlp_doc = stanfordnlp_doc
        self.output_doc = tmp_doc

    @staticmethod
    def stanfordnlp_to_cltk_word_type(stanfordnlp_doc):

        """Take an entire ``stanfordnlp`` document, extract
        each word, and encode it in the way expected by
        the CLTK's ``Word`` type.

        >>> from cltkv1.dependency.processes import StanfordNLPProcess
        >>> from cltkv1.utils.example_texts import get_example_text
        >>> process_stanford = StanfordNLPProcess(input_doc=Doc(raw=get_example_text("lat")), language="lat")
        >>> process_stanford.run()
        >>> cltk_words = process_stanford.output_doc.words
        >>> isinstance(cltk_words, list)
        True
        >>> isinstance(cltk_words[0], Word)
        True
        >>> cltk_words[0]
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='Gallia', pos='A1|grn1|casA|gen2|stAM', lemma='aallius', scansion=None, xpos='A1|grn1|casA|gen2|stAM', upos='NOUN', dependency_relation='nsubj', governor=Word(index_char_start=None, index_char_stop=None, index_token=4, index_sentence=0, string='divisa', pos='L2', lemma='divido', scansion=None, xpos='L2', upos='VERB', dependency_relation='root', governor=None, parent=None, features={'Aspect': 'Perf', 'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing', 'Tense': 'Past', 'VerbForm': 'Part', 'Voice': 'Pass'}, embedding=None, stop=None), parent=None, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, embedding=None, stop=None)
        """
        words_list = list()

        for sentence_index, sentence in enumerate(stanfordnlp_doc.sentences):
            sent_words = dict()
            indices = list()

            for token_index, token in enumerate(sentence.tokens):
                stanfordnlp_word = token.words[0]
                cltk_word = Word(
                    index_token=int(stanfordnlp_word.index),  # same as ``token.index``
                    index_sentence=sentence_index,
                    string=stanfordnlp_word.text,  # same as ``token.text``
                    pos=stanfordnlp_word.pos,
                    xpos=stanfordnlp_word.xpos,
                    upos=stanfordnlp_word.upos,
                    lemma=stanfordnlp_word.lemma,
                    dependency_relation=stanfordnlp_word.dependency_relation,
                    features={}
                    if stanfordnlp_word.feats == "_"
                    else dict(
                        [f.split("=") for f in stanfordnlp_word.feats.split("|")]
                    ),
                )
                sent_words[cltk_word.index_token] = cltk_word
                indices.append(
                    (
                        int(stanfordnlp_word.governor),
                        int(stanfordnlp_word.parent_token.index),
                    )
                )
                words_list.append(cltk_word)

            for i, cltk_word in enumerate(sent_words.values()):
                (governor_index, parent_index) = indices[i]
                cltk_word.governor = (
                    sent_words[governor_index] if governor_index > 0 else None
                )
                if cltk_word.index_token != sent_words[parent_index].index_token:
                    cltk_word.parent = sent_words[parent_index]

        return words_list


@dataclass
class GreekStanfordNLPProcess(StanfordNLPProcess):
    language: str = "grc"
    description: str = "Default process for StanfordNLP for the Ancient Greek language."


@dataclass
class LatinStanfordNLPProcess(StanfordNLPProcess):
    language: str = "lat"
    description: str = "Default process for StanfordNLP for the Latin language."


@dataclass
class OCSStanfordNLPProcess(StanfordNLPProcess):
    language: str = "chu"
    description: str = "Default process for StanfordNLP for the Old Church Slavonic language."


@dataclass
class OldFrenchStanfordNLPProcess(StanfordNLPProcess):
    language: str = "fro"
    description: str = "Default process for StanfordNLP for the Old French language."


@dataclass
class GothicStanfordNLPProcess(StanfordNLPProcess):
    language: str = "got"
    description: str = "Default process for StanfordNLP for the Gothic language."


class TreeBuilderProcess(Process):
    """A ``Process`` that takes a doc containing sentences of CLTK words
    and returns a dependency tree for each sentences.

    TODO: JS help to make this work, illustrate better.

    >>> from cltkv1 import NLP
    >>> nlp = NLP(language="got")
    >>> from cltkv1.dependency.processes import TreeBuilderProcess

    # >>> nlp.pipeline.add_process(TreeBuilderProcess)
    # >>> from cltkv1.utils.example_texts import get_example_text
    # >>> doc = nlp.analyze(text=get_example_text("got"))
    # >>> len(doc.trees)
    # 4
    """

    def algorithm(self, doc):
        doc.trees = [DependencyTree.to_tree(sentence) for sentence in doc.sentences]
        return doc
