"""
Return dictionary of clausulae found in the prosody of Latin prose.

The clausulae analysis function returns a dictionary in which the key is the type of clausula and the value is the number
of times it occurs in the text. The list of clausulae used in the method is derived from the 2019 Journal of Roman Studies
paper "Auceps syllabarum: A Digital Analysis of Latin Prose Rhythm". The list of clausulae are mutually exclusive so no one
rhythm will be counted in multiple categories.
"""
from collections import namedtuple
from typing import Dict, List

__author__ = ["Tyler Kirby <tyler.kirby9398@gmail.com>"]
__license__ = "MIT License. See LICENSE"

Clausula = namedtuple("Clausula", "rhythm_name rhythm")

standard_clausulae = [
    Clausula("cretic_trochee", "-u--x"),
    Clausula("cretic_trochee_resolved_a", "uuu--x"),
    Clausula("cretic_trochee_resolved_b", "-uuu-x"),
    Clausula("cretic_trochee_resolved_c", "-u-uux"),
    Clausula("double_cretic", "-u--ux"),
    Clausula("molossus_cretic", "----ux"),
    Clausula("double_molossus_cretic_resolved_a", "uuu--ux"),
    Clausula("double_molossus_cretic_resolved_b", "-uuu-ux"),
    Clausula("double_molossus_cretic_resolved_c", "-u-uux"),
    Clausula("double_molossus_cretic_resolved_d", "uu---ux"),
    Clausula("double_molossus_cretic_resolved_e", "-uu--ux"),
    Clausula("double_molossus_cretic_resolved_f", "--uu-ux"),
    Clausula("double_molossus_cretic_resolved_g", "---uuux"),
    Clausula("double_molossus_cretic_resolved_h", "-u---ux"),
    Clausula("double_trochee", "-u-x"),
    Clausula("double_trochee_resolved_a", "uuu-x"),
    Clausula("double_trochee_resolved_b", "-uuux"),
    Clausula("hypodochmiac", "-u-ux"),
    Clausula("hypodochmiac_resolved_a", "uuu-ux"),
    Clausula("hypodochmiac_resolved_b", "-uuuux"),
    Clausula("spondaic", "---x"),
    Clausula("heroic", "-uu-x"),
]


class Clausulae:
    def __init__(self, rhythms: List[Clausula] = standard_clausulae):
        """Initialize class."""
        self.rhythms = rhythms

    def clausulae_analysis(self, prosody: List) -> List[Dict[str, int]]:
        """
        Return dictionary in which the key is a type of clausula and the value is its frequency.
        :param prosody: the prosody of a prose text (must be in the format of the scansion produced by the scanner classes.
        :return: dictionary of prosody
        >>> Clausulae().clausulae_analysis(['-uuu-uuu-u--x', 'uu-uu-uu----x'])
        [{'cretic_trochee': 1}, {'cretic_trochee_resolved_a': 0}, {'cretic_trochee_resolved_b': 0}, {'cretic_trochee_resolved_c': 0}, {'double_cretic': 0}, {'molossus_cretic': 0}, {'double_molossus_cretic_resolved_a': 0}, {'double_molossus_cretic_resolved_b': 0}, {'double_molossus_cretic_resolved_c': 0}, {'double_molossus_cretic_resolved_d': 0}, {'double_molossus_cretic_resolved_e': 0}, {'double_molossus_cretic_resolved_f': 0}, {'double_molossus_cretic_resolved_g': 0}, {'double_molossus_cretic_resolved_h': 0}, {'double_trochee': 0}, {'double_trochee_resolved_a': 0}, {'double_trochee_resolved_b': 0}, {'hypodochmiac': 0}, {'hypodochmiac_resolved_a': 0}, {'hypodochmiac_resolved_b': 0}, {'spondaic': 1}, {'heroic': 0}]
        """
        prosody = " ".join(prosody)
        return [{r.rhythm_name: prosody.count(r.rhythm)} for r in self.rhythms]
