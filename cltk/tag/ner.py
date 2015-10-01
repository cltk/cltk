"""Named entity recognition (NER)."""

from cltk.corpus.utils.importer import CorpusImporter
from nltk.tokenize.punkt import PunktLanguageVars
import os

NER_DICT = {'greek': '~/cltk_data/greek/model/greek_models_cltk/ner/proper_names.txt',
            'latin': '~/cltk_data/latin/model/latin_models_cltk/ner/proper_names.txt'}


def _check_latest_data(lang):
    """Check for presence of proper names dir, clone if not."""

    assert lang in NER_DICT.keys(), \
        'Invalid language. Choose from: {}'.format(', '.join(NER_DICT.keys()))

    ner_file_path = os.path.expanduser(NER_DICT[lang])

    if not os.path.isfile(ner_file_path):
        corpus_importer = CorpusImporter(lang)
        corpus_importer.import_corpus('{}_models_cltk'.format(lang))


def tag_ner(lang, input_text, output_type=list):
    """Run NER for chosen language.

    Choosing output_type=list, returns a list of tuples:
    >>> tag_ner('latin', input_text=text_str, output_type=list)
    >>> [('ut',), ('Venus', 'Entity'), (',',), ('ut',), ('Sirius', 'Entity'),
    (',',), ('ut',), ('Spica', 'Entity')]
    """

    _check_latest_data(lang)

    assert lang in NER_DICT.keys(), \
        'Invalid language. Choose from: {}'.format(', '.join(NER_DICT.keys()))
    types = [str, list]
    assert type(input_text) in types, 'Input must be: {}.'.format(', '.join(types))
    assert output_type in types, 'Output must be a {}.'.format(', '.join(types))

    if type(input_text) == str:
        punkt = PunktLanguageVars()
        tokens = punkt.word_tokenize(input_text)
        new_tokens = []
        for word in tokens:
            if word.endswith('.'):
                new_tokens.append(word[:-1])
                new_tokens.append('.')
            else:
                new_tokens.append(word)
        input_text = new_tokens

    ner_file_path = os.path.expanduser(NER_DICT[lang])
    with open(ner_file_path) as file_open:
        ner_str = file_open.read()
    ner_list = ner_str.split('\n')

    ner_tuple_list = []
    for count, word_token in enumerate(input_text):
        match = False
        for ner_word in ner_list:
            # the replacer slows things down, but is necessary
            if word_token == ner_word:
                ner_tuple = (word_token, 'Entity')
                ner_tuple_list.append(ner_tuple)
                match = True
                break
        if not match:
            ner_tuple_list.append((word_token,))

    if output_type is str:
        string = ''
        for tup in ner_tuple_list:
            start_space = ' '
            final_space = ''
            # this is some mediocre string reconstitution
            # maybe not worth the effort
            if tup[0] in [',', '.', ';', ':', '?', '!']:
                start_space = ''
            if len(tup) == 2:
                string += start_space + tup[0] + '/' + tup[1] + final_space
            else:
                string += start_space + tup[0] + final_space
        return string

    return ner_tuple_list


if __name__ == "__main__":
    #from cltk.stem.latin.j_v import JVReplacer
    #input_file = '/Users/kyle/cltk_data/greek/text/tlg/plaintext/TLG0016.TXT'
    #with open(input_file) as file_open:
    #    text_str = file_open.read()

    text_str = 'τὰ Σίλαριν Σιννᾶν Κάππαρος Πρωτογενείας Διονυσιάδες τὴν'

    #jv_replacer = JVReplacer()
    #text_str = jv_replacer.replace(text_str)
    print(tag_ner('greek', input_text=text_str, output_type=list))
