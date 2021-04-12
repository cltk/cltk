"""Unit tests for ``cltk.dependency``."""

import unittest

from cltk import NLP
from cltk.dependency.tree import Dependency, DependencyTree, Form
from cltk.languages.example_texts import get_example_text


class TestDependency(unittest.TestCase):
    """Unit tests for dependency module.

    ..todo::
       - Add check for ``CLTKException`` if explicit model dl refused
    """

    def test_dependency_tree(self):
        cltk_nlp = NLP(language="lat")
        doc = cltk_nlp.analyze(text=get_example_text("lat"))
        one_word = doc.words[0]
        one_word.embedding = list()
        f = Form.to_form(word=one_word)
        form_str = f.full_str()
        target = "Gallia_0 [lemma=mallis,pos=noun,upos=NOUN,xpos=A1|grn1|casA|gen2,Case=nominative,Degree=positive,Gender=feminine,Number=singular]"
        self.assertEqual(form_str, target)

        t = DependencyTree.to_tree(doc.sentences[0])
        self.assertEqual(len(t.get_dependencies()), 28)

        t = DependencyTree.to_tree(doc.words[:25])
        self.assertIsInstance(t.findall("."), list)
        self.assertIsInstance(t.findall(".")[0], Form)


if __name__ == "__main__":
    unittest.main()
