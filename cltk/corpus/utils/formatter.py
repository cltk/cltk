"""Process downloaded or local corpora from one format into another.
Some formatting can happen here, or invoke language-specific formatters in
other files.

#TODO: Add generic HTML stripper
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


from cltk.corpus.greek.beta_to_unicode import Replacer
from cltk.corpus.greek.tlg_index import TLG_INDEX
from cltk.corpus.greek.tlgu import TLGU
from cltk.corpus.utils.cltk_logger import logger
import os
import re
import sys


def remove_non_ascii(input_string):
    """remove non-ascii: http://stackoverflow.com/a/1342373"""
    no_ascii = "".join(i for i in input_string if ord(i) < 128)
    return no_ascii


def cleanup_tlg_txt(tlg_str):
    """"Remove all non–Greek characters from a TLG corpus."""
    # fix beta code transliteration problems
    tlg_str = re.sub(r'ι|\+', 'ϊ', tlg_str)
    tlg_str = re.sub(r'ί\+', 'ΐ', tlg_str)
    tlg_str = re.sub(r'\\.', '.', tlg_str)
    # fix tlg markup
    tlg_str = re.sub(r'@1 \{1.+?\}1 @', '', tlg_str)  # rm book titles
    tlg_str = re.sub(r'\[.+?\]', '', tlg_str)  # rm words in square brackets
    tlg_str = re.sub(r'[0-9]', '', tlg_str)
    tlg_str = re.sub(r'@|%|\x00', '', tlg_str)
    tlg_str = re.sub('—', ' — ', tlg_str)
    return tlg_str


def build_corpus_index(corpus, authtab_path=None):
    """Build index for TLG or PHI5. ``authtab_path`` for testing only.
    TODO: Add a test flag argument and rm authtab_path
    :param corpus:
    :return: dict
    """
    if corpus == 'tlg':
        if not authtab_path:
            authtab_path = '~/cltk_data/originals/tlg/AUTHTAB.DIR'
        slice_start = 1
        slice_end = -6
        file_name_match = 'TLG[\d].{4}'
        pattern_author_regex = '&1|&l|l$|&|1$|\x83|\[2|\]2'
    elif corpus == 'phi5':
        if not authtab_path:
            authtab_path = '~/cltk_data/originals/phi5/AUTHTAB.DIR'
        slice_start = 1
        slice_end = -21
        file_name_match = 'LAT[\d].{4}'
        pattern_author_regex = '&1|&l|l$|&|1$|\x83'
    else:
        logger.warning("Corpus %s not available. Choose from 'tlg' or 'phi5'." % corpus)
        sys.exit(1)
    index_path = os.path.expanduser(authtab_path)
    if not os.path.isfile(index_path):
        logger.info("Failed to locate original %s index at '%s'. Please import first." % (corpus, index_path))
        sys.exit(1)
    with open(index_path, 'rb') as f:
        r = f.read()
    index_all = r.decode('latin-1').split('\xff')[slice_start:slice_end]
    index = [x for x in index_all if x]
    file_author = {}
    for x in index:
        # file name
        pattern_file = re.compile(file_name_match)
        m = pattern_file.match(x)
        file_name = m.group()[:-1]# + '.TXT'

        # author name
        author_name = pattern_file.split(x)[-1]
        pattern_author = re.compile(pattern_author_regex)
        author_name = pattern_author.sub('', author_name)
        pattern_comma = re.compile('\x80')
        author_name = pattern_comma.sub(', ', author_name)
        file_author[file_name] = author_name

    return file_author

def make_tlg_work_dict(author_dict):
    """ Lots to do here still. Pare characters around formats and clean all junk characters.
    Also find why returning only 1777; find rejected authors -- prob at a .split().
    :param author_dict:
    :return:
    """
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)

    final_dict = {}
    for file, author in file_index.items():
        a_id = {'id:': file[:-4]}
        idt_file = file[:-4] + '.IDT'
        author_index_path = os.path.join(orig_dir_path, idt_file)
        with open(author_index_path, 'rb') as a_ind_f:
            a_ind = a_ind_f.read()
        lat_list = a_ind.decode('latin-1').split('ÿ')
        ascii_list = [remove_non_ascii(x) for x in lat_list]

        works_list = []
        author_works = {}
        for possible_title in ascii_list:
            title_parts = possible_title.split('\x10', maxsplit=1)
            title_parts = [x for x in title_parts if x]
            for part in title_parts:
                try:
                    title_format = part.split('\x11', maxsplit=1)
                    title = title_format[0]
                    format = title_format[1]
                    author_works[title] = format
                    works_list.append(author_works)
                except:
                    pass
        author_vals = {'works': works_list, 'id': file[:-4]}
        final_dict[author] = author_vals
    #print(len(final_dict))  # 1777 this is missing ~100 files; find why

    return final_dict


