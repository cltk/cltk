from fuzzywuzzy import fuzz
from fuzzywuzzy import process

query = "Jore"

choices = ['George', "Jacques", "saint George", "Jorge"]

b = process.extract(query, choices)
#print(fuzz.ratio('veisin', 'voisins'))
a = process.extractOne(query, choices)
print(a)


estre_replace = ('(\bsereient\b)|(\bfussions\b)|(\bfussiens\b)|(\bsereies\b)|(\bsereiet\b)|(\bserïens\b)|(\bseriiez\b)|'
          '(\bfussiez\b)|(\bfussent\b)|(\bierent\b)|(\bfustes\b)|(\bfurent\b)|(\bierent\b)|(\bsereie\b)|(\bseroie\b)|'
          '(\bsereit\b)|(\bseiens\b)|(\bseient\b)|(\bfusses\b)|(\bfussez\b)|(\bestant\b)|(\bseiens\b)|(\bsomes\b)|'
          '(\bestes\b)|(\bieres\b)|(\bieres\b)|(\beiens\b)|(\beriez\b)|(\berent\b)|(\bfumes\b)|(\birmes\b)|(\bertes\b)|'
          '(\bseies\b)|(\bseiet\b)|(\bseiez\b)|(\bfusse\b)|(\bseies\b)|(\bseiez\b)|(\bsuis\b)|(\bsont\b)|(\biere\b)|'
          '(\beres\b)|(\beret\b)|(\biers\b)|(\biert\b)|(\bseie\b)|(\bseit\b)|(\bfust\b)|(\besté\b)|(\bies\b)|(\best\b)|'
          '(\bere\b)|(\bert\b)|(\bfui\b)|(\bfus\b)|(\bier\b)|(\bert\b)|(\bes\b)|(\bfu\b)', '\bestre\b')

avoir_replace = ('(\bavreient\b)|(\bavroient\b)|(\beüssions\b)|(\beüssiens\b)|(\bavrarai\b)|(\bavreies\b)|'
         '(\bavroies\b)|(\bavreiet\b)|(\bavroiet\b)|(\bavrïens\b)|(\bavrïons\b)|(\bavriiez\b)|'
         '(\beüssiez\b)|(\beüssent\b)|(\beüstes\b)|(\bóurent\b)|(\bavrons\b)|(\bavront\b)|(\bavreie\b)|'
         '(\bavrïez\b)|(\beüsses\b)|(\beüssez\b)|(\bavons\b)|(\beümes\b)|(\borent\b)|(\bavrai\b)|'
         '(\bavras\b)|(\bavrez\b)|(\baiens\b)|(\bayons\b)|(\baient\b)|(\beüsse\b)|(\bavez\b)|(\bavra\b)|'
         '(\barai\b)|(\baies\b)|(\baiet\b)|(\baiez\b)|(\bayez\b)|(\beüst\b)|(\bont\b)|(\beüs\b)|'
         '(\boüs\b)|(\bóut\b)|(\boiz\b)|(\baie\b)|(\bait\b)|(\bai\b)|(\bas\b)|(\bat\b)|(\boi\b)|'
         '(\bot\b)|(\boü\b)|(\beü\b)|(\ba\b)', '\bavoir\b')

first_conj_rules = [('es\b|e\b|ons\b|ez\b|ent\b|z\b', 'er\b'),
                    ('ai\b|as\b|a\b|at\b|ames\b|astes\b|erent\b', 'er\b'),
                    ('asse\b', 'er\b'),
                    ('é\b', 'er\b')]

i_type_rules = [('i\b|is\b|it\b|imes\b|istes\b|irent\b', 'ir\b'),
                ('isse\b', 'ir\b')]

u_type_rules = [('ui\b|us\b|ut\b|umes\b|ustes\b|urent\b', 'oir\b'),
                ('usse\b', 'oir\b')]

regime_rules = [('on\b', 'e\b'),
                ('ain\b', 'e\b')]

plural_rules = [('ales\b', 'al\b'),
                ('s\b', '\b')]

misc_rules = [('x\b', 'l\b'),
              ('z\b', 't\b'),
              ('un\b', 'on\b'),
              ('eus\b', 'os\b'),
              ('\be\b', '\bet\b')]

masc_to_fem_rules = [('se\b', 'x\b'),
                     ('ive\b', 'if\b'),
                     ('ee\b', 'e\b')]

determiner_rules= [('\bli\b|\blo\b|\ble\b|\bla\b|\bles\b', '\ble\b'),
                   ('\bdel\b|\bdu\b', '\bde le\b'),
                   ('\bal\b|\bau\b', '\bà le\b'),
                   ('\bas\b|\baus\b|\baux\b', "\bà les\b"),
                   ('\buns\b|\bune\b|\bunes\b', '\bun\b')]

reduction_rules = [('d\'', 'de'),
                   ('m\'', 'me'),
                   ('t\'', 'te'),
                   ('l\'', 'lui/la/le')]




