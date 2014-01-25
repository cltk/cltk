import re
from latin import stopwords

#RegexpReplacer should be removed
#from examples, then from here
class RegexpReplacer(object):
    def __init__(self, patterns=stopwords):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
        return s

class StopReplacer(object):
    def __init__(self, patterns=stopwords):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
        return s