def make_tlg_work_dict2(author_dict):

    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)

    final_dict = {}
    for file, author in file_index.items():
        works = []
        idt_file = file[:-4] + '.IDT'
        author_index_path = os.path.join(orig_dir_path, idt_file)
        with open(author_index_path, 'rb') as a_ind_f:
            a_ind = a_ind_f.read()
        lat_list = a_ind.decode('latin-1').split('ÿ')
        ascii_list = [remove_non_ascii(x) for x in lat_list]
        for possible_title in ascii_list:
            title_parts = possible_title.split('\x10', maxsplit=1)
            title_parts = [x for x in title_parts if x]
            for part in title_parts:
                title_format = part.split('\x11', maxsplit=1)
                if len(title_format) == 2:  # Note: nothing with len(title_format) > 2
                    work_title = title_format[0]
                    work_format = title_format[1]

                    # clean work title
                    work_title = remove_non_ascii(work_title)
                    work_title = work_title.replace('	', '').strip()
                    work_title = work_title

                    # clean format info
    return final_dict


def bad_idts():
    l = ['TLG2212.TXT', 'TLG2466.TXT', 'TLG0288.TXT', 'TLG1225.TXT', 'TLG4347.TXT', 'TLG1917.TXT', 'TLG1843.TXT', 'TLG4346.TXT', 'TLG1263.TXT', 'TLG1318.TXT', 'TLG0413.TXT', 'TLG1123.TXT', 'TLG0635.TXT', 'TLG2319.TXT', 'TLG1326.TXT', 'TLG0595.TXT', 'TLG2186.TXT', 'TLG9020.TXT', 'TLG1324.TXT', 'TLG4391.TXT', 'TLG0613.TXT', 'TLG2482.TXT', 'TLG2314.TXT', 'TLG4344.TXT', 'TLG2587.TXT', 'TLG1941.TXT', 'TLG0069.TXT', 'TLG2681.TXT', 'TLG1319.TXT', 'TLG1678.TXT', 'TLG0023.TXT', 'TLG2475.TXT', 'TLG2423.TXT', 'TLG0085.TXT', 'TLG1138.TXT', 'TLG1320.TXT', 'TLG2696.TXT', 'TLG0538.TXT', 'TLG1414.TXT', 'TLG4157.TXT', 'TLG1429.TXT', 'TLG1192.TXT', 'TLG4345.TXT', 'TLG2354.TXT', 'TLG0380.TXT', 'TLG2307.TXT']
    #l = ['TLG0003.TXT']
    l = [str(x[:-4] + '.IDT') for x in l]
    #print(l)
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)

    tmp = []
    for idt_file in l:
        author_index_path = os.path.join(orig_dir_path, idt_file)
        with open(author_index_path, 'rb') as f:
            r = f.read()
        lat_list = r.decode('latin-1').split('ÿ')
        ascii_list = [remove_non_ascii(x) for x in lat_list]
        for possible_title in ascii_list:
            title_parts = possible_title.split('\x10', maxsplit=1)
            title_parts = [x for x in title_parts if x]
            for part in title_parts:
                title_format = part.split('\x11', maxsplit=1)
                if len(title_format) == 2:
                    #print('what', len(title_format), title_format)
                    tmp.append(idt_file)
                elif len(title_format) > 2:
                    print('what', len(title_format), title_format)
    print(len(set(idt_file)))


