import re

suffixes = {
    1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
  2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों", "ें","ीय"],
    3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं", "ुओं", "ुएं", "ुआं"],
    4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं", "ताएं", "ियाँ", "ियों", "ियां"],
    5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
}


class Stemmer:
    def __init__(self, text, clean=False):
        self.text = text
        self.clean = clean
        
        return
    
    def hi_stem(self, word):
        for L in 5, 4, 3, 2, 1:
            if len(word) > L + 1:
                for suf in suffixes[L]:
                    if word.endswith(suf):
                        return word[:-L]
        return word
    
    def clean_text(self):
        self.text = re.sub(r"[()\"#/@;:<>{}`+=~|!?,']", "", self.text)
        self.text = re.sub(r"[॥।-]", " ", self.text)
        
    def stem(self):
        if self.clean == True:
            self.clean_text()
        
        li = []
        for word in self.text.strip().split():
            li.append(self.hi_stem(word))
        
        return li