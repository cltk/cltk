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
          '(\bere\b)|(\bert\b)|(\bfui\b)|(\bfus\b)|(\bier\b)|(\bert\b)|(\bes\b)|(\bfu\b)', 'estre')

avoir_replace = ('(\bavreient\b)|(\bavroient\b)|(\beüssions\b)|(\beüssiens\b)|(\bavrarai\b)|(\bavreies\b)|'
         '(\bavroies\b)|(\bavreiet\b)|(\bavroiet\b)|(\bavrïens\b)|(\bavrïons\b)|(\bavriiez\b)|'
         '(\beüssiez\b)|(\beüssent\b)|(\beüstes\b)|(\bóurent\b)|(\bavrons\b)|(\bavront\b)|(\bavreie\b)|'
         '(\bavrïez\b)|(\beüsses\b)|(\beüssez\b)|(\bavons\b)|(\beümes\b)|(\borent\b)|(\bavrai\b)|'
         '(\bavras\b)|(\bavrez\b)|(\baiens\b)|(\bayons\b)|(\baient\b)|(\beüsse\b)|(\bavez\b)|(\bavra\b)|'
         '(\barai\b)|(\baies\b)|(\baiet\b)|(\baiez\b)|(\bayez\b)|(\beüst\b)|(\bont\b)|(\beüs\b)|'
         '(\boüs\b)|(\bóut\b)|(\boiz\b)|(\baie\b)|(\bait\b)|(\bai\b)|(\bas\b)|(\bat\b)|(\boi\b)|'
         '(\bot\b)|(\boü\b)|(\beü\b)|(\ba\b)', 'avoir')



