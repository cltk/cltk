

def set_path(dicts, keys, v):
    for key in keys[:-1]:
        dicts = dicts.setdefault(key, dict())
    dicts = dicts.setdefault(keys[-1], list())
    dicts.append(v)


def get_paths(src):

    """
    Generates root-to-leaf paths, given a treebank in string format

    :param src: str: treebank
    """
    st = list()
    tmp = ''

    for let in src:
        if let == '(':
            if tmp != '':
                st.append(tmp)
                tmp = ''

        elif let == ')':
            if tmp != '':
                st.append(tmp)
                yield st
            st = st[:-1 - (tmp != '')]
            tmp = ''

        elif let == ' ':
            if tmp != '':
                st.append(tmp)
                tmp = ''

        else:
            tmp += let


def parse_treebanks(st):
    """
    Returns the corresponding tree of the treebank, in the form of
    a nested dictionary
    :param st: str: treebank using Penn notation

    Example:
        >>> st = "((IP-MAT-SPE (' ') (INTJ Yes) (, ,) (' ') (IP-MAT-PRN (NP-SBJ (PRO he)) (VBD seyde)) (, ,) (' ') (NP-SBJ (PRO I)) (MD shall)	(VB promyse) (NP-OB2 (PRO you)) (IP-INF (TO to)	(VB fullfylle) (NP-OB1 (PRO$ youre) (N desyre))) (. .) (' '))"

        >>> tree = parse_treebanks(st)
        
        >>> tree['IP-MAT-SPE']['IP-MAT-PRN']
        {'NP-SBJ': {'PRO': ['he']}, 'VBD': ['seyde']}
    """
    d = dict()
    for path in get_paths(st):
        set_path(d, path[:-1], path[-1])
    return d

