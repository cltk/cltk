from cltk.stem.french import stem
import os
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def french_stemmer_test(self):
        sentence = "ja departissent a itant quant par la vile vint errant tut a cheval " \
                   "une pucele en tut le siecle n’ot si bele un blanc palefrei chevalchot"
        stemmed_text = stem(sentence)
        target = "j depart a it quant par la vil v err tut a cheval un pucel en tut le siecl n' o si bel un blanc palefre" \
                 " chevalcho "
        self.assertEqual(stemmed_text, target)

if __name__ == '__main__':
    unittest.main()