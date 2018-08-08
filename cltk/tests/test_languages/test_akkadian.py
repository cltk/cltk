'''
An experiment to use Huehnergard's grammar and key to test the functions in the cltk.
'''

__author__ = ['M. Willis Monroe <willismonroe@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

from cltk.phonology.akkadian.stress import StressFinder

import os
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_lesson_1_exercise_d(self):
        nouns = ['abum', 'ālum', 'amtum', 'bēlum', 'ḫurāṣum', 'iltum', 'ilum', 'kaspum', 'mārtum', 'mārum', 'qaqqadum',
                 'ṣābum', 'šarratum', 'šarrum', 'wardum']
        stresser = StressFinder()
        stress = []
        for noun in nouns:
            stress.append(stresser.find_stress(noun))
        target = [['[a]', 'bum'], ['[ā]', 'lum'], ['[am]', 'tum'], ['[bē]', 'lum'], ['ḫu', '[rā]', 'ṣum'],
                  ['[il]', 'tum'], ['[i]', 'lum'], ['[kas]', 'pum'], ['[mār]', 'tum'], ['[mā]', 'rum'],
                  ['[qaq]', 'qa', 'dum'], ['[ṣā]', 'bum'], ['[šar]', 'ra', 'tum'], ['[šar]', 'rum'], ['[war]', 'dum']]

        self.assertEqual(stress, target)

    def test_lesson_1_exercise_e(self):
        nouns = ['mušallimum', 'išāl', 'idin', 'iddinūniššum', 'tabnianni', 'niqīaš', 'epēšum', 'kullumum', 'tabnû',
                 'iššiakkum', 'rēdûm', 'iqbi', 'paris', 'išmeānim', 'pete', 'šūṣû']
        stresser = StressFinder()
        stress = []
        for noun in nouns:
            stress.append(stresser.find_stress(noun))
        target = [['mu', '[šal]', 'li', 'mum'], ['i', '[šāl]'], ['[i]', 'din'], ['id', 'di', 'nū', '[niš]', 'šum'],
                  ['tab', 'ni', '[an]', 'ni'], ['ni', '[qī]', 'aš'], ['e', '[pē]', 'šum'], ['[kul]', 'lu', 'mum'],
                  ['tab', '[nû]'], ['iš', 'ši', '[ak]', 'kum'], ['rē', '[dûm]'], ['[iq]', 'bi'], ['[pa]', 'ris'],
                  ['iš', 'me', '[ā]', 'nim'], ['[pe]', 'te'], ['šū', '[ṣû]']]

        self.assertEqual(stress, target)

    def test_lesson_2_exercise_b(self):
        nouns = ['aššatum', 'bītum', 'emūqum', 'īnum', 'išdum', 'libbum', 'mutum', 'nārum', 'šīpātum', 'ṭuppum',
                 'ummum', 'uznum']
        stresser = StressFinder()
        stress = []
        for noun in nouns:
            stress.append(stresser.find_stress(noun))
        target = [['[aš]', 'ša', 'tum'], ['[bī]', 'tum'], ['e', '[mū]', 'qum'], ['[ī]', 'num'], ['[iš]', 'dum'],
                  ['[lib]', 'bum'], ['[mu]', 'tum'], ['[nā]', 'rum'], ['šī', '[pā]', 'tum'], ['[ṭup]', 'pum'],
                  ['[um]', 'mum'], ['[uz]', 'num']]

        self.assertEqual(stress, target)


if __name__ == '__main__':
    unittest.main()
