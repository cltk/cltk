import os
import re

root = os.path.abspath('./')
originals = os.path.join(root,'originals/')

'''
try:
    os.remove('../training_sentences.txt')
except:
    pass
'''
'''
files = os.listdir(originals)
training_set = ''
word_count = 0
for file in files:
    original_path = os.path.join(originals, file)
    with open(original_path) as f:
        #print(file)
        read = f.read()
        line_breaks = re.sub(r'([a-z]+)(\.|;|!|\?|:)\s([\w]+)', r'\1\2\n\3', read)
        no_section_num = re.sub(r'\[.+\]', r'', line_breaks)
        no_digits = re.sub(r'\d', r'', no_section_num)
        no_file_data_1 = re.sub(r'The Latin Library|The Classics Page|', r'', no_digits)
        no_file_data_2 = re.sub(r'Cicero|\: In Catilinam .*|In Catilinam .*|ORATIO.*', r'', no_file_data_1)
        #no_file_data_3 = re.sub(r'PRO A.*', r'uuuuuuuu', no_file_data_2)
        no_roman_nums = re.sub('.*[I|V|IV|X]\. ', '', no_file_data_2)
        no_double_end_ns = re.sub(r'\n\s*', '\n', no_roman_nums)
        no_double_start_ns = re.sub(r'\s*\n', '\n', no_double_end_ns)
        no_ascii_junk = re.sub(r'@|#|\$|%|\^|&|\*', '', no_double_start_ns)
        unbreak_comma_lines = re.sub(r',\s?\n', ', ', no_ascii_junk)
        unbreak_space_lines_1 = re.sub(r'([a-z]{1})\n([a-z]{1})', r'\1 \2', unbreak_comma_lines)
        unbreak_space_lines_2 = re.sub(r'([a-z])\n([a-z])', '\1 \2', unbreak_space_lines_1)
        rm_double_periods = re.sub(r'\.\.', '', unbreak_space_lines_2)
        rm_single_colon = re.sub(r'^:', '', rm_double_periods)
        no_double_end_ns_2 = re.sub(r'\n\n', r'\n', rm_single_colon)#works?
        print(no_double_end_ns_2)
        word_count += len(no_double_end_ns_2.split(' '))
        with open('../training_sentences_cat2.txt', 'a') as f:
            f.write(no_double_end_ns_2)
print(word_count)
'''
with open('cat4.txt') as f:
    read = f.read()
line_breaks = re.sub(r'([a-z]+)(\.|;|!|\?|:)\s([\w]+)', r'\1\2\n\3', read)
no_section_num = re.sub(r'\[.+\]', r'', line_breaks)
no_digits = re.sub(r'\d', r'', no_section_num)
no_file_data_1 = re.sub(r'The Latin Library|The Classics Page|', r'', no_digits)
no_file_data_2 = re.sub(r'Cicero|\: In Catilinam .*|In Catilinam .*|ORATIO.*', r'', no_file_data_1)
#no_file_data_3 = re.sub(r'PRO A.*', r'uuuuuuuu', no_file_data_2)
no_roman_nums = re.sub('.*[I|V|IV|X]\. ', '', no_file_data_2)
no_double_end_ns = re.sub(r'\n\s*', '\n', no_roman_nums)
no_double_start_ns = re.sub(r'\s*\n', '\n', no_double_end_ns)
no_ascii_junk = re.sub(r'@|#|\$|%|\^|&|\*', '', no_double_start_ns)
unbreak_comma_lines = re.sub(r',\s?\n', ', ', no_ascii_junk)
unbreak_space_lines_1 = re.sub(r'([a-z]{1})\n([a-z]{1})', r'\1 \2', unbreak_comma_lines)
unbreak_space_lines_2 = re.sub(r'([a-z])\n([a-z])', '\1 \2', unbreak_space_lines_1)
rm_double_periods = re.sub(r'\.\.', '', unbreak_space_lines_2)
rm_single_colon = re.sub(r'^:', '', rm_double_periods)
no_double_end_ns_2 = re.sub(r'\n\n', r'\n', rm_single_colon)#works?
print(no_double_end_ns_2)
#word_count += len(no_double_end_ns_2.split(' '))
with open('training_sentences_cat4.txt', 'a') as f:
    f.write(no_double_end_ns_2)
