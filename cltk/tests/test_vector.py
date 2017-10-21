<<<<<<< HEAD
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
=======
from cltk.vector.word2vec import get_sims
import unittest

class TestWord2Vec(unittest.TestCase):

    def test_get_sims(self):
>>>>>>> 4a363a1f6bf57ee7b5898a888a03105e31776e0f
        l = get_sims('iubeo', 'latin')
        a = ['uideo', 'gaudeo', 'nolo', 'uolo']
        self.assertEqual(l, a)

if __name__ == '__main__':
    unittest.main()
