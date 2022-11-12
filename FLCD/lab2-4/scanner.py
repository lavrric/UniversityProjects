import re
from enum import Enum

from pif.pif import Pif
from symbol_table.symbol_table import SymbolTable, SymbolTypes


class TokenType(Enum):
    SYMBOL = 1
    SEPARATOR = 2


class Scanner:
    def __init__(self):
        self.program_lines = []
        self.symbol_table = SymbolTable()
        self.pif = Pif()
        self.keywords = ['for', 'if', 'else', 'while', 'in', 'out', 'Number']
        self.separators = ['+', '-', '*', '**', '/', '%', '&&', '||', '<=', '==', '!=', '>=', '=', '<', '>', '{', '}',
                           '(', ')',
                           ';', ' ', '\t', '\n', '"', "'"]

    def __clear(self):
        self.program_lines = []
        self.symbol_table.clear()
        self.pif.clear()

    def __load_file(self, filename):
        with open(filename) as ff:
            self.program_lines = ff.readlines()

    def __parse_tokens(self):
        tokens = []
        for line_id, line in enumerate(self.program_lines):
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
                elif i < len(line) - 1 and (char + line[i + 1]) in self.separators:
                    word = word.strip()
                    if len(word):
                        tokens.append((word,
                                       TokenType.SEPARATOR if word in self.keywords + self.separators
                                       else TokenType.SYMBOL))
                    word = ''
                    tokens.append((char + line[i + 1], TokenType.SEPARATOR))
                    i += 1
                # simple separators
                elif char in self.separators:
                    word = word.strip()
                    if len(word):
                        tokens.append((word,
                                       TokenType.SEPARATOR if word in self.keywords + self.separators
                                       else TokenType.SYMBOL))
                    if char not in [' ', '\t', '\n']:
                        tokens.append((char, TokenType.SEPARATOR))
                    word = ''
                else:
                    word += char
                i += 1
                if i == len(line):
                    word = word.strip()
                    if len(word):
                        tokens.append((word,
                                       TokenType.SEPARATOR if word in self.keywords + self.separators
                                       else TokenType.SYMBOL))
                    word = ''
        return tokens

    def __process_symbols_and_pif(self, tokens):
        # symbol table processing
        for token, token_type in filter(lambda token_data: token_data[1] == TokenType.SYMBOL, tokens):
            if re.fullmatch(r"([a-zA-Z])([a-zA-Z_\d])*", token):
                self.symbol_table.add(token, SymbolTypes.ID)
            elif re.fullmatch(r"['\"].*['\"]", token) and token[0] == token[-1]:
                self.symbol_table.add(token, SymbolTypes.STRING_CONST)
            elif re.fullmatch(r"\d*", token):
                self.symbol_table.add(token, SymbolTypes.INT_CONST)
            else:
                tokens.remove((token, token_type))
                lines_data = list(map(lambda line_data: line_data[0],
                                      filter(lambda line_data: token in line_data[1], enumerate(self.program_lines))
                                      ))
                for line_id in lines_data:
                    print('Error:', token, "doesn't satisfy the lexicon of the language (line " + str(line_id) + ').')

        # pif processing, necessitates a valid symbol table !!!
        for token, token_type in tokens:
            if token_type == TokenType.SYMBOL:
                symbol_table_item = self.symbol_table.search(token)
                self.pif.add(token, symbol_table_item.id, symbol_table_item.symbol_type)
            else:
                self.pif.add(token)
        return self.symbol_table, self.pif

    def scan(self, filename):
        self.__clear()
        self.__load_file(filename)
        return self.__process_symbols_and_pif(self.__parse_tokens())


scanner = Scanner()
filenames = ['../test_programs/p1.txt', '../test_programs/p2.txt',
             '../test_programs/p3.txt', '../test_programs/p1_err.txt']

for name in filenames:
    print('Working on', name + '...')
    symbol_table, pif = scanner.scan(name)
    short_name = name.split("/")[-1].split(".")[-2]  # TODO change in case filenames change structure
    with open(f'./out_scanner/st-{short_name}.out', 'w') as f:
        f.write('\nSymbol table for ' + name + ': ' + '\n\n' + str(symbol_table) + '\n')
        f.close()
    with open(f'./out_scanner/pif-{short_name}.out', 'w') as f:
        f.write('\nPIF for ' + name + ': ' + '\n\n' + str(pif) + '\n')
        f.close()
