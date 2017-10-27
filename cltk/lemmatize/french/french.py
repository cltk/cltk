import re
"""Rules are based on Brunot & Bruneau (1949).
"""


estre_replace = [('^sereient$|^fussions$|^fussiens$|^sereies$|^sereiet$|^serïens$|^seriiez$|^fussiez$|^fussent$|^ierent$|^fustes$|^furent$|^ierent$|^sereie$|^seroie$|^sereit$|^seiens$|^seient$|^fusses$|^fussez$|^estant$|^seiens$|^somes$|^estes$|^ieres$|^ieres$|^eiens$|^eriez$|^erent$|^fumes$|^irmes$|^ertes$|^seies$|^seiet$|^seiez$|^fusse$|^seies$|^seiez$|^suis$|^sont$|^iere$|^eres$|^eret$|^iers$|^iert$|^seie$|^seit$|^fust$|^esté$|^ies$|^est$|^ere$|^ert$|^fui$|^fus$|^ier$|^ert$|^es$|^fu$', 'estre')]

avoir_replace = [('^avreient$|^avroient$|^eüssions$|^eüssiens$|^avrarai$|^avreies$|'
         '^avroies$|^avreiet$|^avroiet$|^avrïens$|^avrïons$|^avriiez$|'
         '^eüssiez$|^eüssent$|^eüstes$|^óurent$|^avrons$|^avront$|^avreie$|'
         '^avrïez$|^eüsses$|^eüssez$|^avons$|^eümes$|^orent$|^avrai$|'
         '^avras$|^avrez$|^aiens$|^ayons$|^aient$|^eüsse$|^avez$|^avra$|'
         '^arai$|^aies$|^aiet$|^aiez$|^ayez$|^eüst$|^ont$|^eüs$|'
         '^oüs$|^óut$|^oiz$|^aie$|^ait$|^ai$|^as$|^at$|^oi$|'
         '^ot$|^oü$|^eü$|^a$', 'avoir')]


auxiliary_rules = estre_replace+avoir_replace



first_conj_rules = [('es$|e$|ons$|ez$|ent$|z$|(e)ai$|(e)as$|(e)a$|(e)at$|(e)ames$|(e)astes$|(e)erent$|(e)asse$|é$', 'er')]

i_type_rules = [('i$|is$|it$|imes$|istes$|irent$|isse$', 'ir')]

u_type_rules = [('ui$|us$|ut$|umes$|ustes$|urent$|usse$', 'oir')]


verbal_rules = u_type_rules+i_type_rules+first_conj_rules



regime_rules = [('on$|ain$', 'e')]

plural_rules = [('ales$|aux$|aus$', 'al'),
                ('s$', '')]

masc_to_fem_rules = [('se$', 'x'),
                     ('ive$', 'if'),
                     ('ee$', 'e')]


french_nominal_rules = regime_rules+plural_rules+masc_to_fem_rules



misc_rules = [('x$', 'l'),
              ('z$', 't'),
              ('un$', 'on'),
              ('eus$', 'os'),
              ('^e$', 'et')]


determiner_rules= [('^li$|^lo$|^le$|^la$|^les$', 'le'),
                   ('^del$|^du$', 'de le'),
                   ('^al$|^au$', 'a le'),
                   ('^as$|^aus$|^aux$', "a les"),
                   ('^uns$|^une$|^unes$', 'un')]


reduction_rules = [("d'", 'de'),
                   ("m'", 'me'),
                   ("t'", 'te'),
                   ("l'", 'le'),
                   ("qu'", "que")]


patterns = determiner_rules+misc_rules+auxiliary_rules+verbal_rules+french_nominal_rules+reduction_rules


def build_match_and_apply_functions(pattern, replace):
    def matches_rule(word):
        return re.search(pattern, word)
    def apply_rule(word):
        return re.sub(pattern, replace, word)
    return (matches_rule, apply_rule)



rules = [build_match_and_apply_functions(pattern, replace)
         for (pattern, replace) in patterns]


def regex(token):
    for matches_rule, apply_rule in rules:
        if matches_rule(token):
            return apply_rule(token)


