from functools import reduce


class Production:
    def __init__(self, _lhs, _rhs):
        self.lhs = _lhs
        self.rhs = _rhs

    def __str__(self):
        return f'{self.lhs} -> {self.rhs}'

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs


class Grammar:
    def __init__(self):
        self.__terminals = set()
        self.__non_terminals = set()
        self.__initial = None
        self.__production_dict = {}  # non terminal -> production[]
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
    def production_dict(self):
        return self.__production_dict

    @property
    def production_list(self):
        return list(
            reduce(lambda acc, key: acc + self.__production_dict[key],
                   self.__production_dict,
                   [],
                   )
        )

    def productions_for_one(self, non_terminal):
        if non_terminal not in self.__non_terminals:
            return []
        return self.__production_dict[non_terminal]

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
            production = Production(non_terminal, rule)
            if non_terminal in self.__production_dict:
                self.__production_dict[non_terminal].append(production)
            else:
                self.__production_dict[non_terminal] = [production]


if __name__ == '__main__':
    grammar = Grammar()
    filename = 'top_g.txt'
    grammar.read(filename)

    print()
    print('Non Terminals:', ', '.join(grammar.non_terminals))
    print('Terminals:', ', '.join(grammar.terminals))
    print('Initial terminal:', grammar.initial, '\n')

    print('Getter for productions for the last non-terminal:',
          list(map(str, grammar.productions_for_one(grammar.non_terminals[-1]))))
    print('Getter for productions for not-existing non-terminal:',
          list(map(str, grammar.productions_for_one('X'))))

    print('Production dict:', reduce(
        lambda acc, cur: acc + '\n' + str(list(map(str, cur[1]))),
        grammar.production_dict.items(), '')
          )
    print()
    print('Production list:', reduce(
        lambda acc, cur: acc + '\n' + str(cur),
        grammar.production_list, '')
          )
