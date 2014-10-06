# encoding: utf-8
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import re


diogenes = '/Applications/Diogenes.app/Contents/Resources/perl/Diogenes/unicode-equivs.pl'
with open(diogenes, 'r') as f:
    d = f.read()
    py_uni = re.sub(r'"\\x{(.{4})}"', r'\t"\\u\1"', d)
    py_dct = re.sub(r"\s=>\s", ": ", py_uni)
    py_dct = re.sub(r"%Diogenes::UnicodeInput::(unicode_equivs)\s=\s\(",
                    r"\1 = {", py_dct)
    py_dct = re.sub(r'\);', "}", py_dct)
    py_dct = re.sub(r'%Diogenes::UnicodeInput::(upper_to_lower)\s=\s\(',
                    r"\1 = {", py_dct)
print(py_dct)
