import re

with open('./latin-analyses.txt') as file_opened:
    string_raw = file_opened.read()
    string_rows = string_raw.splitlines()
    latin_analyses_dict = {}
    for row in string_rows:
        headword = row.split('\t', 1)[0]
        #print(headword)
        analyses_string = row.split('\t', 1)[1]
        reg_bracket = re.compile('\{.*?\}')
        analyses = reg_bracket.findall(analyses_string)
        perseus_pos = {}
        for analysis in analyses:
            parts = analysis.split('\t')
            first = parts[0][1:]
            gloss = parts[1]
            third = parts[2][:-1]
            reg_digits = re.compile('\w+')
            perseus_headword_id = reg_digits.findall(first)[0]
            perseus_pos_id = reg_digits.findall(first)[1]
            persues_parsed = reg_digits.findall(first)[2]
            try:
                perseus_headword = reg_digits.findall(first)[3]
            except:
                pass
            #print(third)
            pos = third.split(' ')
            #print(pos[0])
            verb = {}
            if pos[0] in ('fut', 'futperf', 'imperf', 'perf', 'pres', 'plup'):
                verb['tense'] = pos[0]
                perseus_pos['pos_type'] = 'verb'
                perseus_pos['parts'] = verb
                if pos[1] in ('ind', 'imperat', 'subj'):
                    if pos[2] in ('act', 'pass'):
                        if pos[3] in ('1st', '2nd', '3rd'):
                            pass
                        else:
                            print(pos[3])
                    else:
                        print(pos[2])
                elif pos[1] in ('part'):
                    pass
                elif pos[1] in ('inf'):
                    pass
                elif pos[1] in ('act', 'pass'):
                    pass
                else:
                    pass
            elif pos[0] == 'gerundive':
                pass
            elif pos[0] in ('fem', 'masc', 'neut', 'masc/fem/neut', 'masc/fem', 'masc/neut'):
                pass
            elif pos[0] == 'supine':
                pass
            elif pos[0] == 'indeclform':
                pass
            elif pos[0] == 'adverbial':
                pass
            elif pos[0] in ('nom', 'abl', 'gen','dat', 'nom/acc', 'nom/voc'):
                pass
            elif pos[0] == 'sg':
                pass #??? ex: ut, uter, altus, alter
            elif pos[0] == 'comp':
                pass # ex: diu, se
            elif pos[0] in ('subj', 'ind'):
                pass # ex: fio, impleo, deleo, compleo
            elif pos[0] == 'nu_movable':
                pass #only 1 ex: sum
            else:
                pass
