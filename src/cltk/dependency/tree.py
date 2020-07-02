"""A data structure for representing dependency tree graphs."""

__author__ = ["John Stewart <free-variation>"]

from typing import Dict, List, Union
from xml.etree.ElementTree import Element, ElementTree

from cltk.core.data_types import Doc, Process, Word


class Form(Element):
    """For the word (ie, node) of a dependency tree and its attributes. Inherits
    from the ``Element`` class of Python's ``xml.etree`` library.

    >>> desc_form = Form('described')
    >>> desc_form
    described_0
    >>> desc_form.set('Tense', 'Past')
    >>> desc_form
    described_0
    >>> desc_form / 'VBN'
    described_0/VBN
    >>> desc_form.full_str()
    'described_0 [Tense=Past,pos=VBN]'
    """

    def __init__(self, form: str, form_id: int = 0) -> None:
        """Constructor for the Form class."""
        Element.__init__(self, form, attrib={"form_id": str(form_id)})

    def __truediv__(self, pos_tag: str) -> "Form":
        """Assigns the POS feature for current form. This is
        done by overloading ``operator.truediv()`` (``a / b``) to
        perform ``.set()`` upon and ``Element`` of the xml library.

        >>> desc_form = Form('described')
        >>> desc_form / 'VBN'
        described_0/VBN
        >>> import operator
        >>> desc_form = Form('described')
        >>> operator.truediv(desc_form, 'VBN')
        described_0/VBN
        """
        self.set("pos", pos_tag)
        return self

    def __rshift__(self, other: Union["Form", str]) -> "Dependency":
        """Create a dependency between this form as governor, to
        the other as dependent. Adds the dependent to the children
        of this form. This is done by overloading ``operator.rshift()``
        (``a >> b``) to perform ``.append()`` upon ``Element`` of the xml
        library. Returns ``Dependency`` xxx

        >>> john = Form('John', 1) / 'NNP'
        >>> john
        John_1/NNP
        >>> loves = Form('loves', 2) / 'VRB'
        >>> loves
        loves_2/VRB
        >>> mary = Form('Mary', 3) / 'NNP'
        >>> mary
        Mary_3/NNP
        """
        other = Form(other) if isinstance(other, str) else other
        self.append(other)
        return Dependency(self, other)

    def get_dependencies(self, relation: str) -> List["Dependency"]:
        """Extract dependents of this form for the specified
        dependency relation.

        >>> john = Form('John', 1) / 'NNP'
        >>> loves = Form('loves', 2) / 'VRB'
        >>> mary = Form('Mary', 3) / 'NNP'
        >>> loves >> john | 'subj'
        subj(loves_2/VRB, John_1/NNP)
        >>> loves >> mary | 'obj'
        obj(loves_2/VRB, Mary_3/NNP)
        >>> loves.get_dependencies('subj')
        [subj(loves_2/VRB, John_1/NNP)]
        >>> loves.get_dependencies('obj')
        [obj(loves_2/VRB, Mary_3/NNP)]
        """
        deps = self.findall('*[@relation="{}"]'.format(relation))
        return [Dependency(self, dep, relation) for dep in deps]

    def __str__(self) -> str:
        return (
            self.tag
            + "_"
            + self("form_id")
            + (("/" + self("pos")) if self("pos") else "")
        )

    __repr__ = __str__

    def full_str(self, include_relation=True) -> str:
        """Returns a string containing all features of the Form.
        The ID is attached to the text, and the relation is
        optionally suppressed.

        >>> loves = Form('loves', 2) / 'VRB'
        >>> loves.full_str()
        'loves_2 [pos=VRB]'
        >>> john = Form('John', 1) / 'NNP'
        >>> loves >> john | 'subj'
        subj(loves_2/VRB, John_1/NNP)
        >>> john.full_str(True)
        'John_1 [pos=NNP,relation=subj]'

        """
        excluded = ["form_id", "relation"] if not include_relation else ["form_id"]
        return "{0}_{1} [{2}]".format(
            self.tag,
            self("form_id"),
            ",".join(
                [
                    feature + "=" + self(feature)
                    for feature in self.attrib.keys()
                    if feature not in excluded
                ]
            ),
        )

    def __call__(self, feature: str) -> str:
        return self.get(feature)

    @staticmethod
    def to_form(word: Word) -> "Form":
        """Converts a ``CLTK`` ``Word`` object to a ``Form``.

        >>> cltk_word = Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='Gallia', pos='NOUN', lemma='mallis', scansion=None, xpos='A1|grn1|casA|gen2', upos='NOUN', dependency_relation='nsubj', governor=3, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, embedding=[], stop=False, named_entity=True)
        >>> f = Form.to_form(cltk_word)
        >>> f.full_str()
        'Gallia_0 [lemma=mallis,pos=NOUN,upos=NOUN,xpos=A1|grn1|casA|gen2,Case=Nom,Degree=Pos,Gender=Fem,Number=Sing]'
        """

        form = Form(word.string, form_id=word.index_token)
        form.set("lemma", word.lemma)
        form.set("pos", word.pos)
        form.set("upos", word.upos)
        form.set("xpos", word.xpos)

        for (feature_name, feature_value) in word.features.items():
            form.set(feature_name, feature_value)

        return form


