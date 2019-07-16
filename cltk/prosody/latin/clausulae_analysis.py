"""
Return dictionary of clausulae found in the prosody of Latin prose.

The clausulae analysis function returns a dictionary in which the key is the type of clausula and the value is the number
of times it occurs in the text. The list of clausulae used in the method is derived from the 'Prose Rhythm' section
of John Ramsey's Cambridge commentary on Cicero's Philippics I-II, so it is mostly representative of Ciceronian
clausulae. Because of the heavy Greek influence on Cicero's rhythms, however, the clausulae analysis may also be used
on the prosody of Greek prose as well.
"""

__author__ = ['Tyler Kirby <tyler.kirby9398@gmail.com>']
__license__ = 'MIT License. See LICENSE'


class Clausulae:
    def __init__(self):
        """Initialize class."""
        return

    @staticmethod
    def clausulae_analysis(prosody):
        """
        Return dictionary in which the key is a type of clausula and the value is its frequency.
        :param prosody: the prosody of a prose text (must be in the format of the scansion produced by the scanner classes.
        :return: dictionary of prosody
        """

        prosody = ''.join(prosody)

        return {
            'cretic trochee': prosody.count('-u--x'),
            'cretic trochee resolved a': prosody.count('uuu--x'),
            'cretic trochee resolved b': prosody.count('-uuu-x'),
            'cretic trochee resolbed c': prosody.count('-u-uux'),
            'double cretic': prosody.count('-u--ux'),
            'molossus cretic': prosody.count('----ux'),
            'double/molossus cretic resolved a': prosody.count('uuu--ux'),
            'double/molossus cretic resolved b': prosody.count('-uuu-ux'),
            'double/molossus cretic resolved c': prosody.count('-u-uuux'),
            'double/molossus cretic resolved d': prosody.count('uu---ux'),
            'double/molossus cretic resolved e': prosody.count('-uu--ux'),
            'double/molossus cretic resolved f': prosody.count('--uu-ux'),
            'double/molossus cretic resolved g': prosody.count('---uuux'),
            'double/molossus cretic resolved h': prosody.count('-u---ux'),
            'double trochee': prosody.count('-u-x'),
            'double trochee resolved a': prosody.count('uuu-x'),
            'double trochee resolved b': prosody.count('-uuux'),
            'hypodochmiac': prosody.count('-u-ux'),
            'hypodochmiac resolved a': prosody.count('uuu-ux'),
            'hypodochmiac resolved b': prosody.count('-uuuux'),
            'spondaic': prosody.count('---x'),
            'heroic': prosody.count('-uu-x')
        }
