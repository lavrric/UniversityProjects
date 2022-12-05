from functools import reduce


class Parser:
    def __init__(self):
        self.__terminals = set()
        self.__non_terminals = set()
        self.__initial = None
        self.__productions = {}  # non terminal -> production[]
        self.__is_cfg = True
    
    @property
    def terminals(self):
        return sorted(self.__terminals)

    @property
    def non_terminals(self):
        return sorted(self.__non_terminals)

    @property
    def initial(self):
        return self.__initial

    @property
    def productions(self):
        return self.__productions

    def productions_for_one(self, non_terminal):
        return self.__productions[non_terminal]

    def read(self, filename: str):
        f = open(filename, 'r')
        lines = f.readlines()

        terminals = lines[0]
        non_terminals = lines[1]
        initial = lines[2]
        productions = lines[3:]

        for nt in non_terminals.split():
            self.__non_terminals.add(nt)

        for t in terminals.split():
            self.__terminals.add(t)

        self.__initial = initial.strip()

        for prod_line in productions:
            if len(prod_line.strip()):
                self.__process_production_line(prod_line)

    def __process_production_line(self, prod_line: str):
        non_terminal, rhp = list(map(lambda s: s.strip(), prod_line.split('->')))
        if non_terminal not in self.__non_terminals:  # checks if context free
            print('NON TERMINAL: ' + non_terminal)
            exit(0)

        for rule in list(map(lambda s: s.strip(), rhp.split('|'))):
            if non_terminal in self.__productions:
                self.__productions[non_terminal].append(rule)
            else:
                self.__productions[non_terminal] = [rule]


parser = Parser()
filename = 'g2.txt'  # 'top_g.txt'
parser.read(filename)

print()
print('Non Terminals:', ', '.join(parser.non_terminals))
print('Terminals:', ', '.join(parser.terminals))
print('Initial terminal:', parser.initial, '\n')
print('Getter for productions for the last non-terminal:', parser.productions_for_one(parser.non_terminals[-1]))
print('Productions:', reduce(
    lambda acc, cur: acc + '\n' + str(cur[0]) + ' -> ' + str(cur[1]),
    parser.productions.items(), '')
)
