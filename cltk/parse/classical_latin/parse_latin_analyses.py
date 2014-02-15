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
            if pos[0] in ('pres', 'imperf', 'fut', 'perf', 'plup', 'futperf'):
                verb['tense'] = pos[0]
                perseus_pos['type'] == 'verb'
                perseus_pos['pos'] == verb
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
                print(perseus_headword,pos)
            '''
            if pos[0] == 'gerundive':
                perseus_pos['GERUNDIVE'] = pos[0]
                #print('found gerundive')
            elif pos[0] == 'pres' or 'imperf' or 'fut' or 'perf' or 'plup' or 'futperf':
                perseus_pos['VERB'] = pos[0]
                print('found a verb')
            elif pos[0] == 'fem' or 'masc' or 'neut':
                perseus_pos['Noun'] = pos[0]
                #print('found a noun')
            elif pos[0] == 'fem' or 'masc' or 'neut':
                perseus_pos['Noun'] = pos[0]
            else:
                print(pos[0])
                #print('found nothing')
            '''

            #indeclform

            #print(perseus_headword_id)
            #print(perseus_pos_id)
            #for part in parts:
            #print(part)
            #print(splitted)
            #reg_digits = re.compile('\d*')
            #zero = reg_digits.findall(splitted)
            #little_number = reg_digits.findall(splitted)[3]
            #print(zero)
            #print(little_number)


        '''
        reg_headword = re.compile('\w+')
        headword = reg_headword.findall(row)[0]
        print(headword)
        reg_bracket = re.compile('\{.*?\}')
        def_brackets = reg_bracket.findall(row)
        headword_dict = {}
        for bracket in def_brackets:
            #print(bracket)
            reg_digits = re.compile('\d*')
            big_number = reg_digits.findall(bracket)[1]
            little_number = reg_digits.findall(bracket)[3]
            #print(big_number)
            #print(little_number)
            reg_alphnum = re.compile('[a-zA-Z0-9_\,\-]*')
            keys = reg_alphnum.findall(bracket)[5]#this actually point to the headwords they belong to, I think; these needs to be parsed and looped
            #print(inflections)
            pos_def = reg_alphnum.findall(bracket)[6:]#this actually has the english def in there too, which needs to be removed
            #pos_filtered = [x for x in pos_def if x is not '']
            pos_def_filtered = list(filter(''.__ne__, pos_def))
            #print(pos_filtered)
            headword_dict['big_number'] = big_number
            headword_dict['little_number'] = little_number
            headword_dict['pos_def'] = pos_def_filtered
            print(headword_dict)
        '''
