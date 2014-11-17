"""Wrapper for `tlgu` command line utility

Use methods in importer.py like so:

from cltk.corpus.importer import download_file
from cltk.corpus.importer import save_untar

downloaded_object = download_file(url, corpus_name)
originals_dir, unpack_dir = make_dirs(language, corpus_type, corpus_name)
save_untar(url, downloaded_object, originals_dir, unpack_dir, corpus_name)

"""

__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'


import os.path
import requests
import itertools
import requests
from requests_toolbelt import SSLAdapter
import ssl
import subprocess

from cltk.corpus import CLTK_DATA_DIR
#from cltk.cltk.data import cltk_data

ARGS = {
    'book_breaks': '-b',
    'page_breaks': '-p',
    'latin_text': '-r',
    'level_1': '-v',
    'level_2': '-w',
    'level_3': '-x',
    'level_4': '-y',
    'level_5': '-z',
    'line_tab': '-B',
    'higher_levels': '-X',
    'lower_levels': '-Y',
    'no_spaces': '-N',
    'citation_debug': '-C',
    'code_debug': '-S',
    'verbose': '-V',
    'split_works': '-W'
}


class TLGU(object):
    def __init__(self):
        self.name = 'tlgu'
        self.url = 'https://github.com/cltk/tlgu/blob/master/tlgu-1.6.zip?raw=true'

    @property
    def exe(self):
        query = 'kMDItemFSName=tlgu&&kMDItemContentType=public.unix-executable'
        find_exe = ['mdfind', query]
        c_path = subprocess.check_output(find_exe)
        exe_paths = c_path.split(b'\n')
        if len(exe_paths) > 0:
            if isinstance(exe_paths[0], bytes):
                return exe_paths[0].decode('utf-8')
            if isinstance(exe_paths[0], str):
                return exe_paths[0]
        else:
            self.compile()
            return self.exe

    def compile(self):
        if subprocess.check_output(['which', 'gcc']):
            find_c = ['mdfind', 'kMDItemFSName=tlgu.c']
            c_path = subprocess.check_output(find_c)
            c_path = c_path.strip()
            if c_path:
                # If running in a Virtual Env,
                # it should create the executable file
                # at `[venv]/lib/python3.4/site-packages/cltk/tlgu`
                compile_c = ['gcc', c_path, '-o', 'tlgu']
                subprocess.check_output(compile_c)
            else:
                self.download()
                self.compile()
        else:
            return 'Cannot compile `tlgu` without `gcc`!'

    def convert(self, input_path, markup='plain',
                break_lines=False, divide_works=False,
                output_path=None, opts=[]):
        options = [self.exe]
        # Ensure there are no duplicate options
        poss_opts = list()
        poss_opts.extend(self._language(output_path))
        poss_opts.extend(self._markup(markup))
        poss_opts.extend(self._break_lines(break_lines))
        poss_opts.extend(self._divide_works(divide_works))
        if opts != []:
            poss_opts.extend(opts)
        options.extend(list(set(poss_opts)))
        # Add input and output paths
        paths = [input_path]
        if output_path:
            cltk_data.resolve_path(os.path.dirname(output_path))
            paths = [input_path, output_path]
        options.extend(paths)

        p = subprocess.Popen(options,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        output, err = p.communicate()
        return output.decode('utf-8')
        #return output

    def _language(self, path):
        if path.endswith('.txt'):
            if 'tlg' in path:
                return []
            else:
                return ['-r']
        else:
            return ['-r']

    def _markup(self, markup):
        if markup == 'full':
            return [v for k, v in ARGS.items()
                    if 'level_' in k]
        elif markup == 'plain':
            return []

    def _break_lines(self, break_lines):
        if break_lines is True:
            return []
        elif break_lines is False:
            return ['-N']

    def _divide_works(self, divide_works):
        if divide_works is True:
            return ['-W']
        elif divide_works is False:
            return []

    # mv download and untar logic to importer.py
    '''
    def download(self):
        path = cltk_data.resolve_path(os.path.join(cltk_data.downloads_dir,
                                                   'tlgu.zip'))
        r = requests.get(self.url)
        with open(path, "wb") as code:
            code.write(r.content)
        #Unpack to temp dir
        #Compile
    '''

    def _run_combination_tests(self):
        # TODO: fix paths
        inp = '/Users/smargh/Code/cltk/cltk_data/originals/phi5/LAT1212.TXT'
        out = '/Users/smargh/Code/GitHub/tlgu/tlgu_tests/opts_{}'
        for l in range(len(ARGS.values())):
            i = itertools.combinations(ARGS.values(), l)
            for arg in list(i):
                args = list(arg)
                latin_args = args + ['-r']
                out_path = out.format(''.join(args).replace('-', ''))
                self.run(inp, out_path, opts=latin_args)

# alias
tlgu = TLGU()

if __name__ == '__main__':
    """
    p = '/Users/smargh/Code/cltk/cltk_data/originals/tlg/LSTSCDCN.DIR'
    o = '/Users/smargh/Code/cltk/cltk_data/tlg_LSTSCDCN.txt'
    out = TLGU(p).convert('plain', True, False, output_path=o)
    print(out.encode('utf-8'))
    """

    print(tlgu.compile())
