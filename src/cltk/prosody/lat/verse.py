"""Data structure class for a line of metrical verse."""

__author__ = ["Todd Cook <todd.g.cook@gmail.com>"]
__license__ = "MIT License"


class Verse:
    """
    Class representing a line of metrical verse.

    This class is round-trippable; the __repr__ call can be used for construction.

    >>> positional_hex = Verse(original='impulerit. Tantaene animis caelestibus irae?',
    ... scansion='-  U U -    -   -   U U -    - -  U U  -  - ', meter='hexameter',
    ... valid=True, syllable_count=15, accented='īmpulerīt. Tāntaene animīs caelēstibus īrae?',
    ... scansion_notes=['Valid by positional stresses.'],
    ... syllables = ['īm', 'pu', 'le', 'rīt', 'Tān', 'taen', 'a', 'ni', 'mīs', 'cae', 'lēs', 'ti', 'bus', 'i', 'rae'])
    >>> dupe = eval(positional_hex.__repr__())
    >>> dupe
    Verse(original='impulerit. Tantaene animis caelestibus irae?', scansion='-  U U -    -   -   U U -    - -  U U  -  - ', meter='hexameter', valid=True, syllable_count=15, accented='īmpulerīt. Tāntaene animīs caelēstibus īrae?', scansion_notes=['Valid by positional stresses.'], syllables = ['īm', 'pu', 'le', 'rīt', 'Tān', 'taen', 'a', 'ni', 'mīs', 'cae', 'lēs', 'ti', 'bus', 'i', 'rae'])
    >>> positional_hex
    Verse(original='impulerit. Tantaene animis caelestibus irae?', scansion='-  U U -    -   -   U U -    - -  U U  -  - ', meter='hexameter', valid=True, syllable_count=15, accented='īmpulerīt. Tāntaene animīs caelēstibus īrae?', scansion_notes=['Valid by positional stresses.'], syllables = ['īm', 'pu', 'le', 'rīt', 'Tān', 'taen', 'a', 'ni', 'mīs', 'cae', 'lēs', 'ti', 'bus', 'i', 'rae'])
    """

    def __init__(
        self,
        original,
        scansion="",
        meter=None,
        valid=False,
        syllable_count=0,
        accented="",
        scansion_notes=None,
        syllables=None,
    ):
        if scansion_notes is None:
            scansion_notes = []
        if syllables is None:
            syllables = []
        self.original = original
        self.scansion = scansion
        self.meter = meter
        self.valid = valid
        self.syllable_count = syllable_count
        self.accented = accented
        self.scansion_notes = scansion_notes
        self.syllables = syllables
        self.working_line = ""  #: placeholder for data transformations

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return "{}(original={!r}, scansion={!r}, meter={!r}, valid={!r}, syllable_count={!r}," " accented={!r}, scansion_notes={!r}, syllables = {!r})".format(
            class_name,
            self.original,
            self.scansion,
            self.meter,
            self.valid,
            self.syllable_count,
            self.accented,
            self.scansion_notes,
            self.syllables,
        )

    def __iter__(self):
        return (
            i
            for i in (
                self.original,
                self.scansion,
                self.meter,
                self.valid,
                self.syllable_count,
                self.accented,
                ", ".join(self.scansion_notes),
                ", ".join(self.syllables),
            )
        )

    def __hash__(self):
        base = (
            hash(self.original)
            ^ hash(self.scansion)
            ^ hash(self.meter)
            ^ hash(self.valid)
            ^ hash(self.syllable_count)
            ^ hash(self.accented)
        )
        for note in self.scansion_notes:
            base = base ^ hash(note)
        for syl in self.syllables:
            base = base ^ hash(syl)
        return base

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __bool__(self):
        return self.valid
