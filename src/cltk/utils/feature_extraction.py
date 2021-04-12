"""Helper functions for extracting features from CLTK data structures,
especially for the purpose of preparing data for machine learning.
"""

from typing import List, Tuple, Union

from cltk.core.data_types import Doc
from cltk.core.exceptions import CLTKException
from cltk.dependency.utils import get_governor_relationship, get_governor_word
from cltk.morphology.utils import get_features, get_pos


def cltk_doc_to_features_table(
    cltk_doc: Doc,
) -> Tuple[List[str], List[List[Union[str, int, float, None]]]]:
    """Take a CLTK ``Doc`` and return a list of lists ready for
    machine learning.

    This expects the default features available for Greek and Latin
    (word embeddings, morphology, syntax, lemmata). This should be
    improved to fail gracefully when less features available in the
    input ``Doc``.

    TODO: Fail gracefully when missing info in ``Doc``.
    """

    if len(cltk_doc.sentences) < 1:
        raise CLTKException("Must contain at least one ``Doc.sentence``.")

    list_of_list_features = (
        list()
    )  # type: List[List[Union[str, int, float, None, np.ndarray]]]

    for sentence in cltk_doc.sentences:
        for word in sentence:
            word_features_list = (
                list()
            )  # type: List[Union[str, int, float, None, np.ndarray]]
            # note: this gets made and remade; only needs to be done once, at beginning or at end; need to add check that len == the actual instance row
            variable_names = list()  # type: List[str]
            # Get word token chars
            word_features_list.append(word.string)
            variable_names.append("string")
            # Get lemma
            word_features_list.append(word.lemma)
            variable_names.append("lemma")
            # Get embedding
            word_features_list.append(word.embedding)
            variable_names.append("embedding")
            # Get stopword binary
            word_features_list.append(word.stop)
            variable_names.append("is_stop")
            # Get NER binary
            word_features_list.append(word.named_entity)
            variable_names.append("lemma")

            # Get morphological info
            pos_label = get_pos(word=word)
            word_features_list.append(
                pos_label
            )  # note: incorrectly labels upper-cased words as proper_noun, eg 'Βίβλος'
            variable_names.append("pos")
            feature_names, features_present = get_features(word=word)
            word_features_list += (
                features_present  # add the features list to the big list
            )
            variable_names += feature_names

            # Get dependency info
            governing_word = get_governor_word(word=word, sentence=sentence)
            pos_label_governor = get_pos(word=governing_word)
            word_features_list.append(pos_label_governor)
            variable_names.append("governing_word")
            feature_names_governor, features_present_governor = get_features(
                word=governing_word, prepend_to_label="governor_"
            )
            word_features_list += (
                features_present_governor  # add the features list to the big list
            )
            variable_names += feature_names_governor
            # governor_edge = get_governor_relationship(word=word, sentence=sentence)
            # word_features_list.append(governor_edge)
            relation_type = word.dependency_relation
            word_features_list.append(relation_type)
            variable_names.append("governing_relationship")

            list_of_list_features.append(word_features_list)

    assert len(variable_names) == len(
        list_of_list_features[0]
    ), f"The names of variables ({len(variable_names)}) does not match then actual number of variables ({len(list_of_list_features[0])}). These must be equal."

    return variable_names, list_of_list_features
