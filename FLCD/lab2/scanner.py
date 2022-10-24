from functools import reduce
from symbol_table import SymbolTable
from symbol_types import SymbolTypes
import re


class Scanner:
    def __init__(self):
        self.program_lines = []
        self.symbol_table = SymbolTable()
        self.keywords = ['for', 'if', 'else', 'while', 'in', 'out', 'Number']
        self.separators = ['+', '-', '*', '**', '/', '%', '&&', '||', '<=', '==', '!=', '>=', '=',  '<',  '>', '{', '}', '(', ')',
                           ';', ' ', '\t', '\n', '"', "'"]

    def __load_file(self, filename):
        with open(filename) as f:
            self.program_lines = f.readlines()

    def __parse_keywords(self):
        keywords = []
        for line in self.program_lines:
            word = ''
            open_string_quotes = ''
            i = 0
            while i < len(line):
                char = line[i]
                # open const string
                if not len(open_string_quotes) and char in ['"', "'"]:
                    open_string_quotes = char
                    word += char
                elif len(open_string_quotes):
                    word += char
                    # close const string
                    if char == open_string_quotes:
                        open_string_quotes = ''
                        keywords.append(word)
                # handling <= != == >=
                elif i < len(line) - 1 and (char + line[i+1]) in self.separators:
                    if len(word) and word not in self.keywords:
                        keywords.append(word)
                    word = ''
                    i += 1
                # simple separators
                elif char in self.separators:
                    if len(word) and word not in self.keywords:
                        keywords.append(word)
                    word = ''
                else:
                    word += char
                i += 1
                if i == len(line) and len(word):
                    keywords.append(word)
        return keywords

    def __process_keywords(self, keywords):
        for word in keywords:
            if re.fullmatch(r"([a-zA-Z])([a-zA-Z_\d])*", word):
                self.symbol_table.add(word, SymbolTypes.ID)
            elif re.fullmatch(r"['\"].*['\"]", word) and word[0] == word[-1]:
                self.symbol_table.add(word, SymbolTypes.STRING_CONST)
            elif re.fullmatch(r"\d*", word):
                self.symbol_table.add(word, SymbolTypes.INT_CONST)
            else:
                print('Error:', word, "doesn't satisfy the lexicon of the language.\n")
        return self.symbol_table

    def scan(self, filename):
        self.symbol_table.clear()
        self.__load_file(filename)
        return self.__process_keywords(self.__parse_keywords())


scanner = Scanner()
filenames = ['p1.txt', 'p2.txt', 'p3.txt', 'p1_err.txt']
for name in filenames:
    print('Symbol table for', name + ':', '\n\n' + str(scanner.scan(name)), '\n')

# test symbol table
# symbol_table = SymbolTable()
# symbol_table.add('a', SymbolTypes.CONST)
# symbol_table.add('b', SymbolTypes.CONST)
# symbol_table.add('val', SymbolTypes.ID)
# print(symbol_table.search('a'))
# print(symbol_table.search('none'))
# print(symbol_table.search('val'))
