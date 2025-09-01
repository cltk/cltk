"""Stack module

Includes code written by 'Arabtechies', 'Arabeyes', 'Taha Zerrouki'.
"""

__author__ = ["Taha Zerrouki taha.zerrouki@gmail.com"]
__license__ = "GPL"


class Stack:
    """
    Stack class
    """

    def __init__(self, text=""):
        """
        create a stack
        """
        self.items = list(text)

    def push(self, item):
        """
        puch an item into the stack
        @param item: pushed item
        @type item : mixed
        @return : None
        @rtype: None
        """
        self.items.append(item)

    def pop(self):
        """
        pop an item from the stack
        @return : poped item
        @rtype: mixed
        """
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def is_empty(self):
        """
        test if the stack is empty
        @return : True or False
        @rtype: boolean
        """
        return self.items == []
