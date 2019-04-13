"""Wrapper for the Python Stanford NLP package `stanfordnlp`.
More here: <https://github.com/stanfordnlp/stanfordnlp>.
"""

import os

import stanfordnlp  # type: ignore
from typing import Dict
from typing import Optional

from cltk.exceptions import UnknownLanguageError
from cltk.utils import file_exists


class StanfordNLPWrapper:
    """CLTK's wrapper for the `stanfordnlp` project."""

    def __init__(self, language: str, treebank: Optional[str] = None) -> None:
        """Constructor for StanfordNLP wrapper class.

        >>> stanford_wrapper = StanfordNLPWrapper(language='latin')
        >>> isinstance(stanford_wrapper, StanfordNLPWrapper)
        True

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek', treebank='grc_perseus')
        >>> isinstance(stanford_wrapper, StanfordNLPWrapper)
        True
        """
        self.language = language
        self.treebank = treebank

        # Setup language
        self.map_langs_cltk_stanford = dict(greek='Ancient_Greek',
                                            latin='Latin',
                                            old_church_slavonic='Old_Church_Slavonic',
                                            old_french='Old_French')

        self.wrapper_available = self.is_wrapper_available()  # type: bool
        if not self.wrapper_available:
            raise UnknownLanguageError("Language '{}' either not in scope for CLTK or not supported by StanfordNLP.".format(self.language))
        self.stanford_code = self.get_stanford_code()

        # Setup optional treebank if specified
        self.map_code_treebanks = dict(grc=['grc_proiel', 'grc_perseus'],
                                       la=['la_perseus', 'la_proiel'])
        # if not specified, will use the default treebank of stanfordnlp
        if self.treebank:
            valid_treebank = self.is_valid_treebank()
            if not valid_treebank:
                raise UnknownLanguageError("Invalid treebank '{0}' for language '{1}'.".format(self.treebank, self.language))
        else:
            self.treebank = self.get_default_treebank()

        # check if model present
        # this fp is just to confirm that some model has already been downloaded. This is a weak check for the models actually being downloaded and valid
        self.model_path = os.path.expanduser('~/stanfordnlp_resources/{0}_models/{0}_tokenizer.pt'.format(self.treebank))
        if not self.is_model_present():
            # download model if necessary
            self.download_model()

        # instantiate actual stanfordnlp class
        self.nlp = self.load_pipeline()

    def load_pipeline(self):
        """Instantiate `stanfordnlp.Pipeline()`."""
        models_dir = os.path.expanduser('~/stanfordnlp_resources/')
        nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,pos,lemma,depparse',  # these are the default processors
                                        lang=self.stanford_code,
                                        models_dir=models_dir,
                                        treebank=self.treebank,
                                        use_gpu=True,  # default, won't fail if GPU not present
                                        )
        return nlp

    def parse(self, text):
        """Run all stanfordnlp parsing."""
        doc = self.nlp("Δαρείου καὶ Παρυσάτιδος γίγνονται παῖδες δύο, πρεσβύτερος μὲν Ἀρταξέρξης, νεώτερος δὲ Κῦρος: ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι. ὁ μὲν οὖν πρεσβύτερος παρὼν ἐτύγχανε: Κῦρον δὲ μεταπέμπεται ἀπὸ τῆς ἀρχῆς ἧς αὐτὸν σατράπην ἐποίησε, καὶ στρατηγὸν δὲ αὐτὸν ἀπέδειξε πάντων ὅσοι ἐς Καστωλοῦ πεδίον ἁθροίζονται.")

        doc.sentences[0].print_dependencies()
        '''
        ('Δαρείου', '4', 'iobj')
        ('καὶ', '1', 'cc')
        ('Παρυσάτιδος', '1', 'conj')
        ('γίγνονται', '0', 'root')
        ('παῖδες', '4', 'nsubj')
        ('δύο,', '5', 'nmod')
        ('πρεσβύτερος', '5', 'amod')
        ('μὲν', '7', 'discourse')
        ('Ἀρταξέρξης,', '7', 'nsubj')
        ('νεώτερος', '7', 'conj')
        ('δὲ', '10', 'discourse')
        ('Κῦρος:', '10', 'orphan')
        '''
        res = doc.sentences[0]
        print('dir:', dir(res))  # type: ignore
        # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_dependencies', '_process_tokens', '_tokens', '_words', 'build_dependencies', 'dependencies', 'print_dependencies', 'print_tokens', 'print_words', 'tokens', 'words']
        print('type:', type(res))  # type: ignore
        # <class 'stanfordnlp.pipeline.doc.Sentence'>
        print('res:', res)  # type: ignore
        # <stanfordnlp.pipeline.doc.Sentence object at 0x1cf484ef0>
        print('words:', res.words)  # type: ignore
        # [<Word index=1;text=Δαρείου;lemma=Δαρεῖος;upos=PROPN;xpos=Ne;feats=Case=Gen|Gender=Masc|Number=Sing;governor=4;dependency_relation=iobj>, <Word index=2;text=καὶ;lemma=καί;upos=CCONJ;xpos=C-;feats=_;governor=1;dependency_relation=cc>, <Word index=3;text=Παρυσάτιδος;lemma=Παρύσατις;upos=ADJ;xpos=A-;feats=Case=Gen|Degree=Pos|Gender=Masc|Number=Sing;governor=1;dependency_relation=conj>, <Word index=4;text=γίγνονται;lemma=γιγνώσκω;upos=VERB;xpos=V-;feats=Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Mid;governor=0;dependency_relation=root>, <Word index=5;text=παῖδες;lemma=παῖς;upos=NOUN;xpos=Nb;feats=Case=Nom|Gender=Masc|Number=Plur;governor=4;dependency_relation=nsubj>, <Word index=6;text=δύο,;lemma=δύο,;upos=NOUN;xpos=Nb;feats=Case=Nom|Gender=Masc|Number=Sing;governor=5;dependency_relation=nmod>, <Word index=7;text=πρεσβύτερος;lemma=πρέσβυς;upos=ADJ;xpos=A-;feats=Case=Nom|Degree=Cmp|Gender=Masc|Number=Sing;governor=5;dependency_relation=amod>, <Word index=8;text=μὲν;lemma=μέν;upos=ADV;xpos=Df;feats=_;governor=7;dependency_relation=discourse>, <Word index=9;text=Ἀρταξέρξης,;lemma=Ἀρταξέρξης;upos=PROPN;xpos=Ne;feats=Case=Nom|Gender=Masc|Number=Sing;governor=7;dependency_relation=nsubj>, <Word index=10;text=νεώτερος;lemma=νέος;upos=ADJ;xpos=A-;feats=Case=Nom|Degree=Cmp|Gender=Masc|Number=Sing;governor=7;dependency_relation=conj>, <Word index=11;text=δὲ;lemma=δέ;upos=ADV;xpos=Df;feats=_;governor=10;dependency_relation=discourse>, <Word index=12;text=Κῦρος:;lemma=Κῦρος:;upos=PROPN;xpos=Ne;feats=Case=Nom|Gender=Masc|Number=Sing;governor=10;dependency_relation=orphan>]
        print('tokens:', res.tokens)  # type: ignore
        # [<Token index=1;words=[<Word index=1;text=Δαρείου;lemma=Δαρεῖος;upos=PROPN;xpos=Ne;feats=Case=Gen|Gender=Masc|Number=Sing;governor=4;dependency_relation=iobj>]>, <Token index=2;words=[<Word index=2;text=καὶ;lemma=καί;upos=CCONJ;xpos=C-;feats=_;governor=1;dependency_relation=cc>]>, <Token index=3;words=[<Word index=3;text=Παρυσάτιδος;lemma=Παρύσατις;upos=ADJ;xpos=A-;feats=Case=Gen|Degree=Pos|Gender=Masc|Number=Sing;governor=1;dependency_relation=conj>]>, <Token index=4;words=[<Word index=4;text=γίγνονται;lemma=γιγνώσκω;upos=VERB;xpos=V-;feats=Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Mid;governor=0;dependency_relation=root>]>, <Token index=5;words=[<Word index=5;text=παῖδες;lemma=παῖς;upos=NOUN;xpos=Nb;feats=Case=Nom|Gender=Masc|Number=Plur;governor=4;dependency_relation=nsubj>]>, <Token index=6;words=[<Word index=6;text=δύο,;lemma=δύο,;upos=NOUN;xpos=Nb;feats=Case=Nom|Gender=Masc|Number=Sing;governor=5;dependency_relation=nmod>]>, <Token index=7;words=[<Word index=7;text=πρεσβύτερος;lemma=πρέσβυς;upos=ADJ;xpos=A-;feats=Case=Nom|Degree=Cmp|Gender=Masc|Number=Sing;governor=5;dependency_relation=amod>]>, <Token index=8;words=[<Word index=8;text=μὲν;lemma=μέν;upos=ADV;xpos=Df;feats=_;governor=7;dependency_relation=discourse>]>, <Token index=9;words=[<Word index=9;text=Ἀρταξέρξης,;lemma=Ἀρταξέρξης;upos=PROPN;xpos=Ne;feats=Case=Nom|Gender=Masc|Number=Sing;governor=7;dependency_relation=nsubj>]>, <Token index=10;words=[<Word index=10;text=νεώτερος;lemma=νέος;upos=ADJ;xpos=A-;feats=Case=Nom|Degree=Cmp|Gender=Masc|Number=Sing;governor=7;dependency_relation=conj>]>, <Token index=11;words=[<Word index=11;text=δὲ;lemma=δέ;upos=ADV;xpos=Df;feats=_;governor=10;dependency_relation=discourse>]>, <Token index=12;words=[<Word index=12;text=Κῦρος:;lemma=Κῦρος:;upos=PROPN;xpos=Ne;feats=Case=Nom|Gender=Masc|Number=Sing;governor=10;dependency_relation=orphan>]>]
        print('dependencies:', res.dependencies)  # type: ignore

        for token in res.tokens:  # type: ignore
            # print(type(token.words))
            # print(dir(token.words))
            word_obj = token.words[0]  # type: stanfordnlp.pipeline.doc.Word
            # print(dir(word_obj))
            print('index:', word_obj.index)
            print('text:', word_obj.text)
            print('lemma', word_obj.lemma)
            print('feats:', word_obj.feats)
            print('dependency_relation:', word_obj.dependency_relation)
            print('governor:', word_obj.governor)
            print('parent_token:', word_obj.parent_token)
            print('pos:', word_obj.pos)
            print('upos:', word_obj.upos)
            print('xpos:', word_obj.xpos)
            print('')

    def is_model_present(self) -> bool:
        """Checks if the model is already downloaded.
        """
        if file_exists(self.model_path):
            return True
        else:
            return False

    def download_model(self):
        """Interface with the `stanfordnlp` model downloader."""
        # prompt user to DL the stanford models
        print('')
        print('')
        print('Α' * 80)
        print('')
        print('CLTK message: The part of the CLTK that you are using depends upon the Stanford NLP library (`stanfordnlp`). What follows are several question prompts coming from it. (More at: <https://github.com/stanfordnlp/stanfordnlp>.) Answer with defaults.')
        print('')
        print('Ω' * 80)
        print('')
        print('')
        stanfordnlp.download(self.treebank)
        # if file model still not available after attempted DL, then raise error
        if not file_exists(self.model_path):
            raise FileNotFoundError('Missing required models for `stanfordnlp` at `{0}`.'.format(self.model_path))
        pass

    def get_default_treebank(self) -> str:
        """Return name of a language's default treebank if none
        supplied.

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek')
        >>> stanford_wrapper.get_default_treebank()
        'grc_proiel'
        """
        stanford_default_treebanks = stanfordnlp.utils.resources.default_treebanks  # type: Dict[str, str]
        return stanford_default_treebanks[self.stanford_code]

    def is_valid_treebank(self) -> bool:
        """Check whether for chosen language, optional
        treebank value is valid.

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek', treebank='grc_proiel')
        >>> stanford_wrapper.is_valid_treebank()
        True
        """
        possible_treebanks = self.map_code_treebanks[self.stanford_code]
        if self.treebank in possible_treebanks:
            return True
        else:
            return False

    def is_wrapper_available(self) -> bool:
        """Maps CLTK's internal language term (e.g., `latin`) to
        that used by `stanfordnlp` (`la`); confirm that this is
        a language the CLTK supports (i.e., is it Classical or not).

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek')
        >>> stanford_wrapper.is_wrapper_available()
        True
        """
        if self.language in self.map_langs_cltk_stanford:
            return True
        else:
            return False

    def get_stanford_code(self) -> str:
        """Using known-supported language, use the CLTK's
        internal code to look up the code used by StanfordNLP.

        >>> stanford_wrapper = StanfordNLPWrapper(language='latin')
        >>> stanford_wrapper.get_stanford_code()
        'la'
        """
        try:
            stanford_lang_name = self.map_langs_cltk_stanford[self.language]
        except KeyError:
            raise KeyError
        stanford_lang_code = stanfordnlp.models.common.constant.lang2lcode  # type: Dict[str, str]
        try:
            return stanford_lang_code[stanford_lang_name]
        except KeyError:
            raise KeyError


if __name__ == '__main__':

    stanford_nlp_obj = StanfordNLPWrapper(language='greek', treebank='grc_proiel')
    # stanford_nlp_obj = StanfordNLPWrapper(language='latin', treebank=None)
    print('')
    print('stanford_nlp_obj:', stanford_nlp_obj)
