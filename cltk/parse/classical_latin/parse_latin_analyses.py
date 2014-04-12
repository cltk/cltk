"""rework Perseus latin-analyses.txt into Python dictionary"""
#!TODO
#add perseus word ids
#break multiple cases (eg, nom/acc/voc) and genders (masc/neut)
from pprint import pprint
import re

with open('./latin-analyses.txt') as file_opened:
    string_raw = file_opened.read()
    string_rows = string_raw.splitlines()
    headword_dict = {}
    for row in string_rows:
        perseus_pos_dict = {}
        headword = row.split('\t', 1)[0]
        analyses_string = row.split('\t', 1)[1]
        reg_bracket = re.compile('\{.*?\}')
        analyses = reg_bracket.findall(analyses_string)
        print(headword)
        pos_counter = -1
        perseus_pos_list = []
        for analysis in analyses:
            pos_counter += 1
            pos_iterator = 'pos' + str(pos_counter)
            parts = analysis.split('\t')
            first = parts[0][1:]
            gloss = parts[1]
            if gloss == ' ':
                gloss = ''
            third = parts[2][:-1]
            reg_digits = re.compile('\w+')
            perseus_headword_id = reg_digits.findall(first)[0]
            #print(perseus_headword_id)
            perseus_pos_id = reg_digits.findall(first)[1]
            #print(perseus_pos_id)
            perseus_parsed = reg_digits.findall(first)[2]
            #print(perseus_parsed)
            try:
                perseus_headword = reg_digits.findall(first)[3]
            except:
                pass
            pos = third.split(' ')
            word_dict = {}
            pos_dict = {}
            if pos[0] in ('fut', 'futperf', 'imperf', 'perf', 'pres', 'plup'):
                pos_dict['type'] = 'verb'
                pos_dict['tense'] = pos[0]
                if pos[1] in ('ind', 'imperat', 'subj'):
                    pos_dict['mood'] = pos[1]
                    if pos[2] in ('act', 'pass'):
                        pos_dict['voice'] = pos[2]
                        if pos[3] in ('1st', '2nd', '3rd'):
                            pos_dict['person'] = pos[3]
                            if pos[4] in ('pl', 'sg'):
                                pos_dict['number'] = pos[4]
                                pos_dict['gloss'] = gloss
                                word_dict[pos_iterator] = pos_dict
                                perseus_pos_list.append(word_dict)
                                perseus_pos_dict['perseus_pos'] = perseus_pos_list
                                headword_dict[headword] = perseus_pos_dict
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                elif pos[1] in ('part'):
                    pos_dict['tense'] = pos[0]
                    pos_dict['participle'] = pos[1]
                    if pos[2] in ('act', 'pass'):
                        pos_dict['voice'] = pos[2]
                        if pos[3] in ('fem', 'masc', 'neut'):
                            pos_dict['gender'] = pos[3]
                            if pos[4] in ('abl', 'acc', 'dat', 'gen', 'voc', 'nom', 'nom/voc', 'nom/voc/acc'):
                                pos_dict['case'] = pos[4]
                                try:
                                    if pos[5] in ('pl', 'sg'):
                                        pos_dict['number'] = pos[5]
                                        pos_dict['gloss'] = gloss
                                        word_dict[pos_iterator] = pos_dict
                                        perseus_pos_list.append(word_dict)
                                        perseus_pos_dict['perseus_pos'] = perseus_pos_list
                                        headword_dict[headword] = perseus_pos_dict

                                    else:
                                        pass
                                #~10 -iens participles w/o number
                                except:
                                    pos_dict['number'] = 'sg'
                                    pos_dict['gloss'] = gloss
                                    word_dict[pos_iterator] = pos_dict
                                    perseus_pos_list.append(word_dict)
                                    perseus_pos_dict['perseus_pos'] = perseus_pos_list
                                    headword_dict[headword] = perseus_pos_dict
                    #b/c voice left off present tense participles
                    elif pos[2] in ('masc/fem/neut', 'masc/fem', 'neut'):
                        pos_dict['voice'] = 'act'
                        if pos[3] in ('acc', 'gen', 'abl', 'dat', 'nom/voc/acc', 'nom/voc'):
                            if pos[3] in ('pl', 'sg'):
                                pos_dict['number'] = pos[4]
                                pos_dict['gloss'] = gloss
                                word_dict[pos_iterator] = pos_dict
                                perseus_pos_list.append(word_dict)
                                perseus_pos_dict['perseus_pos'] = perseus_pos_list
                                headword_dict[headword] = perseus_pos_dict
                        else:
                            pass
                    else:
                        if pos[2] in ('abl', 'dat', 'gen'):
                            #b/c voice left off present voice participles
                            pos_dict['voice'] = 'act'
                            pos_dict['gloss'] = gloss
                            word_dict[pos_iterator] = pos_dict
                            perseus_pos_list.append(word_dict)
                            perseus_pos_dict['perseus_pos'] = perseus_pos_list
                            headword_dict[headword] = perseus_pos_dict
                        else:
                            pass
                elif pos[1] in ('inf'):
                    if pos[2] in ('act', 'pass'):
                        pos_dict['voice'] = pos[2]
                        pos_dict['gloss'] = gloss
                        word_dict[pos_iterator] = pos_dict
                        perseus_pos_list.append(word_dict)
                        perseus_pos_dict['perseus_pos'] = perseus_pos_list
                        headword_dict[headword] = perseus_pos_dict
                    else:
                        pass
                elif pos[1] in ('act', 'pass'):
                    #ferre verbs
                    pos_dict['voice'] = pos[1]
                    if pos[2] in ('1st', '2nd', '3rd'):
                        pos_dict['person'] = pos[2]
                        if pos[3] in ('pl', 'sg'):
                            pos_dict['number'] = pos[3]
                            pos_dict['gloss'] = gloss
                            word_dict[pos_iterator] = pos_dict
                            perseus_pos_list.append(word_dict)
                            perseus_pos_dict['perseus_pos'] = perseus_pos_list
                            headword_dict[headword] = perseus_pos_dict
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            elif pos[0] == 'gerundive':
                pos_dict['type'] = 'gerundive'
                if pos[1] in ('fem', 'neut', 'masc', 'masc/neut'):
                    pos_dict['gender'] = pos[1]
                    if pos[2] in ('abl', 'acc', 'dat', 'gen', 'voc', 'nom', 'nom/voc', 'nom/voc/acc'):
                        if pos[3] in ('pl', 'sg'):
                            pos_dict['number'] = pos[3]
                            pos_dict['gloss'] = gloss
                            word_dict[pos_iterator] = pos_dict
                            perseus_pos_list.append(word_dict)
                            perseus_pos_dict['perseus_pos'] = perseus_pos_list
                            headword_dict[headword] = perseus_pos_dict
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            elif pos[0] in ('fem', 'masc', 'neut', 'masc/fem/neut', 'masc/fem', 'masc/neut'):
                pos_dict['type'] = 'substantive'
                pos_dict['gender'] = pos[0]
                try:
                    if pos[1] in ('abl', 'acc', 'dat', 'gen', 'voc', 'nom', 'nom/voc', 'nom/voc/acc'):
                        pos_dict['case'] = pos[1]
                        if pos[2] in ('pl', 'sg'):
                            pos_dict['number'] = pos[2]
                            pos_dict['gloss'] = gloss
                            word_dict[pos_iterator] = pos_dict
                            perseus_pos_list.append(word_dict)
                            perseus_pos_dict['perseus_pos'] = perseus_pos_list
                            headword_dict[headword] = perseus_pos_dict
                        else:
                            if pos[2] in ('comp', 'superl'):
                                pos_dict['comparison'] = pos[2]
                                pos_dict['gloss'] = gloss
                                word_dict[pos_iterator] = pos_dict
                                perseus_pos_list.append(word_dict)
                                perseus_pos_dict['perseus_pos'] = perseus_pos_list
                                headword_dict[headword] = perseus_pos_dict
                            else:
                                pass
                    else:
                        if pos[1] in ('pl', 'sg'):
                            pos_dict['number'] = pos[1]
                            pos_dict['gloss'] = gloss
                            word_dict[pos_iterator] = pos_dict
                            perseus_pos_list.append(word_dict)
                            perseus_pos_dict['perseus_pos'] = perseus_pos_list
                            headword_dict[headword] = perseus_pos_dict
                except:
                    pos_dict['case'] = 'indeclinable'
                    pos_dict['gender'] = pos[0]
                    pos_dict['number'] = 'sg'
                    pos_dict['gloss'] = gloss
                    word_dict[pos_iterator] = pos_dict
                    perseus_pos_list.append(word_dict)
                    perseus_pos_dict['perseus_pos'] = perseus_pos_list
                    headword_dict[headword] = perseus_pos_dict
            elif pos[0] == 'supine':
                pos_dict['type'] = pos[0]
                if pos[1] == 'neut':
                    pos_dict['gender'] = pos[1]
                    if pos[2] in ('nom', 'dat'):
                        pos_dict['case'] = pos[2]
                        if pos[3] == 'sg':
                            pos_dict['number'] = pos[3]
                            pos_dict['gloss'] = gloss
                            word_dict[pos_iterator] = pos_dict
                            perseus_pos_list.append(word_dict)
                            perseus_pos_dict['perseus_pos'] = perseus_pos_list
                            perseus_pos_dict[headword] = word_dict

                    else:
                        pass
                else:
                    pass
            elif pos[0] == 'indeclform':
                pos_dict['case'] = pos[0]
                pos_dict['type'] = pos[1][1:-1]
                pos_dict['gloss'] = gloss
                word_dict[pos_iterator] = pos_dict
                perseus_pos_list.append(word_dict)
                perseus_pos_dict['perseus_pos'] = perseus_pos_list
                headword_dict[headword] = perseus_pos_dict
            elif pos[0] == 'adverbial':
                if pos[0] == 'adverbial':
                    pos_dict['type'] = pos[0]
                    try:
                        if pos[1] in ('comp', 'superl'):
                            pos_dict['comparison'] = pos[1]
                            pos_dict['gloss'] = gloss
                            word_dict[pos_iterator] = pos_dict
                            perseus_pos_list.append(word_dict)
                            perseus_pos_dict['perseus_pos'] = perseus_pos_list
                            headword_dict[headword] = perseus_pos_dict
                        else:
                            pass
                    except:
                        pass
                else:
                    pass
            #!confirm that these elifs don't output anything
            elif pos[0] in ('nom', 'abl', 'gen', 'dat', 'nom/acc', 'nom/voc'):
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
#pprint(headword_dict)
try:
    with open('cltk_analyses.txt', 'w') as new_file:
        #write_morph.write(str(inflections))
        pprint(headword_dict, stream=new_file)
except IOError:
    pass
