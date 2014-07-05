"""Build taggers and tag text"""
import logging
import os
from pprint import pprint
import re
import site


class MakePOSTagger(object):
    """rework Perseus latin-analyses.txt into Python dictionary"""

    def __init__(self):
        """identify absolute path to cltk_local dir
        TODO: add argument for cltk_local not at root"""
        self.cltk_bin_path = os.path.join(site.getsitepackages()[0], 'cltk')
        default_cltk_local = '~/cltk_local'
        cltk_local = os.path.expanduser(default_cltk_local)
        if os.path.isdir(cltk_local) is True:
            logging.info('cltk_local dir found.')
        else:
            logging.error('cltk_local dir not found.')
        log_path = os.path.join(cltk_local, 'cltk.log')
        logging.basicConfig(filename=log_path,
                            level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        self.cltk_local_compiled_pos_latin = \
            os.path.join(cltk_local, 'compiled', 'pos_latin')
        if os.path.isdir(self.cltk_local_compiled_pos_latin) is True:
            logging.info('compiled/pos_latin dir found.')
        else:
            logging.error('compiled/pos_latin dir not found.')
        self.cltk_latin_pos_dict_path = \
            os.path.join(self.cltk_local_compiled_pos_latin,
                         'cltk_latin_pos_dict.txt')

    def make_file(self):
        """build tagger out of old Perseus files
        TODO:
        add perseus word ids
        check if some entries (esp. at end) need gender manually added
        """
        lat_anal_txt = os.path.join(self.cltk_local_compiled_pos_latin,
                                    'latin-analyses.txt')
        with open(lat_anal_txt) as file_opened:
            string_raw = file_opened.read()
            string_rows = string_raw.splitlines()
            headword_dict = {}
            for row in string_rows:
                perseus_pos_dict = {}
                headword = row.split('\t', 1)[0]
                analyses_string = row.split('\t', 1)[1]
                reg_bracket = re.compile('\{.*?\}')
                analyses = reg_bracket.findall(analyses_string)
                # print(headword)
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
                    # TODO what are these doing?
                    # perseus_headword_id = reg_digits.findall(first)[0]
                    # perseus_pos_id = reg_digits.findall(first)[1]
                    # perseus_parsed = reg_digits.findall(first)[2]
                    try:
                        perseus_headword = reg_digits.findall(first)[3]
                    except:
                        pass
                    pos = third.split(' ')
                    word_dict = {}
                    pos_dict = {}
                    if pos[0] in ('fut', 'futperf', 'imperf', 'perf',
                                  'pres', 'plup'):
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
                                        perseus_pos_dict['perseus_pos'] = \
                                            perseus_pos_list
                                        headword_dict[headword] = \
                                            perseus_pos_dict
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        elif pos[1] in 'part':
                            pos_dict['tense'] = pos[0]
                            pos_dict['participle'] = pos[1]
                            if pos[2] in ('act', 'pass'):
                                pos_dict['voice'] = pos[2]
                                if pos[3] in ('fem', 'masc', 'neut'):
                                    pos_dict['gender'] = pos[3]
                                    if pos[4] in ('abl', 'acc', 'dat', 'gen',
                                                  'voc', 'nom', 'nom/voc',
                                                  'nom/voc/acc'):
                                        cases = pos[4]
                                        split_cases = cases.split('/')
                                        for a_case in split_cases:
                                            pos_dict['case'] = a_case
                                            try:
                                                if pos[5] in ('pl', 'sg'):
                                                    pos_dict['number'] = pos[5]
                                                    pos_dict['gloss'] = gloss
                                                    word_dict[pos_iterator] = \
                                                        pos_dict
                                                    perseus_pos_list.append(word_dict)
                                                    perseus_pos_dict['perseus_pos'] = \
                                                        perseus_pos_list
                                                    headword_dict[headword] = \
                                                        perseus_pos_dict

                                                else:
                                                    pass
                                            # ~10 -iens participles w/o number
                                            except:
                                                pos_dict['number'] = 'sg'
                                                pos_dict['gloss'] = gloss
                                                word_dict[pos_iterator] = \
                                                    pos_dict
                                                perseus_pos_list.append(word_dict)
                                                perseus_pos_dict['perseus_pos'] = \
                                                    perseus_pos_list
                                                headword_dict[headword] = \
                                                    perseus_pos_dict
                            # b/c voice left off present tense participles
                            elif pos[2] in ('masc/fem/neut', 'masc/fem',
                                            'neut'):
                                genders = pos[2]
                                genders_split = genders.split('/')
                                for a_gender in genders_split:
                                    pos_dict['gender'] = a_gender
                                    pos_dict['voice'] = 'act'
                                    if pos[3] in ('acc', 'gen', 'abl', 'dat',
                                                  'nom/voc/acc', 'nom/voc'):
                                        cases = pos[3]
                                        cases_split = cases.split('/')
                                        for a_case in cases_split:
                                            pos_dict['case'] = a_case
                                            if pos[3] in ('pl', 'sg'):
                                                pos_dict['number'] = pos[4]
                                                pos_dict['gloss'] = gloss
                                                word_dict[pos_iterator] = pos_dict
                                                perseus_pos_list.append(word_dict)
                                                perseus_pos_dict['perseus_pos'] = \
                                                    perseus_pos_list
                                                headword_dict[headword] = \
                                                    perseus_pos_dict
                                    else:
                                        pass
                            else:
                                if pos[2] in ('abl', 'dat', 'gen'):
                                    # b/c voice left off present voice
                                    # participles
                                    # TODO: make sure this is with the right
                                    # else
                                    pos_dict['voice'] = 'act'
                                    pos_dict['gloss'] = gloss
                                    word_dict[pos_iterator] = pos_dict
                                    perseus_pos_list.append(word_dict)
                                    perseus_pos_dict['perseus_pos'] = \
                                        perseus_pos_list
                                    headword_dict[headword] = \
                                        perseus_pos_dict
                                else:
                                    pass
                        elif pos[1] in 'inf':
                            if pos[2] in ('act', 'pass'):
                                pos_dict['voice'] = pos[2]
                                pos_dict['gloss'] = gloss
                                word_dict[pos_iterator] = pos_dict
                                perseus_pos_list.append(word_dict)
                                perseus_pos_dict['perseus_pos'] = \
                                    perseus_pos_list
                                headword_dict[headword] = perseus_pos_dict
                            else:
                                pass
                        elif pos[1] in ('act', 'pass'):
                            # ferre verbs
                            pos_dict['voice'] = pos[1]
                            if pos[2] in ('1st', '2nd', '3rd'):
                                pos_dict['person'] = pos[2]
                                if pos[3] in ('pl', 'sg'):
                                    pos_dict['number'] = pos[3]
                                    pos_dict['gloss'] = gloss
                                    word_dict[pos_iterator] = pos_dict
                                    perseus_pos_list.append(word_dict)
                                    perseus_pos_dict['perseus_pos'] = \
                                        perseus_pos_list
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
                            genders = pos[1]
                            genders_split = genders.split('/')
                            for a_gender in genders_split:
                                pos_dict['gender'] = a_gender
                                if pos[2] in ('abl', 'acc', 'dat', 'gen',
                                              'voc', 'nom', 'nom/voc',
                                              'nom/voc/acc'):
                                    cases = pos[2]
                                    cases_split = cases.split('/')
                                    for a_case in cases_split:
                                        pos_dict['case'] = a_case
                                        if pos[3] in ('pl', 'sg'):
                                            pos_dict['number'] = pos[3]
                                            pos_dict['gloss'] = gloss
                                            word_dict[pos_iterator] = pos_dict
                                            perseus_pos_list.append(word_dict)
                                            perseus_pos_dict['perseus_pos'] = \
                                                perseus_pos_list
                                            headword_dict[headword] = \
                                                perseus_pos_dict
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    elif pos[0] in ('fem', 'masc', 'neut', 'masc/fem/neut',
                                    'masc/fem', 'masc/neut'):
                        genders = pos[0]
                        genders_split = genders.split('/')
                        for a_gender in genders_split:
                            pos_dict['gender'] = a_gender
                            pos_dict['type'] = 'substantive'
                            pos_dict['gender'] = pos[0]
                            try:
                                if pos[1] in ('abl', 'acc', 'dat', 'gen',
                                              'voc', 'nom', 'nom/voc', 'nom/voc/acc'):
                                    cases = pos[1]
                                    cases_split = cases.split('/')
                                    for a_case in cases_split:
                                        pos_dict['case'] = a_case
                                        if pos[2] in ('pl', 'sg'):
                                            pos_dict['number'] = pos[2]
                                            pos_dict['gloss'] = gloss
                                            word_dict[pos_iterator] = pos_dict
                                            perseus_pos_list.append(word_dict)
                                            perseus_pos_dict['perseus_pos'] = \
                                                perseus_pos_list
                                            headword_dict[headword] = \
                                                perseus_pos_dict
                                        else:
                                            if pos[2] in ('comp', 'superl'):
                                                pos_dict['comparison'] = \
                                                    pos[2]
                                                pos_dict['gloss'] = gloss
                                                word_dict[pos_iterator] = \
                                                    pos_dict
                                                perseus_pos_list.append(word_dict)
                                                perseus_pos_dict['perseus_pos'] = \
                                                    perseus_pos_list
                                                headword_dict[headword] = \
                                                    perseus_pos_dict
                                            else:
                                                pass
                                else:
                                    if pos[1] in ('pl', 'sg'):
                                        pos_dict['number'] = pos[1]
                                        pos_dict['gloss'] = gloss
                                        word_dict[pos_iterator] = pos_dict
                                        perseus_pos_list.append(word_dict)
                                        perseus_pos_dict['perseus_pos'] = \
                                            perseus_pos_list
                                        headword_dict[headword] = \
                                            perseus_pos_dict
                            except:
                                pos_dict['case'] = 'indeclinable'
                                pos_dict['gender'] = pos[0]
                                pos_dict['number'] = 'sg'
                                pos_dict['gloss'] = gloss
                                word_dict[pos_iterator] = pos_dict
                                perseus_pos_list.append(word_dict)
                                perseus_pos_dict['perseus_pos'] = \
                                    perseus_pos_list
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
                                    perseus_pos_dict['perseus_pos'] = \
                                        perseus_pos_list
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
                                    perseus_pos_dict['perseus_pos'] = \
                                        perseus_pos_list
                                    headword_dict[headword] = perseus_pos_dict
                                else:
                                    pass
                            except:
                                pass
                        else:
                            pass
                    # ? confirm that these elifs don't output anything
                    # maybe do fix at 113
                    # yes this has values:
                    elif pos[0] in ('nom', 'abl', 'gen', 'dat', 'nom/acc',
                                    'nom/voc'):
                        cases = pos[0]
                        cases_split = cases.split('/')
                        for a_case in cases_split:
                            pos_dict['case'] = a_case
                            if pos[1] in 'comp':
                                pos_dict['comparison'] = pos[1]
                                try:
                                    if pos[2] in ('sg', 'pl'):
                                        pos_dict['case'] = pos[2]
                                        word_dict[pos_iterator] = pos_dict
                                        perseus_pos_list.append(word_dict)
                                        perseus_pos_dict['perseus_pos'] = \
                                            perseus_pos_list
                                        headword_dict[headword] = \
                                            perseus_pos_dict
                                    else:
                                        pass
                                except:
                                    pass
                            elif pos[1] in ('sg', 'pl'):
                                pos_dict['type'] = 'substantive'
                                pos_dict['number'] = pos[1]
                                # ?gender? all 3?
                                word_dict[pos_iterator] = pos_dict
                                perseus_pos_list.append(word_dict)
                                perseus_pos_dict['perseus_pos'] = \
                                    perseus_pos_list
                                headword_dict[headword] = perseus_pos_dict
                            else:
                                pass
                    elif pos[0] == 'sg':
                        pos_dict['type'] = 'substantive'
                        pos_dict['number'] = pos[0]
                        # ?gender? all 3?
                        word_dict[pos_iterator] = pos_dict
                        perseus_pos_list.append(word_dict)
                        perseus_pos_dict['perseus_pos'] = perseus_pos_list
                        headword_dict[headword] = perseus_pos_dict
                    elif pos[0] == 'comp':
                        pos_dict['comparison'] = pos[0]
                        # adv or subst?: diutius, diutiusque, setius
                        # I'm calling these adverbs, but maybe should be
                        # written as substantives too
                        pos_dict['type'] = 'adverbial'
                        word_dict[pos_iterator] = pos_dict
                        perseus_pos_list.append(word_dict)
                        perseus_pos_dict['perseus_pos'] = perseus_pos_list
                        headword_dict[headword] = perseus_pos_dict
                    elif pos[0] in ('subj', 'ind'):
                        pos_dict['type'] = 'verb'
                        pos_dict['mood'] = pos[0]
                        if pos[1] == 'act':
                            pos_dict['voice'] = pos[1]
                            if pos[2] in ('1st', '2nd', '3rd'):
                                pos_dict['person'] = pos[2]
                                if pos[3] in ('sg', 'pl'):
                                    pos_dict['number'] = pos[3]
                                    word_dict[pos_iterator] = pos_dict
                                    perseus_pos_list.append(word_dict)
                                    perseus_pos_dict['perseus_pos'] = \
                                        perseus_pos_list
                                    headword_dict[headword] = perseus_pos_dict
                            else:
                                pass
                        else:
                            pass
                    elif pos[0] == 'nu_movable':
                        pos_dict['type'] = 'conj'
                        # only 1: sin; conjunction, right?
                        pos_dict['case'] = pos[1]
                    else:
                        pass
        try:
            with open(self.cltk_latin_pos_dict_path, 'w') as new_file:
                pprint(headword_dict, stream=new_file)
                logging.info('Successfully wrote Latin POS file at %s',
                             self.cltk_latin_pos_dict_path)
        except IOError:
            logging.error('Failed to write Latin POS file at %s',
                          self.cltk_latin_pos_dict_path)
