"""Wrapper for the Python Stanford NLP package `stanfordnlp`.
More here: <https://github.com/stanfordnlp/stanfordnlp>.
"""

import os

import stanfordnlp

def file_exists(file_path, is_dir=False):
    """Try to expand `~/` and check if a file or dir exists.
    Optionally check if it's a dir.
    """
    file_path_expanded = os.path.expanduser(file_path)
    if is_dir:
        exists = os.path.isdir(file_path_expanded)
    else:
        exists = os.path.isfile(file_path_expanded)
    return exists

if __name__ == '__main__':

    language = 'en'
    model_path = '~/stanfordnlp_resources/{0}_ewt_models/{0}_ewt_tokenizer.pt'.format(language)

    if not file_exists(model_path):
        # prompt user to DL the stanford models
        print('')
        print('CLTK message: The part of the CLTK that you are using depends upon the `stanfordnlp` library. What follows are several question prompts coming from `stanfordnlp`. Answer with defaults.')
        print('')
        stanfordnlp.download(language)
        # if file model still not available after attempted DL, then raise error
        if not file_exists(model_path):
            raise FileNotFoundError('Missing required models for `stanfordnlp` at `{0}`.'.format(model_path))

    nlp = stanfordnlp.Pipeline()  # This sets up a default neural pipeline in English
    doc = nlp("Barack Obama was born in Hawaii.  He was elected president in 2008.")
    doc.sentences[0].print_dependencies()
    res = doc.sentences[0]
    print('dir:', dir(res))  # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_dependencies', '_process_tokens', '_tokens', '_words', 'build_dependencies', 'dependencies', 'print_dependencies', 'print_tokens', 'print_words', 'tokens', 'words']
    print('type:', type(res))  # <class 'stanfordnlp.pipeline.doc.Sentence'>
    print('res:', res)  # <stanfordnlp.pipeline.doc.Sentence object at 0x1cf484ef0>
    print('words:', res.words)  # [<Word index=1;text=Barack;lemma=Barack;upos=PROPN;xpos=NNP;feats=Number=Sing;governor=4;dependency_relation=nsubj:pass>, <Word index=2;text=Obama;lemma=Obama;upos=PROPN;xpos=NNP;feats=Number=Sing;governor=1;dependency_relation=flat>, <Word index=3;text=was;lemma=be;upos=AUX;xpos=VBD;feats=Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin;governor=4;dependency_relation=aux:pass>, <Word index=4;text=born;lemma=bear;upos=VERB;xpos=VBN;feats=Tense=Past|VerbForm=Part|Voice=Pass;governor=0;dependency_relation=root>, <Word index=5;text=in;lemma=in;upos=ADP;xpos=IN;feats=_;governor=6;dependency_relation=case>, <Word index=6;text=Hawaii;lemma=Hawaii;upos=PROPN;xpos=NNP;feats=Number=Sing;governor=4;dependency_relation=obl>, <Word index=7;text=.;lemma=.;upos=PUNCT;xpos=.;feats=_;governor=4;dependency_relation=punct>]
    print('tokens:', res.tokens)  # [<Token index=1;words=[<Word index=1;text=Barack;lemma=Barack;upos=PROPN;xpos=NNP;feats=Number=Sing;governor=4;dependency_relation=nsubj:pass>]>, <Token index=2;words=[<Word index=2;text=Obama;lemma=Obama;upos=PROPN;xpos=NNP;feats=Number=Sing;governor=1;dependency_relation=flat>]>, <Token index=3;words=[<Word index=3;text=was;lemma=be;upos=AUX;xpos=VBD;feats=Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin;governor=4;dependency_relation=aux:pass>]>, <Token index=4;words=[<Word index=4;text=born;lemma=bear;upos=VERB;xpos=VBN;feats=Tense=Past|VerbForm=Part|Voice=Pass;governor=0;dependency_relation=root>]>, <Token index=5;words=[<Word index=5;text=in;lemma=in;upos=ADP;xpos=IN;feats=_;governor=6;dependency_relation=case>]>, <Token index=6;words=[<Word index=6;text=Hawaii;lemma=Hawaii;upos=PROPN;xpos=NNP;feats=Number=Sing;governor=4;dependency_relation=obl>]>, <Token index=7;words=[<Word index=7;text=.;lemma=.;upos=PUNCT;xpos=.;feats=_;governor=4;dependency_relation=punct>]>]
    print('dependencies:', res.dependencies)  # [(<Word index=4;text=born;lemma=bear;upos=VERB;xpos=VBN;feats=Tense=Past|VerbForm=Part|Voice=Pass;governor=0;dependency_relation=root>, 'nsubj:pass', <Word index=1;text=Barack;lemma=Barack;upos=PROPN;xpos=NNP;feats=Number=Sing;governor=4;dependency_relation=nsubj:pass>), (<Word index=1;text=Barack;lemma=Barack;upos=PROPN;xpos=NNP;feats=Number=Sing;governor=4;dependency_relation=nsubj:pass>, 'flat', <Word index=2;text=Obama;lemma=Obama;upos=PROPN;xpos=NNP;feats=Number=Sing;governor=1;dependency_relation=flat>), (<Word index=4;text=born;lemma=bear;upos=VERB;xpos=VBN;feats=Tense=Past|VerbForm=Part|Voice=Pass;governor=0;dependency_relation=root>, 'aux:pass', <Word index=3;text=was;lemma=be;upos=AUX;xpos=VBD;feats=Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin;governor=4;dependency_relation=aux:pass>), (<Word index=0;text=ROOT>, 'root', <Word index=4;text=born;lemma=bear;upos=VERB;xpos=VBN;feats=Tense=Past|VerbForm=Part|Voice=Pass;governor=0;dependency_relation=root>), (<Word index=6;text=Hawaii;lemma=Hawaii;upos=PROPN;xpos=NNP;feats=Number=Sing;governor=4;dependency_relation=obl>, 'case', <Word index=5;text=in;lemma=in;upos=ADP;xpos=IN;feats=_;governor=6;dependency_relation=case>), (<Word index=4;text=born;lemma=bear;upos=VERB;xpos=VBN;feats=Tense=Past|VerbForm=Part|Voice=Pass;governor=0;dependency_relation=root>, 'obl', <Word index=6;text=Hawaii;lemma=Hawaii;upos=PROPN;xpos=NNP;feats=Number=Sing;governor=4;dependency_relation=obl>), (<Word index=4;text=born;lemma=bear;upos=VERB;xpos=VBN;feats=Tense=Past|VerbForm=Part|Voice=Pass;governor=0;dependency_relation=root>, 'punct', <Word index=7;text=.;lemma=.;upos=PUNCT;xpos=.;feats=_;governor=4;dependency_relation=punct>)]
