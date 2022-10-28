import re
from enum import Enum

from lab2.symbol_table import SymbolTable
from lab2.symbol_types import SymbolTypes


class TokenType(Enum):
    SYMBOL = 1
    SEPARATOR = 2


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
                        tokens.append((word, TokenType.SYMBOL))
                # handling <= != == >=
                elif i < len(line) - 1 and (char + line[i+1]) in self.separators:
                    if len(word):
                        tokens.append((word,
                                       TokenType.SEPARATOR if word in self.keywords + self.separators
                                       else TokenType.SYMBOL))
                    word = ''
                    tokens.append((char + line[i+1], TokenType.SEPARATOR))
                    i += 1
                # simple separators
                elif char in self.separators:
                    if len(word):
                        tokens.append((word,
                                       TokenType.SEPARATOR if word in self.keywords + self.separators
                                       else TokenType.SYMBOL))
                    if char != ' ' and char != '\n':
                        tokens.append((char, TokenType.SEPARATOR))
                    word = ''
                else:
                    word += char
                i += 1
                if i == len(line) and len(word):
                    tokens.append((word,
                                   TokenType.SEPARATOR if word in self.keywords + self.separators
                                   else TokenType.SYMBOL))
        # print(list(map(lambda token: token[0], filter(lambda token: token[1] == TokenType.SEPARATOR, tokens))))
        return tokens

    def __process_symbols(self, tokens):
        for token, _ in filter(lambda token_data: token_data[1] == TokenType.SYMBOL, tokens):
            if re.fullmatch(r"([a-zA-Z])([a-zA-Z_\d])*", token):
                self.symbol_table.add(token, SymbolTypes.ID)
            elif re.fullmatch(r"['\"].*['\"]", token) and token[0] == token[-1]:
                self.symbol_table.add(token, SymbolTypes.STRING_CONST)
            elif re.fullmatch(r"\d*", token):
                self.symbol_table.add(token, SymbolTypes.INT_CONST)
            else:
                print('Error:', token, "doesn't satisfy the lexicon of the language.")
        return self.symbol_table

    def scan(self, filename):
        self.symbol_table.clear()
        self.__load_file(filename)
        return self.__process_symbols(self.__parse_tokens())


scanner = Scanner()
filenames = ['../test_programs/p1.txt', '../test_programs/p2.txt',
             '../test_programs/p3.txt', '../test_programs/p1_err.txt']
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
