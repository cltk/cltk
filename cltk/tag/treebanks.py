

def set_path(dicts, keys, v):
    """ Helper function for modifying nested dictionaries

    :param dicts: dict: the given dictionary
    :param keys: list str: path to added value
    :param v: str: value to be added

    Example:
        >>> d = dicts()

        >>> set_path(d, ['a', 'b', 'c'],  'd')

        >>> d
        {'a': {'b': {'c': ['d']}}}

        In case of duplicate paths, the additional value will
        be added to the leaf node rather than simply replace it:

        >>> set_path(d, ['a', 'b', 'c'],  'e')
        
        >>> d
        {'a': {'b': {'c': ['d', 'e']}}}
    """
    for key in keys[:-1]:
        dicts = dicts.setdefault(key, dict())
    dicts = dicts.setdefault(keys[-1], list())
    dicts.append(v)


def get_paths(src):
    """ Generates root-to-leaf paths, given a treebank in string format. Note that
    get_path is an iterator and does not return all the paths simultaneously.

    :param src: str: treebank

    Examples:
        >>> st = "((IP-MAT-SPE (' ') (INTJ Yes) (, ,) (' ') (IP-MAT-PRN (NP-SBJ (PRO he)) (VBD seyde)) (, ,) (' ') (NP-SBJ (PRO I)) (MD shall)	(VB promyse) (NP-OB2 (PRO you)) (IP-INF (TO to)	(VB fullfylle) (NP-OB1 (PRO$ youre) (N desyre))) (. .) (' '))"

        Get the sixth generated path:

        >>> list(get_paths(st))[5]
        ['IP-MAT-SPE', 'IP-MAT-PRN', 'VBD', 'seyde']
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
    """Returns the corresponding tree of the treebank, in the form of
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
