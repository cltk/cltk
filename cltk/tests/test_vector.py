from cltk.vector.word2vec import get_sims
import unittest

class TestWord2Vec(unittest.TestCase):

    def test_get_sims(self):
        l = get_sims('iubeo', 'latin')
        a = ['uideo', 'gaudeo', 'nolo', 'uolo']
        self.assertEqual(l, a)

if __name__ == '__main__':
    unittest.main()
