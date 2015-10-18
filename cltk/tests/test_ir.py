"""Test cltk.ir.

TODO: Test Greek version of some of these.
"""

import unittest

from cltk.ir.query import _highlight_match
from cltk.ir.query import _regex_span
from cltk.ir.query import _paragraph_context
from cltk.ir.query import _sentence_context
from cltk.ir.query import match_regex

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_regex_span(self):
        """Test _regex_span()."""
        text = 'ὅτι μὲν ὑμεῖς, ὦ ἄνδρες Ἀθηναῖοι, πεπόνθατε ὑπὸ τῶν ἐμῶν κατηγόρων, οὐκ οἶδα:'
        _matches = _regex_span(r'ς', text)
        matches_list = []
        for match in _matches:
            matches_list.append(match.span())
        self.assertEqual(matches_list, [(12, 13), (22, 23)])

    def test_sentence_context(self):
        """Test _sentence_context()."""
        sentence = None
        paragraph = """Ita fac, mi Lucili; vindica te tibi, et tempus, quod adhuc aut auferebatur aut subripiebatur aut excidebat, collige et serva. Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt. Turpissima tamen est iactura, quae per neglegentiam fit. Et si volueris attendere, maxima pars vitae elabitur male agentibus, magna nihil agentibus, tota vita aliud agentibus."""  # pylint: disable=line-too-long
        _matches = _regex_span(r'scribo', paragraph)
        for _match in _matches:
            sentence = _sentence_context(_match, language='latin')
        sentence_target = 'Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt.'  # pylint: disable=line-too-long
        self.assertEqual(sentence, sentence_target)

    def test_highlight_match(self):
        """Test _highlight_match()."""
        sentence = None
        paragraph = """Ita fac, mi Lucili; vindica te tibi, et tempus, quod adhuc aut auferebatur aut subripiebatur aut excidebat, collige et serva. Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt. Turpissima tamen est iactura, quae per neglegentiam fit. Et si volueris attendere, maxima pars vitae elabitur male agentibus, magna nihil agentibus, tota vita aliud agentibus."""  # pylint: disable=line-too-long
        _matches = _regex_span(r'scribo', paragraph)
        for _match in _matches:
            sentence = _highlight_match(_match, window=10)
        sentence_target = ' esse, ut *scribo*: quaedam '  # pylint: disable=line-too-long
        self.assertEqual(sentence, sentence_target)

    def test_paragraph_context(self):
        """Test _paragraph_context()."""
        text = """Ita fac, mi Lucili; vindica te tibi.

et tempus, quod adhuc aut auferebatur aut subripiebatur aut excidebat, collige et serva.

Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt.

Turpissima tamen est iactura, quae per neglegentiam fit.

Et si volueris attendere, maxima pars vitae elabitur male agentibus, magna nihil agentibus, tota vita aliud agentibus."""  # pylint: disable=line-too-long
        _matches = _regex_span(r'scribo', text)
        for _match in _matches:
            para = _paragraph_context(_match)
        target = 'Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt.'  # pylint: disable=line-too-long
        self.assertEqual(para, target)

    def test_match_regex_para(self):
        """Test match_regex()."""
        text = """Ita fac, mi Lucili; vindica te tibi.

et tempus, quod adhuc aut auferebatur aut subripiebatur aut excidebat, collige et serva.

Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt.

Turpissima tamen est iactura, quae per neglegentiam fit.

Et si volueris attendere, maxima pars vitae elabitur male agentibus, magna nihil agentibus, tota vita aliud agentibus.
"""
        _matches = match_regex(text, r'scribo', language='latin', context='paragraph')
        for _match in _matches:
            para = _match
        para_target = 'Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt.'  # pylint: disable=line-too-long
        self.assertEqual(para, para_target)

    def test_match_regex_sentence(self):
        """Test match_regex()."""
        text = """Ita fac, mi Lucili; vindica te tibi. et tempus, quod adhuc aut auferebatur aut subripiebatur aut excidebat, collige et serva. Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt. Turpissima tamen est iactura, quae per neglegentiam fit. Et si volueris attendere, maxima pars vitae elabitur male agentibus, magna nihil agentibus, tota vita aliud agentibus."""  # pylint: disable=line-too-long
        _matches = match_regex(text, r'scribo', language='latin', context='sentence')
        for _match in _matches:
            sent = _match
        sent_target = 'Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt.'  # pylint: disable=line-too-long
        self.assertEqual(sent, sent_target)

    def test_match_regex_window(self):
        """Test match_regex()."""
        text = """Ita fac, mi Lucili; vindica te tibi. et tempus, quod adhuc aut auferebatur aut subripiebatur aut excidebat, collige et serva. Persuade tibi hoc sic esse, ut scribo: quaedam tempora eripiuntur nobis, quaedam subducuntur, quaedam effluunt. Turpissima tamen est iactura, quae per neglegentiam fit. Et si volueris attendere, maxima pars vitae elabitur male agentibus, magna nihil agentibus, tota vita aliud agentibus."""  # pylint: disable=line-too-long
        _matches = match_regex(text, r'scribo', language='latin', context=50)
        for _match in _matches:
            sent = _match
        sent_target = ' collige et serva. Persuade tibi hoc sic esse, ut *scribo*: quaedam tempora eripiuntur nobis, quaedam subduc'  # pylint: disable=line-too-long
        self.assertEqual(sent, sent_target)

if __name__ == '__main__':
    unittest.main()
