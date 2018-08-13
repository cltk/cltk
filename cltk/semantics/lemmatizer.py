'''Use the unsupervised language model created by frequency.py in order to lemmatize
Latin words. Picking the most common lemma, as in this module tests out at > 90% accurate.
'''
# the list of punctuation is used to identify non-word tokens in the test corpus.
punctuation_list = ['!', ';', ':', '?', '-', '–', '&', '*', '(', ')', '[', ']', ',', '"', '\'']

def frequency_lemmatize(target):
    '''Use the unsupervised count of lemma frequencies generated by read_files_count()
    to assign probabilities in the case of an ambiguous lemmatization.
    parameters
    ----------
    target: a token to be lemmatized
    results
    -------
    a list of tuples of the form [(lemma, probability)]
    '''
    if target in punctuation_list:
        lemmalist = [('punc', 1)]
        return lemmalist
    if target == 'ne':
        lemmalist = [('ne', 1)]
        return lemmalist
    lemmalist = lemmatizer.lookup([target])
    lemmas = lemmatizer.isolate(lemmalist)
    if len(lemmas) > 1:
        all_lemmas_total = sum([COUNT_LIBRARY[l] for l in lemmas])
        try:
            lemmalist = [(l, (COUNT_LIBRARY[l] / all_lemmas_total)) for l in lemmas]
        except ZeroDivisionError:
            print([(COUNT_LIBRARY[l], l) for l in lemmas])
        return lemmalist
    else:
        lemmalist = []
        lemmaobj = (lemmas[0], 1)
        lemmalist.append(lemmaobj)
        return lemmalist


def test_count_library(token_list, lemma_list):
    '''Test the ability of frequency_lemmatize(), (which uses the COUNT_LIBRARY dictionary,
    to predict the most likely lemmatization in ambiguous cases. Punctuation is 
    automatically counted as correct, because the 'punc' lemmatization usage is inconsistent
    in the test corpus.
    dependencies
    ------------
    itemgetter class from operator package
    parameters
    ----------
    token_list: a list of tokens
    lemma_list: a list of corresponding 'correct' lemmatizaitons
    results
    -------
    prints four numbers: the number of correctly assigned lemmas in ambiguous cases;
    the number of ambiguous cases in total; the number of tokens analyzed; and a
    decimal between 0 and 1 representing the proportion of correct lemmatizations.
    return
    ------
    a list object containing all incorrect lemmatizations for analysis. Format:
    [(token, answer_given, correct_answer), (token...)]

    NOTE: Initial tests show roughly 91% accuracy, identification of punctuation included.
    '''
    trials = 0
    correct = 0
    errors = []
    for position in range(0, (len(token_list)-1)):
        lemmalist = frequency_lemmatize(token_list[position])
        lemma = max(lemmalist,key=itemgetter(1))
        if len(lemmalist) > 1:
            trials = trials + 1
            if lemma[0] == lemma_list[position] or lemma[0] == 'punc':
                correct = correct + 1
            else:
                errors.append((token_list[position], lemma[0], lemma_list[position]))
    print(correct)
    print(trials)
    print(len(lemma_list))
    rate = (len(lemma_list) - trials + correct) / len(lemma_list)
    print(rate)
    return errors