def tlgu_break_works():
    """Use the work-breaking option for TLGU.
    TODO: This should be added to ``tlgu.py`` to allow bulk corpus converting with work-breaking."""
    t = TLGU()
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)
    tlg_files = os.listdir(orig_dir_path)
    texts = [x for x in tlg_files if x.endswith('.TXT') and x.startswith('TLG')]

    for file in texts:
        orig_file_path = os.path.join(orig_dir_path, file)
        works_dir_rel = '~/cltk_data/greek/text/tlg/individual_works'
        works_dir = os.path.expanduser(works_dir_rel)
        if not os.path.isdir(works_dir):
            os.makedirs(works_dir)
        new_file_path = os.path.join(works_dir_rel, file)

        orig_file_rel = os.path.join(orig_dir_path_rel, file)
        print(orig_file_rel)
        print(new_file_path)
        t.convert(orig_file_rel, new_file_path, divide_works=True)


def find_works_in_texts(author_dict):
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)
    comp_title = re.compile('\{1(.+?)\}1')
    author_works = {}
    replacer = Replacer()
    for file, auth in author_dict.items():
        author_file_path = os.path.join(orig_dir_path, file)
        with open(author_file_path, 'rb') as auth_file:
            auth_read = auth_file.read()
        auth_read = auth_read.decode('latin-1')
        titles = comp_title.findall(auth_read)
        unicode_titles = []
        for title in titles:
            title = remove_non_ascii(title)
            unicode_title = replacer.beta_code(title)
            unicode_titles.append(unicode_title)
        titles_in_file = {'titles_in_file': unicode_titles}
        author_works[auth] = titles_in_file
        print(author_works)
        input()


# was doing something with parsing the individually divided works
''''
individual_work_dir_rel = '~/cltk_data/greek/text/tlg/individual_works/'
individual_work_dir = os.path.expanduser(individual_work_dir_rel)
individual_work = os.path.join(individual_work_dir, 'TLG0007.TXT-007.txt')
if not os.path.isfile(individual_work):
    tlgu_break_works()
for file, author in TLG_INDEX.items():
    file_base = os.path.join(individual_work_dir, file)
    print(file_base)
    input()
'''


def read_tlg_idts():
    """Read TLG IDT files from the directory. These should later be checked against the TLG_INDEX."""
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)
    return [os.path.join(orig_dir_path, x) for x in os.listdir(orig_dir_path) if x.endswith('.IDT') and x.startswith('TLG')]


def open_idt(idt_path):
    #print(idt_path)
    with open(idt_path, 'rb') as opened_idt:
        return opened_idt.read()


def cleanup_author(author_text):
    comp_clean_author = re.compile('&|\[2|\]2|1')
    author = comp_clean_author.sub('', author_text)

    # super ugly. replace name if 1 of 3 which has Greek in name
    greek_name = {'Dialexeis ($*DISSOI\\ LO/GOI)': 'Dialexeis Δισσοὶ λόγοι',
                  'Dionysius $*METAQE/MENOS Phil.': 'Dionysius Μεταθέμενος Phil.',
                  'Lexicon $AI(MWDEI=N': 'Lexicon αἱμωδεῖν'}
    if author in greek_name:
        author = greek_name[author]

    # same as above. damn ugly. replace name w/ dict value if name is one we
    # know to have a diaresis in it
    diaresis_authors = {'Danai+s vel Danai+des': 'Danaïs vel Danaïdes',
                       'Ae+tius Doxogr.': 'Aëtius Doxogr.',
                       'Aglai+s Poet. Med.': 'Aglaïs Poet. Med.',
                       'Ae+tius Med.': 'Aëtius Med.',
                       'Thebai+s': 'Thebaïs',
                       'Boi+das Phil.': 'Boïdas Phil.'
    }
    if author in diaresis_authors:
        author = diaresis_authors[author]

    return author

def match_idt_author_name(idt_binary):
    idt_text = idt_binary.decode('latin-1')
    comp_name = re.compile('&1(.+?)\x02')
    author = comp_name.findall(idt_text)
    return author[0]

