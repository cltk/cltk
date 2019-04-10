"""Wrapper for the Python Stanford NLP package `stanfordnlp`.
More here: <https://github.com/stanfordnlp/stanfordnlp>.
"""

import os
import sys

import stanfordnlp  # type: ignore

from cltk.utils import file_exists

if __name__ == '__main__':

    models_dir = os.path.expanduser('~/stanfordnlp_resources/')
    language = 'grc'  # type: str
    if language == 'grc':
        res = int(input('Which models, (1) PROIEL or (2) Perseus? '))
        assert res in [1, 2], "Invalid answer. Just 1 or 2."
        if res == 1:
            model = 'grc_proiel'  # type: str
        else:
            model = 'grc_perseus'

    model_path = os.path.expanduser('~/stanfordnlp_resources/{0}_models/{0}_tokenizer.pt'.format(language))
    if not file_exists(model_path):
        # prompt user to DL the stanford models
        print('')
        print('CLTK message: The part of the CLTK that you are using depends upon the `stanfordnlp` library. What follows are several question prompts coming from `stanfordnlp`. Answer with defaults.')
        print('')
        stanfordnlp.download(language)
        # if file model still not available after attempted DL, then raise error
        if not file_exists(model_path):
            raise FileNotFoundError('Missing required models for `stanfordnlp` at `{0}`.'.format(model_path))


    nlp = stanfordnlp.Pipeline(lang=language,
                               models_dir=models_dir,
                               treebank=model
                               )

    doc = nlp("Δαρείου καὶ Παρυσάτιδος γίγνονται παῖδες δύο, πρεσβύτερος μὲν Ἀρταξέρξης, νεώτερος δὲ Κῦρος: ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι. ὁ μὲν οὖν πρεσβύτερος παρὼν ἐτύγχανε: Κῦρον δὲ μεταπέμπεται ἀπὸ τῆς ἀρχῆς ἧς αὐτὸν σατράπην ἐποίησε, καὶ στρατηγὸν δὲ αὐτὸν ἀπέδειξε πάντων ὅσοι ἐς Καστωλοῦ πεδίον ἁθροίζονται.")

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
    print('dir:', dir(res))  # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_dependencies', '_process_tokens', '_tokens', '_words', 'build_dependencies', 'dependencies', 'print_dependencies', 'print_tokens', 'print_words', 'tokens', 'words']
    print('type:', type(res))  # <class 'stanfordnlp.pipeline.doc.Sentence'>
    print('res:', res)  # <stanfordnlp.pipeline.doc.Sentence object at 0x1cf484ef0>
    print('words:', res.words)  # [<Word index=1;text=Δαρείου;lemma=Δαρεῖος;upos=PROPN;xpos=Ne;feats=Case=Gen|Gender=Masc|Number=Sing;governor=4;dependency_relation=iobj>, <Word index=2;text=καὶ;lemma=καί;upos=CCONJ;xpos=C-;feats=_;governor=1;dependency_relation=cc>, <Word index=3;text=Παρυσάτιδος;lemma=Παρύσατις;upos=ADJ;xpos=A-;feats=Case=Gen|Degree=Pos|Gender=Masc|Number=Sing;governor=1;dependency_relation=conj>, <Word index=4;text=γίγνονται;lemma=γιγνώσκω;upos=VERB;xpos=V-;feats=Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Mid;governor=0;dependency_relation=root>, <Word index=5;text=παῖδες;lemma=παῖς;upos=NOUN;xpos=Nb;feats=Case=Nom|Gender=Masc|Number=Plur;governor=4;dependency_relation=nsubj>, <Word index=6;text=δύο,;lemma=δύο,;upos=NOUN;xpos=Nb;feats=Case=Nom|Gender=Masc|Number=Sing;governor=5;dependency_relation=nmod>, <Word index=7;text=πρεσβύτερος;lemma=πρέσβυς;upos=ADJ;xpos=A-;feats=Case=Nom|Degree=Cmp|Gender=Masc|Number=Sing;governor=5;dependency_relation=amod>, <Word index=8;text=μὲν;lemma=μέν;upos=ADV;xpos=Df;feats=_;governor=7;dependency_relation=discourse>, <Word index=9;text=Ἀρταξέρξης,;lemma=Ἀρταξέρξης;upos=PROPN;xpos=Ne;feats=Case=Nom|Gender=Masc|Number=Sing;governor=7;dependency_relation=nsubj>, <Word index=10;text=νεώτερος;lemma=νέος;upos=ADJ;xpos=A-;feats=Case=Nom|Degree=Cmp|Gender=Masc|Number=Sing;governor=7;dependency_relation=conj>, <Word index=11;text=δὲ;lemma=δέ;upos=ADV;xpos=Df;feats=_;governor=10;dependency_relation=discourse>, <Word index=12;text=Κῦρος:;lemma=Κῦρος:;upos=PROPN;xpos=Ne;feats=Case=Nom|Gender=Masc|Number=Sing;governor=10;dependency_relation=orphan>]
    print('tokens:', res.tokens)  # [<Token index=1;words=[<Word index=1;text=Δαρείου;lemma=Δαρεῖος;upos=PROPN;xpos=Ne;feats=Case=Gen|Gender=Masc|Number=Sing;governor=4;dependency_relation=iobj>]>, <Token index=2;words=[<Word index=2;text=καὶ;lemma=καί;upos=CCONJ;xpos=C-;feats=_;governor=1;dependency_relation=cc>]>, <Token index=3;words=[<Word index=3;text=Παρυσάτιδος;lemma=Παρύσατις;upos=ADJ;xpos=A-;feats=Case=Gen|Degree=Pos|Gender=Masc|Number=Sing;governor=1;dependency_relation=conj>]>, <Token index=4;words=[<Word index=4;text=γίγνονται;lemma=γιγνώσκω;upos=VERB;xpos=V-;feats=Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Mid;governor=0;dependency_relation=root>]>, <Token index=5;words=[<Word index=5;text=παῖδες;lemma=παῖς;upos=NOUN;xpos=Nb;feats=Case=Nom|Gender=Masc|Number=Plur;governor=4;dependency_relation=nsubj>]>, <Token index=6;words=[<Word index=6;text=δύο,;lemma=δύο,;upos=NOUN;xpos=Nb;feats=Case=Nom|Gender=Masc|Number=Sing;governor=5;dependency_relation=nmod>]>, <Token index=7;words=[<Word index=7;text=πρεσβύτερος;lemma=πρέσβυς;upos=ADJ;xpos=A-;feats=Case=Nom|Degree=Cmp|Gender=Masc|Number=Sing;governor=5;dependency_relation=amod>]>, <Token index=8;words=[<Word index=8;text=μὲν;lemma=μέν;upos=ADV;xpos=Df;feats=_;governor=7;dependency_relation=discourse>]>, <Token index=9;words=[<Word index=9;text=Ἀρταξέρξης,;lemma=Ἀρταξέρξης;upos=PROPN;xpos=Ne;feats=Case=Nom|Gender=Masc|Number=Sing;governor=7;dependency_relation=nsubj>]>, <Token index=10;words=[<Word index=10;text=νεώτερος;lemma=νέος;upos=ADJ;xpos=A-;feats=Case=Nom|Degree=Cmp|Gender=Masc|Number=Sing;governor=7;dependency_relation=conj>]>, <Token index=11;words=[<Word index=11;text=δὲ;lemma=δέ;upos=ADV;xpos=Df;feats=_;governor=10;dependency_relation=discourse>]>, <Token index=12;words=[<Word index=12;text=Κῦρος:;lemma=Κῦρος:;upos=PROPN;xpos=Ne;feats=Case=Nom|Gender=Masc|Number=Sing;governor=10;dependency_relation=orphan>]>]
    print('dependencies:', res.dependencies)

    for token in res.tokens:
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
