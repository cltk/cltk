import re

with open('./latin-analyses.txt') as file_opened:
    string_raw = file_opened.read()
    string_rows = string_raw.splitlines()
    latin_analyses_dict = {}
    for row in string_rows[39000:39010]:
        #print(row)
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
