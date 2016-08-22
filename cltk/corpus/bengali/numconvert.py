"""This module contains functions relating to numbers in Bengali."""

from cltk.corpus.bengali.alphabet import DIGITS
def bengaliToEnglish_number(number):

    output = 0 
    for num in number:
        output = 10 * output + DIGITS.index(num)
    return output


def englishToBengali_number(number):
    """This function converts the english numbers to the bengali
    number with bengali digits"""
    output = ''
    number = list(str(number))
    for digit in number:
        output += DIGITS[int(digit)]
    return output
