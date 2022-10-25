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
        self.curr_id = 1

    def __load_file(self, filename):
        with open(filename) as f:
            self.program_lines = f.readlines()

    def __parse_tokens(self):
        tokens = []
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
                        tokens.append((word, self.curr_id))
                        self.curr_id += 1
                # handling <= != == >=
                elif i < len(line) - 1 and (char + line[i+1]) in self.separators:
                    if len(word) and word not in self.keywords:
                        tokens.append((word, self.curr_id))
                        self.curr_id += 1
                    word = ''
                    i += 1
                # simple separators
                elif char in self.separators:
                    if len(word) and word not in self.keywords:
                        tokens.append((word, self.curr_id))
                        self.curr_id += 1
                    word = ''
                else:
                    word += char
                i += 1
                if i == len(line) and len(word):
                    tokens.append((word, self.curr_id))
                    self.curr_id += 1
        return tokens

    def __process_tokens(self, tokens):
        for word, i in tokens:
            if re.fullmatch(r"([a-zA-Z])([a-zA-Z_\d])*", word):
                self.symbol_table.add(word, i, SymbolTypes.ID)
            elif re.fullmatch(r"['\"].*['\"]", word) and word[0] == word[-1]:
                self.symbol_table.add(word, i, SymbolTypes.STRING_CONST)
            elif re.fullmatch(r"\d*", word):
                self.symbol_table.add(word, i, SymbolTypes.INT_CONST)
            else:
                print('Error:', word, "doesn't satisfy the lexicon of the language.")
        return self.symbol_table

    def scan(self, filename):
        self.symbol_table.clear()
        self.curr_id = 1
        self.__load_file(filename)
        return self.__process_tokens(self.__parse_tokens())


scanner = Scanner()
filenames = ['p1.txt', 'p2.txt', 'p3.txt', 'p1_err.txt']
print()
for name in filenames:
    print('Working on', name + '...')
    print('\nSymbol table for', name + ':', '\n\n' + str(scanner.scan(name)), '\n')

# test symbol table
# symbol_table = SymbolTable()
# symbol_table.add('a', SymbolTypes.CONST)
# symbol_table.add('b', SymbolTypes.CONST)
# symbol_table.add('val', SymbolTypes.ID)
# print(symbol_table.search('a'))
# print(symbol_table.search('none'))
# print(symbol_table.search('val'))
