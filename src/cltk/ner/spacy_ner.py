"""Module for all NER relying on spaCy."""

from typing import List, Union

import spacy
from spacy.tokens import Doc, Token
from spacy.util import DummyTokenizer

from cltk.core.exceptions import CLTKException


class CustomTokenizer(DummyTokenizer):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, words):
        return Doc(self.vocab, words=words)


def spacy_tag_ner(text_tokens: List[str], model_path: str) -> List[Union[str, bool]]:
    """Take a list of tokens and return label or None.

    >>> text_tokens = ["Gallia", "est", "omnis", "divisa", "in", "partes", "tres", ",", "quarum", "unam", "incolunt", "Belgae", ",", "aliam", "Aquitani", ",", "tertiam", "qui", "ipsorum", "lingua", "Celtae", ",", "nostra", "Galli", "appellantur", "."]
    >>> from cltk.utils import CLTK_DATA_DIR
    >>> spacy_tag_ner(text_tokens=text_tokens, model_path=os.path.join(CLTK_DATA_DIR, "/lat/model/lat_models_cltk/ner/spacy_model/"))
    ['LOCATION', False, False, False, False, False, False, False, False, False, False, 'LOCATION', False, False, 'LOCATION', False, False, False, False, False, 'LOCATION', False, False, 'LOCATION', False, False]
    """
    # make sure that we have a List[str]
    if not isinstance(text_tokens[0], str):
        raise CLTKException("`spacy_tag_ner()` requires `List[str]`.")
    spacy_nlp = spacy.load(model_path)
    # Create the tokenizer for the spacy model
    spacy_nlp.tokenizer = CustomTokenizer(vocab=spacy_nlp.vocab)
    # Create the spacy Doc Object that contains the metadata for entities
    spacy_doc = spacy_nlp(text_tokens)  # type: Doc
    # generate the final output
    token_labels = list()  # type: List[Union[str, bool]]
    for word in spacy_doc:
        if word.ent_type_:
            # word.ent_type_  # type: str
            token_labels.append(word.ent_type_)
        else:
            token_labels.append(False)
    return token_labels


if __name__ == "__main__":
    SENTENCES_TOKENS = [
        [
            "Gallia",
            "est",
            "omnis",
            "divisa",
            "in",
            "partes",
            "tres",
            ",",
            "quarum",
            "unam",
            "incolunt",
            "Belgae",
            ",",
            "aliam",
            "Aquitani",
            ",",
            "tertiam",
            "qui",
            "ipsorum",
            "lingua",
            "Celtae",
            ",",
            "nostra",
            "Galli",
            "appellantur",
            ".",
        ],
        [
            "Etsi",
            "vereor",
            ",",
            "iudices",
            ",",
            "ne",
            "turpe",
            "sit",
            "pro",
            "fortissimo",
            "viro",
            "dicere",
            "incipientem",
            "timere",
            ",",
            "minimeque",
            "deceat",
            ",",
            "cum",
            "T.",
            "Annius",
            "ipse",
            "magis",
            "de",
            "rei",
            "publicae",
            "salute",
            "quam",
            "de",
            "sua",
            "perturbetur",
            ",",
            "me",
            "ad",
            "eius",
            "causam",
            "parem",
            "animi",
            "magnitudinem",
            "adferre",
            "non",
            "posse",
            ",",
            "tamen",
            "haec",
            "novi",
            "iudici",
            "nova",
            "forma",
            "terret",
            "oculos",
            ",",
            "qui",
            ",",
            "quocumque",
            "inciderunt",
            ",",
            "consuetudinem",
            "fori",
            "et",
            "pristinum",
            "morem",
            "iudiciorum",
            "requirunt",
            ".",
        ],
    ]
    for sentence_tokens in SENTENCES_TOKENS:
        ner_labels = cltk_ner(sentence_tokens)  # type: List[Union[None, str]]
        # print(ner_labels)
        print(list(zip(sentence_tokens, ner_labels)))
