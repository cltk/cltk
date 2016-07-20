from cltk.corpus.punjabi.alphabet import *
def punToEnglish_number(number):
    '''
        Thee punToEnglish_number function will take a string num which is\
        the number written in punjabi, like ੧੨੩, this is 123, the function\
        will convert it to 123 and return the output as 123 of type int
    '''
    output = 0 #This is a simple logic, here we go to each digit and check the number and compare its index with DIGITS list in alphabet.py
    for num in number:
        output = 10 * output + DIGITS.index(num)
    return output

def englishToPun_number(number):
    '''
        This function converts the normal english number to the punjabi \
        number with punjabi digits, its input will be an integer of type \
        int, and output will be a string.
    '''
    output = ''
    number = list(str(number))
    for digit in number:
        output += DIGITS[int(digit)]
    return output

if __name__ == '__main__':
    print (englishToPun_number(123))