def match_idt_titles(idt_binary):
    #idt_text = idt_binary.decode('latin-1')
    comp_post_name = re.compile(b'\x02')
    post_name = comp_post_name.split(idt_binary, 1)
    comp_pre_first_title = re.compile(b'\xff\x10')
    pre_first_title = comp_pre_first_title.split(post_name[1])
    titles_format = pre_first_title[1:]  #! This is good! Each element of the list is a work + its index method
    #print(len(titles))
    # for testing that I get at least 1 title for every .idt
    if len(titles_format) < 1:
        print(titles_format)  # success! A title found for every .idt
    for title_format in titles_format:
        comp_pre_format = re.compile(b'\x11')
        pre_format = comp_pre_format.split(title_format, 1)
        problem_idts = []
        try:
            title = pre_format[0]
            format = pre_format[1]

            # clean the title
            comp_clean_title = re.compile(b'\x01|\t|\n|\x0e|\x1e|\x13|\x1d|\x14|\x08|\x07|\x1b|\x10|\x0f|\x19|\x1c|\x10|\x15|\x06|\x03|\x12|\x18|\x0b|\x0c|\x17|\x16|\x1f|\x05|\x04|\x04|\x1a|\x04|\x1a|\x00|\r')
            title_clean = comp_clean_title.sub(b'', title)

            # parse and clean the format
            try:
                comp_between_format = re.compile(b'\x11')
                format_units = comp_between_format.split(format)  # tested no fewer than len() 1
                # end of format break = '\x03\x00\x00\x08' # nec?

                work_formats = []
                for format in format_units:
                    #! this is super ugly and contains redundancies
                    # the purpose: to rm enough junk in order to .decode('latin-1') w/o breaking text
                    comp_clean_format = re.compile(b'\x01|\x08|\x00|\x02|\x03|x91|\n|\x90|\x88|\xad|\n|\x94|\x88|\x9a|\t|\x96|\x88|\x98|\x0b|\x9f|\xf4|\xff|\x0c|\x83|\x02|\x7f|\x02|\xef|\x81|\xb0|\xb0|\xb2|\x04|\x07|\xd4|\x9b|\x89|\x84|\xc4|\x84|\xd8|\xe8|\xaf|\xc1|\xf5|\xec|\xe9|\x91|\xaf|\xc5|\xf0|\xe9|\xe9|\x91|\xaa|\xaf|\xc5|\xe9|\xe6|\xe9|\x91|\x85|\x80|\x95|\x82|\x93|\x9d|\x95|\x9c|\x8a|\x8b|\x93|\x9c|\x95|\xb8|\x97|\xb8|\x99|\xb9|\x9c|\x95|\x9e|\x97|\xa2|\x95|\xa5|\xa8|\r|\xb1|\xb1|\xa1|\xa3!|\xa1|\x1d|\x87|\xa6|\x86|\x1c|\xf8|\x1c|\x8f|\x1c|\x1c|\xf1|\xb5|\x8d|\xf2|\xa0|\xe1|\xf2|\xf2|\xa0|\xe5|\xac|\xac|\xe7|\xac|\xe3|\xa0|\xa3|\xe2|\x8d|\xf2|\xa0|\xe7|\xa0|\xe3|\xa0|\xf2|\xa0|\xf2|\xda|\xd5|\xfd|\xe4|\xb7|~|\xd9|\x8cd|\x06|!||\xce|\xce|\xb3|\xee|\xce|\xce|\xdb|\xb4|\xc9|\xb4|\xa9|\xc9|\xb6|\xa9|\xbd|\xf3|\xed|\xcd|\xbe|\xcf|\x92|\xab|\xc0|\xdb|\x92|\xf6|\xbc|\xb3|\xb6|\xd3|\xc7|\x10|\xb3|\xbb|\xc6E|\xb4|\xb3|\xbb|\xa9|\xc8N|\xd0|\xdb|\xa7|\xc6A|\xb4|\xb3|\xb3|\xb6|\xb3|\xc9|\xbf|\x92|\x1f|\xba|\xae|\xc2|\x8c|\x8e|\x1f|\xee|\x1f|\xb6|\xb4|\xce|\x92|\xa4|\xa7|\x92|\x8c|\xb4|\xbb|\xc3|\xc2|\x8c|\xcb|\xce|\xd1|\xb3\xb4|\x92|S\xb4|\xb3V\xd7|\xdb|\xd2|\xb4|\xbf|\x8c|\xa4|=|\xf3|\xee|\x8c|\xf3|\xf6|\x8e|\x8ed|\xb6|\x8cf|\xb4|\x8cg|\xb3|\x92|\xbf|\xb6|\xb4|\xf6|\xf6|@|\xb6W|\xb6|\xf6|\xa4|\xee|\xa4s|\x92|\xc2|\x92|\xd0|\xee|\xb3|\x8e|\xbc|\\|\xb3|\x8c|\x92|\x92|\xa4|\xa9|\xab|\xa7|\x8e|\xb4|\xbb|\xbe|\xc0|\xa4|\xc3|\xc8|\xca|\x92|\xcc|\xcf|\x92|\xd1|\xa4|\xd6|\xdb|\xde|\xe0|\xee|\xf3|\xf7|\xa7|\xfa|\x8e|\xfc|\x92|\x8e|\xb3|\xbc|\xc3|\xb3|\xcf|\xc3|\xb4v|\xb3|N\x92NTO|EEG\xc7GSN|9\xc09:\xb6|00|8\xbf8N9|\x92|\xa7|\x8c|\x8e|\x8c|\x8e|\x8c|\xab|\xaeM8|\xb4|\x1b|\xbc|\xc8|\x1b|\xc6|\xb3|\x19|\xa4|\x19G|\x1b|\x17|\xa4|\x17b|\x19|\xfb|\x92|\xa7|\x92|\x92|\x8c|\xa4|\xa9|\xab|\x8e|\xb3|\xfbH|\x17|\xb3|\xc7|\xb3|\xcd|\x8c|\x92|\x8e|^|\xb6|\xa4|\x92|\xa4T|\x92W|\xb4|}|\x8e|\xbdl|\xb3|\xa7|\xbd|\x8cyM|\x92|\xa9|\xa9|\xa7|\xbf|\xd0|\xde|\xbe|\x92Zy|\xc6|\x10|\x92|\x8e|\xa7|\x10|"|\xae|\xb3|\xb6|\x05|\xae|\xed|\xf3|\xee|\xfa|\x8e|\xb3|\xed|\xbd|\xce|\xd0|\xea|\x8e|\x92|\x8e|\x8c|\x12|\x14|\x8c|\x13|\x8c|\x92|\x923|\x8c|\(|\)|\xcf|\x8c| \xb4|\x1eX |\x1a|\x8e|\xa9M|\x1e|\x1a|\xb4|\xcc|\xbf|\xd0|\x8c|\x8e|\x8e|\xab|\x92|\xa9|\xa7|\x13E|\x13|\x12|\xfb')
                    format = comp_clean_format.sub(b'', format)

                    format_2 = format.decode('latin-1')

                    # the following is a more direct approach to cleaning up
                    # problem formatting
                    comp_line = re.compile(r'line.*')
                    format_2 = comp_line.sub('line', format_2)

                    comp_line = re.compile(r'Line.*')
                    format_2 = comp_line.sub('line', format_2)

                    comp_line = re.compile(r'Volume-Jacoby.*')
                    format_2 = comp_line.sub('line', format_2)

                    comp_line = re.compile(r'Lexicon.*')
                    format_2 = comp_line.sub('Lexicon', format_2)

                    comp_line = re.compile(r'%Argumentum-dramatis personae-scholion')
                    format_2 = comp_line.sub('Argumentum-dramatis personae-scholion', format_2)

                    comp_line = re.compile(r'\x0eStephanus page')
                    format_2 = comp_line.sub('Stephanus page', format_2)

                    #\x12line
                    comp_line = re.compile(r'\x12line')
                    format_2 = comp_line.sub('line', format_2)

                    #\x10line
                    comp_line = re.compile(r'\x10line')
                    format_2 = comp_line.sub('line', format_2)

                    #\x10Alphabetic entry
                    comp_line = re.compile(r'\x10Alphabetic entry')
                    format_2 = comp_line.sub('Alphabetic entry', format_2)


                    #\x05Entry
                    comp_line = re.compile(r'\x05Entry')
                    format_2 = comp_line.sub('Entry', format_2)


                    #\x05entry
                    comp_line = re.compile(r'\x05entry')
                    format_2 = comp_line.sub('entry', format_2)


                    #\x12column or fragment
                    comp_line = re.compile(r'\x12column or fragment')
                    format_2 = comp_line.sub('column or fragment', format_2)



                    #\x10Kaibel paragraph
                    comp_line = re.compile(r'\x10Kaibel paragraph')
                    format_2 = comp_line.sub('Kaibel paragraph', format_2)



                    #\x18hypothesis-verse of play
                    comp_line = re.compile(r'\x18hypothesis-verse of play')
                    format_2 = comp_line.sub('hypothesis-verse of play', format_2)

                    #\x19Hypothesis-apologia-cento
                    comp_line = re.compile(r'\x19Hypothesis-apologia-cento')
                    format_2 = comp_line.sub('Hypothesis-apologia-cento', format_2)



                    #\x1bhypothesis-epigram-scholion
                    comp_line = re.compile(r'\x1bhypothesis-epigram-scholion')
                    format_2 = comp_line.sub('hypothesis-epigram-scholion', format_2)


                    #\x0fQuestion+answer
                    comp_line = re.compile(r'\x0fQuestion+answer')
                    format_2 = comp_line.sub('Question+answer', format_2)

                    #\x05Codex
                    comp_line = re.compile(r'\x05Codex')
                    format_2 = comp_line.sub('Codex', format_2)

                    #Ku+hn volume --> Kühn volume
                    comp_line = re.compile(r'Ku+hn volume')
                    format_2 = comp_line.sub('Kühn volume', format_2)

                    #\x05Idyll
                    comp_line = re.compile(r'\x05Idyll')
                    format_2 = comp_line.sub('Idyll', format_2)

                    #\x10Tome+volume+part
                    comp_line = re.compile(r'\x10Tome+volume+part')
                    format_2 = comp_line.sub('Tome+volume+part', format_2)

                    #\x05Title
                    comp_line = re.compile(r'\x05Title')
                    format_2 = comp_line.sub('Title', format_2)

                    #\x05verse
                    comp_line = re.compile(r'verse')
                    format_2 = comp_line.sub('verse', format_2)


                    #\x18Vita-argumentum-scholion
                    comp_line = re.compile(r'\x18Vita-argumentum-scholion')
                    format_2 = comp_line.sub('Vita-argumentum-scholion', format_2)

                    #$*PENTAETHRIKO/S&
                    comp_line = re.compile(r'\$*PENTAETHRIKO/S&')
                    format_2 = comp_line.sub('$*PENTAETHRIKO/S& !!! TRANSLITERATE', format_2)

                    #&1Palladius& Med.Y
                    comp_line = re.compile(r'&1Palladius& Med.Y')
                    format_2 = comp_line.sub('Palladius Med. !!! AUTHOR NOT FORMAT', format_2)

                    #\x05Psalm
                    #\x12Preisendanz number
                    #\x15Prolegomenon-scholion
                    #&1Simonides& Lyr.S
                    #\x1ePausanias book+chapter+section
                    #$*PERI\\ STA/SEWN&
                    #\x10Bekker page+line'
                    #\x05Paean
                    #\x0fBook of Odyssey
                    #$*PERI\\ METOXW=N&
                    #\x12Fragment or column
                    #\x0fFragment+column
                    #\x12Verso-recto+column
                    #$*KWMW|DOU/MENOI&
                    #&1Hesiodus& Epic.E
                    #&1Nicolaus& Hist.³
                    #\x05Folio
                    #\x12column or fragment
                    #$*SUMMAXIKO\\S A#&
                    #$*PANAQHNAI+KO/S&
                    #\x13Argumentum-scholion
                    #\x13Hypothesis-scholion
                    #\x1bhypothesis-epigram-scholion
                    #\x16Dindorf-Stephanus page

                    '''
                    #! Super horrible parsing. hopefully this only has to be done once
                    format_2.replace('\x10Alphabetic entry', 'Alphabetic entry').replace('\x05Entry', 'Entry')\
                        .replace('\x12column or fragment', 'column or fragment').replace('\x10Kaibel paragraph', 'Kaibel paragraph')\
                        .replace('\x18hypothesis-verse of play', 'hypothesis-verse of play')\
                        .replace(r'\x19Hypothesis-apologia-cento', 'Hypothesis-apologia-cento')\
                        .replace('\x1bhypothesis-epigram-scholion', 'hypothesis-epigram-scholion')\
                        .replace('\x12line', 'line').replace('\x0fQuestion+answer', 'Question+answer')\
                        .replace('\x05Codex', 'Codex').replace('Ku+hn volume', 'Kühn volume')\
                        .replace('\x05Idyll', 'Idyll').replace('\x10Tome+volume+part', 'Tome+volume+part')\
                        .replace('\x05Title', 'Title').replace('\x05verse', 'verse')\
                        .replace('\x18Vita-argumentum-scholion', 'Vita-argumentum-scholion')\
                        .replace('$*PENTAETHRIKO/S&', '$*PENTAETHRIKO/S& !!!! TRANSLITERATE')\
                        .replace('&1Palladius& Med.Y', 'Palladius& Med. !!! THIS IS A NAME NOT FORMAT')\
                        .replace('\x05Psalm', 'Psalm').replace('\x12Preisendanz number', 'Preisendanz number')\
                        .replace('\x15Prolegomenon-scholion', 'Prolegomenon-scholion')\
                        .replace('&1Simonides& Lyr.S', 'Simonides& Lyr. !!! THIS IS A NAME NOT FORMAT')\
                        .replace('\x1ePausanias book+chapter+section', 'Pausanias book+chapter+section !!! CHECK FORMAT TYPE')\
                        .replace('$*PERI\\ STA/SEWN&', '$*PERI\\ STA/SEWN& !!! TRANSLITERATE')\
                        .replace('\x10Bekker page+line', 'Bekker page+line')\
                        .replace('\x05Paean', 'Paean').replace('\x0fBook of Odyssey', 'Book of Odyssey')\
                        .replace('$*PERI\\ METOXW=N&', '$*PERI\\ METOXW=N& !!! TRANSLITERATE')\
                        .replace('\x12Fragment or column', 'Fragment or column').replace('\x0fFragment+column', 'Fragment+column')\
                        .replace('\x12Verso-recto+column', 'Verso-recto+column')\
                        .replace('\x12column or fragment', 'column or fragment').replace('$*SUMMAXIKO\\S A#&', '$*SUMMAXIKO\\S A#& !!! TRANSLITERATE')\
                        .replace('$*PANAQHNAI+KO/S&', '$*PANAQHNAI+KO/S& !!! TRANSLITERATE')\
                        .replace('\x13Argumentum-scholion', 'Argumentum-scholion').replace('\x13Hypothesis-scholion', 'Hypothesis-scholion')\
                        .replace('\x1bhypothesis-epigram-scholion', 'hypothesis-epigram-scholion')\
                        .replace('\x16Dindorf-Stephanus page', 'Dindorf-Stephanus page')#.replace('', '').replace('', '').replace('', '').replace('', '').replace('', '').replace('', '').replace('', '')
                    '''



                    #print(format_2)

                    work_formats.append(format_2)
                try:
                    print(work_formats)
                except:
                    pass

                #input()


            except:
                print('ERROR!!', format) #! check for errrors. None so far.
        except:
            problem_idts.append(title_format)  # these have index error on pre_format[1]
            #continue
    #input()
    return ''

