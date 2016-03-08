"""
Return dictionary of clausulae found in the prosody of Latin prose.
"""

import re

__author__ = 'Tyler Kirby <tyler.kirby9398@gmail.com>'
__license__ = 'MIT License. See LICENSE'

class Clausulae:
    def __init__(self):
        """Initialize class."""
        return

    @staticmethod
    def clausulae_analysis(prosody):

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


if __name__ == "__main__":
    print(Clausulae().clausulae_analysis(['¯˘˘¯x']))