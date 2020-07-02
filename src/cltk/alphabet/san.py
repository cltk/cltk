"""Data module for the Sanskrit languages alphabet and related characters."""

# The digits in sanskrit start from index 0 to 9. The index
# of the list tells about the corresponding number digit in Sanskrit

DIGITS = ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"]

# This is a list of Simple Vowels for Sanskrit Language.
# They give the sound aaa, e, ee, u, uuu,e,o, ri, lri

INDEPENDENT_VOWELS_SIMPLE = ["अ", "आ", "इ", "ई", "उ", "ऊ", "ए", "ओ", "ऋ", "ऌ"]

# These vowels are dipthongs in Sanskrit meaning they are pronounced differently depending on
# They give the sound ai, au

INDEPENDENT_VOWELS_DIPTHONGS = ["ऐ", "औ"]

# These are other independent alphabets which are not vowels or consonants either but are placed in with vowels
# These are anuswara and visarga
# Anuswara gives a nasal sound and its point of pronounciation is same as the consonant that follows it
# For example, The word Sanskrit has a anuswara and is pronounced as sans-kri-ta.
# Anuswara is pronounced like "h" in "house".

INDEPENDENT_VOWELS = ["अं", "अः"]

# The given are the dependent vowels, these are added after or on the consonants

DEPENDENT_VOWELS = ["ा", "ि", "ी", "ु", "ू", "े", "ै", "ो", "ौ", "ं", "ः", "ृ", "ॄ"]

# These are the various consonants in Sanskrit.
# As we move from Index 0 to the last index of the list, We go from unaspirated to nasal.


# These consonants require the part of throat for pronouncing

CONSONANT_GUTTURALS = ["क", "ख", "ग", "घ", "ङ"]

# These consonants require rear tongue parts for the pronounciation of the consonant

CONSONANT_PALATALS = ["च", "छ", "ज", "झ", "ञ"]

# These consonant require tongue tip for pronounciation

CONSONANT_CEREBRALS = ["ट", "ठ", "ड", "ढ", "ण"]

# These consonant require the top teeth part for the pronounciation

CONSONANT_DENTALS = ["त", "थ", "द", "ध", "न"]

# These consonants require the part of lips for pronounciation

CONSONANT_LABIALS = ["प", "फ", "ब", "भ", "म"]

# These almost sound like vowel when pronouncing, hence semi-vowel

SEMIVOWEL_CONSONANT = ["य", "र", "ल", "व"]

# These consonants make a hiss sound when pronounced.
SIBILANT_CONSONANT = ["श", "ष", "स"]

# This consonant requires air to come out of lungs for the pronounciation
SONANT_ASPIRATE = ["ह"]


# These are the other alphabets which are used in Sanskrit language.
# At Index 0, The alphabet is called Om symbol.At Index 1, we have the Virama Symbol(also called halant)
# which is used in sacred texts for supressing inherent vowels in the consonant letter.
# At Index 3 we have chandrabindu used for nasalization of vowel.
# At Index 4 we have the letter called avagraha, 5th Index symbol is called as the nukta
# At index 6 and 7 we have the danda and double-danda used for ending shlokas in Sanskrit

OTHER_ALPHABETS = ["ॐ", "्", "ँ", "ऽ", "़", "।", "॥"]
