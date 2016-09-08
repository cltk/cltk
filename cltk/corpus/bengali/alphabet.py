"""Bengali is an Indic language which uses Bengali script, closely related to Devanagri script, both
deriving from Brahmi script. Bengali script is also used to write other languages, including
Assamese, Daphla, Garo, Hallam, Khasi, Manipuri, Mizo, Munda, Naga, Rian and Santali 
Bengali character set is divided into 21 vowels, 36 consonants and modifiers. The vowels
themselves can be divided into dependent and independent vowels"""



# The digits in bengali start from index 0 to 9.

DIGITS = ['০','১','২','৩','৪','৫','৬','৭','৮','৯']

VOWELS = ['অ','আ','ই','ঈ','উ','ঊ','এ','ঐ','ও','ঔ']

DEPENDENT_VOWELS = ['◌া','ি','◌ী','◌ু','◌ূ','◌ৃ','ে','ৈ','ো','ৌ']

CONSONANTS = ['ক','খ','গ','ঘ ','ঙ','চ',' ছ ','জ','ঝ',' ঞ','ট',' ঠ', 'ড',' ঢ', 'ণ','ত', 'থ',' দ',' ধ',' ন', 'প', 'ফ', 'ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'ষ','স', 'হ', 'ড় ','ঢ়', 'য়', 'ৎ‌']


# Along with consonants and vowels there are some special modifiers, called Virama, Visarga, Anusvara, Candrabindu and Ishar. 
# Anusvara is used for final velar nasal sound, Visarga adds voiceless breath after vowel and Candrabindu is used to nasalize vowels 

MODIFIERS = ['◌্','◌ঁ','◌ং','◌ঃ']
