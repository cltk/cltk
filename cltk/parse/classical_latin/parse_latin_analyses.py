latin_analyses_dict = {}
with open('./latin-analyses.txt') as file_opened:
    string_raw = file_opened.read()
    string_rows = string_raw.splitlines()
    for row in string_rows[:10]:
        print(row)
