"""Stem Latin words with an implementation of the Schinke Latin stemming algorithm (Schnike, 1995)."""

import re


class Stemmer(object):
    """Stem Latin words via Schnike Latin stemming algorithm"""

    def __init__(self):
        """Initializer for stemmer."""

    def stem(self, text):
        """Stem the ."""
        for (pattern, repl) in self.patterns:
            text = re.subn(pattern, repl, text)[0]
        return text

    def _check_endsin_que(self, word):
        """If word ends in -que, if word is not in pass list, strip -que""" 
        pass_list = ['atque', 
                    'quoque',
                    'neque', 
                    'itaque', 
                    'absque', 
                    'apsque', 
                    'abusque', 
                    'adaeque', 
                    'adusque', 
                    'denique',
                    'deque', 
                    'susque', 
                    'oblique', 
                    'peraeque', 
                    'plenisque', 
                    'quandoque', 
                    'quisque', 
                    'quaeque',
                    'cuiusque', 
                    'cuique', 
                    'quemque', 
                    'quamque', 
                    'quaque', 
                    'quique', 
                    'quorumque', 
                    'quarumque',
                    'quibusque', 
                    'quosque', 
                    'quasque', 
                    'quotusquisque', 
                    'quousque', 
                    'ubique', 
                    'undique', 
                    'usque',
                    'uterque', 
                    'utique', 
                    'utroque', 
                    'utribique', 
                    'torque', 
                    'coque', 
                    'concoque', 
                    'contorque',
                    'detorque', 
                    'decoque', 
                    'excoque', 
                    'extorque', 
                    'obtorque', 
                    'optorque', 
                    'retorque', 
                    'recoque',
                    'attorque', 
                    'incoque', 
                    'intorque', 
                    'praetorque']

        if word not in pass_list:
            word = re.sub(r'que$', '', word)

        return word