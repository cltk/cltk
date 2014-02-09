import re

latin_analyses_dict = {}
with open('./latin-analyses.txt') as file_opened:
    string_raw = file_opened.read()
    string_rows = string_raw.splitlines()
    for row in string_rows[39000:39110]:
        #print(row)
        reg_headword = re.compile('\w+')
        headword = reg_headword.findall(row)[0]
        print(headword)
        reg_bracket = re.compile('\{.*?\}')
        def_brackets = reg_bracket.findall(row)
        for bracket in def_brackets:
            print(bracket)
            reg_digits = re.compile('\d*')
            big_number = reg_digits.findall(bracket)[1]
            little_number = reg_digits.findall(bracket)[3]
            print(big_number)
            print(little_number)
            reg_inflection = re.compile('[a-zA-Z0-9_\,\-]*')
            print(reg_inflection.findall(bracket)[5])
