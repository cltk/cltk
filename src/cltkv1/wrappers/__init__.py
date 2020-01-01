"""Init for `cltkv1.wrappers`."""

from cltkv1.utils.data_types import Doc, Process, Word

from .stanford import StanfordNLPWrapper

import copy

class StanfordNLPProcess(Process):
    """A ``Process`` type to capture everything
    that the ``stanfordnlp`` project can do for a
    given language.


    .. note::
        ``stanfordnlp`` has only partial functionality available for some languages.


    >>> from cltkv1.wrappers import StanfordNLPProcess
    >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
    >>> process_stanford = StanfordNLPProcess(data_input=EXAMPLE_TEXTS["lat"], language="lat")
    >>> isinstance(process_stanford, StanfordNLPProcess)
    True
    >>> from stanfordnlp.pipeline.doc import Document
    >>> _ = process_stanford.data_output
    >>> isinstance(process_stanford.stanfordnlp_doc, Document)
    True
    """

    def __init__(self, input_doc, language):
        """Constructor."""
        super().__init__(input_doc = input_doc, language = language)
        self.stanfordnlp_wrapper = StanfordNLPWrapper.get_nlp(language = self.language)
        
    def algorithm(self, doc_in):
        stanfordnlp_doc = self.stanfordnlp_wrapper.parse(doc_in.raw)
        (cltk_words, indices_tokens) = StanfordNLPProcess.stanfordnlp_to_cltk_word_type(stanfordnlp_doc)
        doc_out = copy.deepcopy(doc_in)
        doc_out.words = cltk_words
        doc_out.indices_tokens = indices_tokens
        doc_out.stanfordnlp_doc = stanfordnlp_doc

        return doc_out

    @staticmethod
    def stanfordnlp_to_cltk_word_type(stanfordnlp_doc):
        """Take an entire ``stanfordnlp`` document, extract
        each word, and encode it in the way expected by
        the CLTK's ``Word`` type.

        >>> from cltkv1.wrappers import StanfordNLPProcess
        >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
        >>> process_stanford = StanfordNLPProcess(data_input=EXAMPLE_TEXTS["lat"], language="lat")
        >>> cltk_words = process_stanford.data_output
        >>> isinstance(cltk_words, list)
        True
        >>> isinstance(cltk_words[0], Word)
        True
        >>> cltk_words[0]
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='Gallia', pos='A1|grn1|casA|gen2|stAM', lemma='aallius', scansion=None, xpos='A1|grn1|casA|gen2|stAM', upos='NOUN', dependency_relation='nsubj', governor=4, parent_token=<Token index=1;words=[<Word index=1;text=Gallia;lemma=aallius;upos=NOUN;xpos=A1|grn1|casA|gen2|stAM;feats=Case=Nom|Degree=Pos|Gender=Fem|Number=Sing;governor=4;dependency_relation=nsubj>]>, feats='Case=Nom|Degree=Pos|Gender=Fem|Number=Sing')
        """
        words_list = list()
        sentence_list = list()
        # print('* * * ', dir(self.nlp_doc_stanford))  # .sentences, .text, .conll_file, .load_annotations, .write_conll_to_file
        # .text is the raw str
        # .sentences is list
        for sentence_index, sentence in enumerate(stanfordnlp_doc.sentences):
            token_indices = list()

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
                    governor=stanfordnlp_word.governor,
                    parent_token=stanfordnlp_word.parent_token,
                    feats=stanfordnlp_word.feats,
                )
                words_list.append(cltk_word)
                token_indices.append(token_index)
            sentence_list.append(token_indices)

        return (words_list, sentence_list)
