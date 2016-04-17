"""Example iTrans for Nurendra

In [1]: from cltk.corpus.sanskrit.itrans.unicode_transliterate import lower_case_and_replace

In [2]: lower_case_and_replace('APPLE BANANA CUCUMBER')
Out[2]: 'अpple बअnअnअ कuकumबer'
"""

from cltk.corpus.sanskrit.itrans.itrans_transliterator import FAKE_ITRANS_MAP


def lower_case_and_replace(string_input):
    """Just a test function."""
    string_lower = string_input.lower()
    string_replaced_list = []
    for char in string_lower:
        if char in FAKE_ITRANS_MAP.keys():
            new_char = FAKE_ITRANS_MAP[char]
        else:
            new_char = char
        string_replaced_list.append(new_char)

    string_replaced = ''.join(string_replaced_list)

    return string_replaced
