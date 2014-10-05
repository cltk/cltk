# encoding: utf-8
"""Utility functions for working with BeautifulSoup data"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'


def tags(tag):
    l = [x.name for x in tag.contents if x.name]
    return l


def strings(tag):
    return [{x.name: x.string} for x in tag.contents
            if x.string and x.name]
