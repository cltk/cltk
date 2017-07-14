#!/usr/bin/python
# -*- coding=utf-8 -*-
"""
Stack module
@author: Taha Zerrouki
@contact: taha dot zerrouki at gmail dot com
@copyright: Arabtechies,  Arabeyes,   Taha Zerrouki
@license: GPL
@date:2010/03/01
@version: 0.1
"""
__author__ = 'Lakhdar Benzahia, <lakhdar.benzahia@gmail.com>'
__reviewers__ = ['Taha Zerrouki taha.zerrouki@gmail.com', 'Kyle P. Johnson <kyle@kyle-p-johnson.com>']

class Stack :
    """
	Stack class
    """
    def __init__(self, text="") :
        """
        create a stack
        """
        self.items = list(text)

    def push(self, item) :
        """
        puch an item into the stack
        @param item: pushed item
        @type item : mixed
        @return : None
        @rtype: None
        """
        self.items.append(item)

    def pop(self) :
        """
        pop an item from the stack
        @return : poped item
        @rtype: mixed
        """
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def is_empty(self) :
        """
        test if the stack is empty
        @return : True or False
        @rtype: boolean
        """
        return (self.items == [])
