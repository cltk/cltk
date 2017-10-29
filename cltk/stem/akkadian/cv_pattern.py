"""
Return a CV patterned string based on the word.
"""

__author__ = ['M. Willis Monroe <willismonroe@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

from cltk.stem.akkadian.syllabifier import AKKADIAN


class CVPattern(object):
    """Return a patterned string representing the consonants
     and vowels of the input word."""

    def __init__(self):
        self.akkadian = AKKADIAN

    def get_cv_pattern(self, word, pprint=False):
        """
        input = iparras
        pattern = [('V', 1, 'i'), ('C', 1, 'p'), ('V', 2, 'a'), ('C', 2, 'r'),
                  ('C', 2, 'r'), ('V', 2, 'a'), ('C', 3, 's')]
        pprint = V₁C₁V₂C₂C₂V₂C₃
        """
        subscripts = {
            1: '₁',
            2: '₂',
            3: '₃',
            4: '₄',
            5: '₅',
            6: '₆',
            7: '₇',
            8: '₈',
            9: '₉',
            0: '₀'
        }
        pattern = []
        c_count = 1
        v_count = 1
        count = 0
        for char in word:
            if char in self.akkadian['consonants']:
                cv = 'C'
            else:
                cv = 'V'
                # remove length:
                if char in self.akkadian['macron_vowels']:
                    char = self.akkadian['short_vowels'][self.akkadian['macron_vowels'].index(char)]
                elif char in self.akkadian['circumflex_vowels']:
                    char = self.akkadian['short_vowels'][self.akkadian['circumflex_vowels'].index(char)]
            if char not in [x[2] for x in pattern]:
                if cv == 'C':
                    count = c_count
                    c_count += 1
                elif cv == 'V':
                    count = v_count
                    v_count += 1
                pattern.append((cv, count, char))
            elif char in [x[2] for x in pattern]:
                pattern.append((cv, next(x[1] for x in pattern if x[2] == char), char))
        if pprint:
            output = ''
            for item in pattern:
                output += (item[0] + subscripts[item[1]])
            return output
        return pattern
