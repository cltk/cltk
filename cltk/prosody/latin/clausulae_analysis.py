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
            'cretic + trochee': prosody.count('¯˘¯¯x'),
            '4th paeon + trochee': prosody.count('˘˘˘¯¯x'),
            '1st paeon + trochee': prosody.count('¯˘˘˘¯x'),
            'substituted cretic + trochee': prosody.count('˘˘˘˘˘¯x'),
            '1st paeon + anapest': prosody.count('¯˘˘˘˘˘x'),
            'double cretic': prosody.count('¯˘¯¯˘x'),
            '4th paeon + cretic': prosody.count('˘˘˘¯¯˘x'),
            'molossus + cretic': prosody.count('¯¯¯¯˘x'),
            'double trochee': prosody.count('¯˘¯x'),
            'molossus + double trochee': prosody.count('¯¯¯¯˘¯x'),
            'cretic + double trochee': prosody.count('¯˘¯¯˘¯x'),
            'dactyl + double trochee': prosody.count('¯˘˘¯˘¯x'),
            'choriamb + double trochee': prosody.count('¯˘˘¯¯˘¯x'),
            'cretic + iamb': prosody.count('¯˘¯˘x'),
            'molossus + iamb': prosody.count('¯¯¯˘x'),
            'double spondee': prosody.count('¯¯¯x'),
            'cretic + double spondee': prosody.count('¯˘¯¯¯¯x'),
            'heroic': prosody.count('¯˘˘¯x')
        }
