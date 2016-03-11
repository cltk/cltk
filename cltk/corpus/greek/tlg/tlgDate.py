# TODO: Meke it compatible with dateTime
class Year(object):
    def __init__(self):
        self.val = ""
        self.isAD = False
        self.isBC = False
        self.isPost = False
        self.isAnte = False
        self.isProblematical = False


class tlgDate(object):

    def __init__(self):
        self.isRange = False
        self.separator = None
        self.year_first = Year()
        self.year_second = Year()
        self.isIncertum = False
        self.isVaria = False

    def __str__(self):
        out = "{"
        if self.isVaria:
            out += "Varia"
        elif self.isIncertum:
            out += "Incertum"
        else:
            if self.isRange:
                out += self._print(self.year_first)
                out += " " + self.separator + " "
                out += self._print(self.year_second)
            else:
                out += self._print(self.year_first)
        out += "}"
        return out

    def _print(self, year):
        out = ""
        if year.isPost:
            out += "post "
        if year.isAnte:
            out += "ante "
        out += year.val
        if year.isAD:
            out += " A.D."
        elif year.isBC:
            out += " B.C."
        if year.isProblematical:
            out += ", Problematical"
        return out

    def parse(self, to_parse):
        to_parse = str(to_parse)
        if "incertum" in to_parse.lower():
            self.isIncertum = True
        elif "varia" in to_parse.lower():
            self.isVaria = True
        else:
            if "A.D." in to_parse:
                to_parse = to_parse.replace('A.D.', 'AD')
            if "B.C." in to_parse:
                to_parse = to_parse.replace('B.C.', 'BC')

            if "-" in to_parse or "/" in to_parse:
                if "-" in to_parse:
                    self.separator = "-"
                elif "/" in to_parse:
                    self.separator = "/"
                self.isRange = True
                loc = to_parse.find(self.separator)
                first_range = to_parse[:loc]
                second_range = to_parse[loc+1:]
                come_back_to_first = False
                if "AD" in first_range:
                    self.year_first.isAD = True
                elif "BC" in first_range:
                    self.year_first.isBC = True
                else:
                    come_back_to_first = True

                if "AD" in second_range:
                    self.year_second.isAD = True
                elif "BC" in second_range:
                    self.year_second.isBC = True
                else:
                    self.year_second.isAD = self.year_first.isAD
                    self.year_second.isBC = self.year_first.isBC

                if(come_back_to_first):
                    self.year_first.isAD = self.year_second.isAD
                    self.year_first.isBC = self.year_second.isBC
                self.year_first.val, self.year_first.isPost, self.year_first.isAnte, \
                    self.year_first.isProblematical = self._add_attributes(first_range)
                self.year_second.val, self.year_second.isPost, self.year_second.isAnte, \
                    self.year_second.isProblematical = self._add_attributes(second_range)
            else:
                self.isRange = False
                self.year_second = None
                if "AD" in to_parse:
                    self.year_first.isAD = True
                elif "BC" in to_parse:
                    self.year_first.isBC = True
                self.year_first.val, self.year_first.isPost, self.year_first.isAnte, \
                    self.year_first.isProblematical = self._add_attributes(to_parse)
        return self

    def _add_attributes(self, to_check):
        val = ""
        isPost = None
        isAnte = None
        isProblematical = False
        for i in range(len(to_check)):
            if to_check[i].isdigit():
                val += to_check[i]
        if("p." in to_check):
            isPost = True
            isAnte = False
        elif("a." in to_check):
            isPost = False
            isAnte = True
        if("?" in to_check):
            isProblematical = True
        return val, isPost, isAnte, isProblematical