class Dependency:
    """The asymmetric binary relationship (or edge) between a governing
    Form (the "head") and a subordinate Form (the "dependent").

    In principle the relationship could capture any form-to-form relation
    that the systems deems of interest, be it syntactic, semantic, or discursive.

    If the `relation` attribute is not speficied, then the dependency simply states
    that there's some asymmetric relationship between the head and the dependenent.
    This is an *untyped* dependency.

    For a *typed* dependency, a string value is supplied for the `relation` attribute.
    """

    def __init__(self, head: Form, dep: Form, relation: str = None) -> None:
        self.head = head
        self.dep = dep
        self.relation = relation

    def __str__(self) -> str:
        return "{0}({1}, {2})".format(
            self.relation if self.relation else "", self.head, self.dep
        )

    __repr__ = __str__

    def __or__(self, relation: str) -> "Dependency":
        self.relation = relation
        self.dep.set("relation", relation)
        return self


class DependencyTree(ElementTree):
    """The hierarchical tree representing the entirety of a parse."""

    def __init__(self, root: Form) -> None:
        root.set("relation", "root")

        ElementTree.__init__(self, root)

    def get_dependencies(self) -> List[Dependency]:
        """Returns a list of all the dependency relations in the tree,
        generated by depth-first search.

        >>> a_sentence = [Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='Gallia', pos='NOUN', lemma='mallis', scansion=None, xpos='A1|grn1|casA|gen2', upos='NOUN', dependency_relation='nsubj', governor=3, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, embedding=[], stop=False, named_entity=True), Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='est', pos='AUX', lemma='sum', scansion=None, xpos='N3|modA|tem1|gen6', upos='AUX', dependency_relation='cop', governor=3, features={'Mood': 'Ind', 'Number': 'Sing', 'Person': '3', 'Tense': 'Pres', 'VerbForm': 'Fin', 'Voice': 'Act'}, embedding=[], stop=True, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=2, index_sentence=0, string='omnis', pos='PRON', lemma='omnis', scansion=None, xpos='C1|grn1|casA|gen2', upos='PRON', dependency_relation='det', governor=0, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing', 'PronType': 'Ind'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=3, index_sentence=0, string='divisa', pos='VERB', lemma='divido', scansion=None, xpos='L2|modM|tem4|grp1|casA|gen2', upos='VERB', dependency_relation='root', governor=-1, features={'Aspect': 'Perf', 'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing', 'Tense': 'Past', 'VerbForm': 'Part', 'Voice': 'Pass'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=4, index_sentence=0, string='in', pos='ADP', lemma='in', scansion=None, xpos='S4', upos='ADP', dependency_relation='case', governor=5, features={'AdpType': 'Prep'}, embedding=[], stop=True, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=5, index_sentence=0, string='partes', pos='NOUN', lemma='pars', scansion=None, xpos='C1|grn1|casM|gen2', upos='NOUN', dependency_relation='obl:arg', governor=3, features={'Case': 'Acc', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Plur'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=6, index_sentence=0, string='tres', pos='NUM', lemma='tres', scansion=None, xpos='C1|grn1|casM|gen2|vgr1', upos='NUM', dependency_relation='nummod', governor=5, features={'Case': 'Acc', 'Degree': 'Pos', 'Gender': 'Fem', 'NumType': 'Card', 'Number': 'Plur'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=7, index_sentence=0, string=',', pos='PUNCT', lemma=',', scansion=None, xpos='Punc', upos='PUNCT', dependency_relation='punct', governor=10, features={}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=8, index_sentence=0, string='quarum', pos='PRON', lemma='qui', scansion=None, xpos='F1|grn1|casK|gen2', upos='PRON', dependency_relation='nmod', governor=9, features={'Case': 'Gen', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Plur', 'PronType': 'Rel'}, embedding=[], stop=True, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=9, index_sentence=0, string='unam', pos='NUM', lemma='unus', scansion=None, xpos='F1|grn1|casD|gen2', upos='NUM', dependency_relation='obj', governor=10, features={'Case': 'Acc', 'Degree': 'Pos', 'Gender': 'Fem', 'NumType': 'Card', 'Number': 'Sing'}, embedding=[], stop=True, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=10, index_sentence=0, string='incolunt', pos='VERB', lemma='incolo', scansion=None, xpos='L3|modA|tem1|gen9', upos='VERB', dependency_relation='acl:relcl', governor=5, features={'Mood': 'Ind', 'Number': 'Plur', 'Person': '3', 'Tense': 'Pres', 'VerbForm': 'Fin', 'Voice': 'Act'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=11, index_sentence=0, string='Belgae', pos='NOUN', lemma='melgus', scansion=None, xpos='A1|grn1|casJ|gen2|vgr1', upos='NOUN', dependency_relation='nsubj', governor=10, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Plur'}, embedding=[], stop=False, named_entity=True), Word(index_char_start=None, index_char_stop=None, index_token=12, index_sentence=0, string=',', pos='PUNCT', lemma=',', scansion=None, xpos='Punc', upos='PUNCT', dependency_relation='punct', governor=14, features={}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=13, index_sentence=0, string='aliam', pos='PRON', lemma='alius', scansion=None, xpos='F1|grn1|casD|gen2', upos='PRON', dependency_relation='obj', governor=24, features={'Case': 'Acc', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing', 'PronType': 'Ind'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=14, index_sentence=0, string='Aquitani', pos='NOUN', lemma='mquitanus', scansion=None, xpos='B1|grn1|casJ|gen1', upos='NOUN', dependency_relation='nmod', governor=11, features={'Case': 'Gen', 'Degree': 'Pos', 'Gender': 'Masc', 'Number': 'Sing'}, embedding=[], stop=False, named_entity=True), Word(index_char_start=None, index_char_stop=None, index_token=15, index_sentence=0, string=',', pos='PUNCT', lemma=',', scansion=None, xpos='Punc', upos='PUNCT', dependency_relation='punct', governor=24, features={}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=16, index_sentence=0, string='tertiam', pos='ADJ', lemma='tertius', scansion=None, xpos='A1|grn1|casD|gen2', upos='ADJ', dependency_relation='amod', governor=13, features={'Case': 'Acc', 'Degree': 'Pos', 'Gender': 'Fem', 'NumType': 'Ord', 'Number': 'Sing'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=17, index_sentence=0, string='qui', pos='PRON', lemma='qui', scansion=None, xpos='F1|grn1|casJ|gen1', upos='PRON', dependency_relation='nsubj', governor=20, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Masc', 'Number': 'Plur', 'PronType': 'Rel'}, embedding=[], stop=True, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=18, index_sentence=0, string='ipsorum', pos='PRON', lemma='ipse', scansion=None, xpos='F1|grn1|casK|gen1', upos='PRON', dependency_relation='nmod', governor=19, features={'Case': 'Gen', 'Degree': 'Pos', 'Gender': 'Masc', 'Number': 'Plur', 'PronType': 'Dem,Prs'}, embedding=[], stop=True, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=19, index_sentence=0, string='lingua', pos='NOUN', lemma='lingua', scansion=None, xpos='A1|grn1|casF|gen2', upos='NOUN', dependency_relation='obl', governor=20, features={'Case': 'Abl', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=20, index_sentence=0, string='Celtae', pos='ADJ', lemma='meltus', scansion=None, xpos='A1|grn1|casJ|gen2', upos='ADJ', dependency_relation='acl:relcl', governor=14, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Plur'}, embedding=[], stop=False, named_entity=True), Word(index_char_start=None, index_char_stop=None, index_token=21, index_sentence=0, string=',', pos='PUNCT', lemma=',', scansion=None, xpos='Punc', upos='PUNCT', dependency_relation='punct', governor=20, features={}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=22, index_sentence=0, string='nostra', pos='ADJ', lemma='noster', scansion=None, xpos='A1|grn1|casM|gen2', upos='ADJ', dependency_relation='amod', governor=23, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Neut', 'Number': 'Plur', 'Poss': 'Yes'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=23, index_sentence=0, string='Galli', pos='ADJ', lemma='mallus', scansion=None, xpos='B1|grn1|casJ|gen1', upos='ADJ', dependency_relation='xcomp', governor=24, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Masc', 'Number': 'Plur'}, embedding=[], stop=False, named_entity=True), Word(index_char_start=None, index_char_stop=None, index_token=24, index_sentence=0, string='appellantur', pos='VERB', lemma='appello', scansion=None, xpos='J3|modJ|tem1|gen9', upos='VERB', dependency_relation='acl:relcl', governor=5, features={'Mood': 'Ind', 'Number': 'Plur', 'Person': '3', 'Tense': 'Pres', 'VerbForm': 'Fin', 'Voice': 'Pass'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=25, index_sentence=0, string='.', pos='PUNCT', lemma='.', scansion=None, xpos='Punc', upos='PUNCT', dependency_relation='punct', governor=3, features={}, embedding=[], stop=False, named_entity=False)]
        >>> t = DependencyTree.to_tree(a_sentence)
        >>> len(t.get_dependencies())
        28
        """

        def _get_deps(node: Form, deps: List[Dependency]) -> List[Dependency]:
            for child_node in list(node):
                deps = _get_deps(child_node, deps)
                deps.extend(node.get_dependencies(child_node("relation")))
            return deps

        deps = _get_deps(self.getroot(), [])
        deps.append(Dependency(None, self.getroot(), "root"))
        return deps

    def print_tree(self, all_features: bool = True):
        """Prints a pretty-printed (indented) representation
        of the dependency tree. If all_features is True, then
        each node is printed with its complete feature bundles.
        """

        def _print_treelet(node: Form, indent: int, all_features: bool):
            edge = "└─ " if indent > 0 else ""
            node_str = node.full_str(False) if all_features else str(node)
            print(" " * indent + edge + node("relation") + " | " + node_str)

            for child_node in list(node):
                _print_treelet(child_node, indent + 4, all_features)

        # self._print_treelet(self.getroot(), indent=0, all_features=all_features)

    @staticmethod
    def to_tree(sentence: List[Word]) -> "DependencyTree":
        """Factory method to create trees from sentences parses, i.e. lists of words.

        >>> from cltk.core.data_types import Word
        >>> a_sentence = [Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='Gallia', pos='NOUN', lemma='mallis', scansion=None, xpos='A1|grn1|casA|gen2', upos='NOUN', dependency_relation='nsubj', governor=3, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, embedding=[], stop=False, named_entity=True), Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='est', pos='AUX', lemma='sum', scansion=None, xpos='N3|modA|tem1|gen6', upos='AUX', dependency_relation='cop', governor=3, features={'Mood': 'Ind', 'Number': 'Sing', 'Person': '3', 'Tense': 'Pres', 'VerbForm': 'Fin', 'Voice': 'Act'}, embedding=[], stop=True, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=2, index_sentence=0, string='omnis', pos='PRON', lemma='omnis', scansion=None, xpos='C1|grn1|casA|gen2', upos='PRON', dependency_relation='det', governor=0, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing', 'PronType': 'Ind'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=3, index_sentence=0, string='divisa', pos='VERB', lemma='divido', scansion=None, xpos='L2|modM|tem4|grp1|casA|gen2', upos='VERB', dependency_relation='root', governor=-1, features={'Aspect': 'Perf', 'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing', 'Tense': 'Past', 'VerbForm': 'Part', 'Voice': 'Pass'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=4, index_sentence=0, string='in', pos='ADP', lemma='in', scansion=None, xpos='S4', upos='ADP', dependency_relation='case', governor=5, features={'AdpType': 'Prep'}, embedding=[], stop=True, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=5, index_sentence=0, string='partes', pos='NOUN', lemma='pars', scansion=None, xpos='C1|grn1|casM|gen2', upos='NOUN', dependency_relation='obl:arg', governor=3, features={'Case': 'Acc', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Plur'}, embedding=[], stop=False, named_entity=False), Word(index_char_start=None, index_char_stop=None, index_token=6, index_sentence=0, string='tres', pos='NUM', lemma='tres', scansion=None, xpos='C1|grn1|casM|gen2|vgr1', upos='NUM', dependency_relation='nummod', governor=5, features={'Case': 'Acc', 'Degree': 'Pos', 'Gender': 'Fem', 'NumType': 'Card', 'Number': 'Plur'}, embedding=[], stop=False, named_entity=False)]
        >>> t = DependencyTree.to_tree(a_sentence)
        >>> t.findall(".")
        [divisa_3/VERB]
        """

        forms = {}  # type: Dict[int, Form]
        for word in sentence:
            forms[word.index_token] = Form.to_form(word)

        for word in sentence:
            if word.dependency_relation == "root":
                root = forms[word.index_token]
            else:
                gov = forms[word.governor]
                dep = forms[word.index_token]
                gov >> dep | word.dependency_relation

        return DependencyTree(root)
