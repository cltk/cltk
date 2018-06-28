
from tesserae.utils import TessFile

import pprint
pp = pprint.PrettyPrinter(indent=4)

skip_library = dict()

#open a new file
tokens = NewFile(v)
stop = 0
while stop!=1:
    #the target should be five away from the end of the file, until the end
    target = len(tokens) - 6
    targettoken = tokens[target]
    #grab all the other tokens but the target
    contexttokens = [x for i,x in enumerate(tokens) if i!=target]
    #add this context to the skipgram map
    Skipgram(targettoken, contexttokens)
    try:
        tokens.append(next(v))
        if len(tokens) > 11:
            tokens.pop(0)
    except StopIteration:
        # we have reached EOF. Loop through until the last token is done then quit
        # when this happens, the token list should have 11 indices, and the 'target' index will be the sixth (i.e. tokens[5])
        # pop the first index off, leaving 10 indices and making the sixth index (previously the seventh) the new target.
        while len(tokens) > 5:
            tokens.pop(0)
            # as long as there are six or more indexes, make the target the sixth index.
            if len(tokens) > 6:
                target = 5
            # if there are exactly six indexes, then the target is the last index.
            else:
                target = len(tokens) - 1
            targettoken = tokens[target]
            #grab all the other tokens but the target
            contexttokens = [x for i,x in enumerate(tokens) if i!=target]
            #add this context to the skipgram map
            Skipgram(targettoken, contexttokens)
        stop = 1



def Skipgram(t, c):
    '''Builds a complex data structure that will contain the 'average context' for each type in the corpus.
    param t: the token in question
    param c: the context tokens
    global skip_library: a dictionary whose keys are types and whose values are dictionaries; 
    in turn their keys are context types and values are incremented counts.
    '''
    global skip_library
    if t not in skip_library:
        skip_library[t] = defaultdict(int)
    for w in c:
        skip_library[t][w] += 1

def NewFile(v):
    '''Takes an iterator object for the file being read.
    Reads in the first six tokens and returns them'''
    tokens = []
    for i in range(0,6):
        tokens.append(next(v))
    return tokens

