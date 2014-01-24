import re

#I need to decide whether to always lower() before this replacement
#and with main lemmatizer
replacement_patterns = [
    (r'j', 'i'),
    (r'v', 'u'),
    (r'J', 'I'),
    (r'V', 'U'),
]

class JVReplacer(object):
    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
        return s
