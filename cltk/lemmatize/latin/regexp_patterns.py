pia_patterns = [(r'(\w*)o\b', 1),
                (r'(\w*)[a|e|i]?s\b', 1),
                (r'(\w*)[a|e|i]?t\b', 1),
                (r'(\w*)[a|e|i]?mus\b', 1),
                (r'(\w*)[a|e|i]?tis\b', 1),
                (r'(\w*)[a|e|u]nt\b', 1)]

pip_patterns = [(r'(\w*)or\b', 1),
                (r'(\w*)[a|e]ris\b', 1),
                (r'(\w*e)ris\b', 1),
                (r'(\w*)[a|e|i]tur\b', 1),
                (r'(\w*e)tur\b', 1),
                (r'(\w*)[a|e|i]?mur\b', 1),
                (r'(\w*)[a|e|i]mini\b', 1),
                (r'(\w*)[a|e|u]ntur\b', 1)]

psa_patterns = [(r'(\w*)em\b', 1),
                (r'(\w*)[a|e|ia]s\b', 1),
                (r'(\w*)[a|e|ia]t\b', 1),
                (r'(\w*)[a|e|ia]mus\b', 1),
                (r'(\w*)[a|e|ia]?tis\b', 1),
                (r'(\w*)[a|e|ia]nt\b', 1)]

iia_patterns = [(r'(\w*)[a|ie]bam', 1),
                (r'(\w*)[a|ie]bas\b', 1),
                (r'(\w*)[a|ie]bat\b', 1),
                (r'(\w*)[a|ie]bamus\b', 1),
                (r'(\w*)[a|ie]batis\b', 1),
                (r'(\w*)[a|ie]bant\b', 1),
                (r'(\w*e?)bam\b', 1),
                (r'(\w*e?)bas\b', 1),
                (r'(\w*e?)bat\b', 1),
                (r'(\w*e?)bamus\b', 1),
                (r'(\w*e?)batis\b', 1),
                (r'(\w*e?)bant\b', 1), ]

isa_patterns = [(r'(\w*)m', 2),
                (r'(\w*)s\b', 2),
                (r'(\w*)t\b', 2),
                (r'(\w*)mus\b', 2),
                (r'(\w*)ris\b', 2),
                (r'(\w*)nt\b', 2)]

iip_patterns = [(r'(\w*)[a|ie]bar', 1),
                (r'(\w*)[a|ie]baris\b', 1),
                (r'(\w*)[a|ie]batur\b', 1),
                (r'(\w*)[a|ie]bamur\b', 1),
                (r'(\w*)[a|ie]bamini\b', 1),
                (r'(\w*)[a|ie]bant\b', 1),
                (r'(\w*e?)bar\b', 1),
                (r'(\w*e?)baris\b', 1),
                (r'(\w*e?)batur\b', 1),
                (r'(\w*e?)bamur\b', 1),
                (r'(\w*e?)bamini\b', 1),
                (r'(\w*e?)bantur\b', 1), ]

isp_patterns = [(r'(\w*)r', 2),
                (r'(\w*)ris\b', 2),
                (r'(\w*)tur\b', 2),
                (r'(\w*)mur\b', 2),
                (r'(\w*)mini\b', 2),
                (r'(\w*)ntur\b', 2)]

fia_patterns = [(r'(\w*)[a|ie]bo\b', 1),
                (r'(\w*)[a|ie]bis\b', 1),
                (r'(\w*)[a|ie]bit\b', 1),
                (r'(\w*)[a|ie]bimus\b', 1),
                (r'(\w*)[a|ie]bitis\b', 1),
                (r'(\w*)[a|ie]bunt\b', 1),
                (r'(\w*e)bo\b', 1),
                (r'(\w*e?)bis\b', 1),
                (r'(\w*e?)bit\b', 1),
                (r'(\w*e?)bimus\b', 1),
                (r'(\w*e?)bitis\b', 1),
                (r'(\w*e?)bunt\b', 1),
                (r'(\w*)am\b', 1),
                (r'(\w*)es\b', 1),
                (r'(\w*)et\b', 1),
                (r'(\w*)emus\b', 1),
                (r'(\w*)etis\b', 1),
                (r'(\w*)ent\b', 1)]

fip_patterns = [(r'(\w*)[a|ie]bor\b', 1),
                (r'(\w*)[a|ie]beris\b', 1),
                (r'(\w*)[a|ie]bitur\b', 1),
                (r'(\w*)[a|ie]bimur\b', 1),
                (r'(\w*)[a|ie]bimini\b', 1),
                (r'(\w*)[a|ie]buntur\b', 1),
                (r'(\w*e)bor\b', 1),
                (r'(\w*e?)beris\b', 1),
                (r'(\w*e?)bitur\b', 1),
                (r'(\w*e?)bimur\b', 1),
                (r'(\w*e?)bimini\b', 1),
                (r'(\w*e?)buntur\b', 1),
                (r'(\w*)ar\b', 1),
                (r'(\w*)eris\b', 1),
                (r'(\w*)etur\b', 1),
                (r'(\w*)emur\b', 1),
                (r'(\w*)emini\b', 1),
                (r'(\w*)entur\b', 1)]

pfia_patterns = [(r'(\w*)i\b', 3),
                 (r'(\w*)isti\b', 3),
                 (r'(\w*)it\b', 3),
                 (r'(\w*)imus\b', 3),
                 (r'(\w*)istis\b', 3),
                 (r'(\w*)erunt\b', 3)]

pfsa_patterns = []

ppfa_patterns = [(r'(\w*)eram\b', 3),
                 (r'(\w*)eras\b', 3),
                 (r'(\w*)erat\b', 3),
                 (r'(\w*)eramus\b', 3),
                 (r'(\w*)eratis\b', 3),
                 (r'(\w*)erant\b', 3)]

ppfsa_patterns = [(r'(\w*)issem', 3),
                  (r'(\w*)isses\b', 3),
                  (r'(\w*)isset\b', 3),
                  (r'(\w*)issemus\b', 3),
                  (r'(\w*)issetis\b', 3),
                  (r'(\w*)issent\b', 3),
                  (r'(\w*)asset\b', 1)]

fpfa_patterns = [(r'(\w*)erim\b', 3),
                 (r'(\w*)eris\b', 3),
                 (r'(\w*)erit\b', 3),
                 (r'(\w*)erimus\b', 3),
                 (r'(\w*)eritis\b', 3),
                 (r'(\w*)erint\b', 3)]

verb_ending_patterns = fpfa_patterns + ppfa_patterns + pfia_patterns + iia_patterns + fia_patterns + pia_patterns + pip_patterns + iip_patterns + psa_patterns + isa_patterns + isp_patterns + pfsa_patterns + ppfsa_patterns

### Regexp patterns for use with the RomanNumeralLemmatizer
roman_numeral_patterns = [(r'(?=^[MDCLXVUI]+$)(?=^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|IU|V?I{0,3}|U?I{0,3})$)', 'NUM'),
            (r'(?=^[mdclxvui]+$)(?=^m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,4})(ix|iv|iu|v?i{0,3}|u?i{0,3})$)', 'NUM')]