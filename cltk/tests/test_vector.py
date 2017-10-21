import unittest
from cltk.vector.word2vec import get_sims

class TestWord2Vec(unittest.TestCase):
    '''
        This class is to be used for testing
        TODO: Add unittests for all functions
    '''
    def test_get_sims(self):
        '''
            TODO: Write unittests for all conditions
        '''
        l = get_sims('iubeo', 'latin')
        a = ['uideo', 'gaudeo', 'nolo', 'uolo']
        self.assertEqual(l, a)

if __name__ == '__main__':
    unittest.main()