def author_names_from_idts():
    """There are 1823 TLG*.IDT files, but the authors in them are only 1773
    unique. That is 50 IDT files give an author name identical to one in
    another file. OIPOPOI!
    """
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)
    #return [os.path.join(orig_dir_path, x) for x in os.listdir(orig_dir_path) if x.endswith('.IDT') and x.startswith('TLG')]

    author_dict = {}

    for tlg_id, dir_name in TLG_INDEX.items():
        idt_path = os.path.join(orig_dir_path, tlg_id + '.IDT')

        idt_binary = open_idt(idt_path)
        author_ugly = match_idt_author_name(idt_binary)
        author = cleanup_author(author_ugly)

        author_names = {'name_idt': author,
                        'name_authtab': dir_name
                        }
        author_dict[tlg_id] = author_names

    # here add parsing of works in .idt file
    for tlg_id, dir_name in TLG_INDEX.items():
        idt_path = os.path.join(orig_dir_path, tlg_id + '.IDT')
        idt_binary = open_idt(idt_path)
        titles_ugly = match_idt_titles(idt_binary)


    return author_dict


if __name__ == '__main__':
    author_dict = author_names_from_idts()

    '''
    with open('cltk/corpus/greek/tlg_master_index.py', 'w') as f:
        f.write('TLG_MASTER_INDEX = ' + str(author_dict))
    '''

