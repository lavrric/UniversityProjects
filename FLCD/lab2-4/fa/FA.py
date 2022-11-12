from functools import reduce


class Transition:
    def __init__(self, from_state, to_state, move):
        self.from_state = from_state
        self.to_state = to_state
        self.move = move

    def __str__(self):
        return 'd(' + self.from_state.name + ', ' + self.move + ') = ' + self.to_state.name


class State:
    def __init__(self, name):
        self.name = name
        self.transitions = [] # keep the transitions that start from this state
        self.is_start = False
        self.is_final = False

    def __str__(self):
        return f'State {self.name} (start: {self.is_start}, final: {self.is_final}), ' \
               f'{len(self.transitions)} transitions from it.'

    def full_str(self):
        return f'State {self.name} (start: {self.is_start}, final: {self.is_final}) has transitions:\n' + \
               "\n".join(map(str, self.transitions))


class FiniteAutomata:
    def __init__(self, _filename):
        self.filename = _filename
        self.states = []
        self.alphabet = set()
        self.start_state = None
        self.load_file()

    def load_file(self):
        with open(self.filename) as ff:
            lines = list(map(lambda l: l.strip(), ff.readlines()))
            # print(list(enumerate(lines)))
            # first input the number of states, the first of which is the starting one
            states_no = int(lines[0])
            for i in range(1, states_no + 1):
                state = State(lines[i])
                if i == 1:
                    state.is_start = True
                    self.start_state = state
                self.states.append(state)

            current_line = states_no + 1
            final_states_no = int(lines[current_line])
            for i in range(current_line + 1, current_line + final_states_no + 1):
                name = lines[i]
                for state in self.states:
                    if state.name == name:
                        state.is_final = True

            current_line = current_line + final_states_no + 1
            transition_no = int(lines[current_line])
            for i in range(current_line + 1, current_line + transition_no + 1):
                from_name, to_name, moves = lines[i].split()
                for state in self.states:
                    if state.name == to_name:
                        to_state = state
                for state in self.states:
                    if state.name == from_name:
                        for move in moves:
                            self.alphabet.add(move)
                            state.transitions.append(Transition(state, to_state, move))

    @property
    def sorted_alphabet(self):
        return sorted(self.alphabet)

    @property
    def transitions(self):
        return list(reduce(lambda acc, cur: acc + cur,
                           (map(lambda s:
                                s.transitions,
                                self.states
                                )
                            )
                           )
                    )

    @property
    def final_states(self):
        return list(filter(lambda s: s.is_final, self.states))

    def __str__(self):
        return '\n\n'.join(list(map(lambda t: t.full_str(), self.states)))

    def check_sequence(self, s):
        cur_state = self.start_state
        cur_index = 0
        while cur_index < len(s):
            exists = False
            for transition in cur_state.transitions:
                if transition.move == s[cur_index]:
                    cur_state = transition.to_state
                    cur_index += 1
                    exists = True
                    break
            if not exists:
                return False
        return True if cur_state.is_final else False


def list_to_str(ll):
    return reduce(lambda acc, cur: acc + str(cur) + '\n', ll, '')


filename = 'FA_int.in'
FA = FiniteAutomata(filename)
menu = {
    '0': ('states', lambda _: print(list_to_str(FA.states))),
    '1': ('alphabet', lambda _: print('Alphabet:\n' + str(FA.sorted_alphabet))),
    '2': ('transitions', lambda _: print(list_to_str(FA.transitions))),
    '3': ('initial state', lambda _: print(FA.start_state.full_str())),
    '4': ('final states', lambda _: print(list_to_str(FA.final_states))),
    '5': ('full info', lambda _: print(FA)),
    '6': ('check string', lambda s: print(FA.check_sequence(s))),
    '7': ('exit', lambda _: exit(0))
}

done = False
while not done:
    print()
    for item in menu.items():
        print(item[0] + ':', item[1][0])
    chosen = input()
    if chosen not in menu.keys():
        print('Not a menu key')
    else:
        param = ''
        if chosen == '6':
            param = input('Enter string:\n')
        menu[chosen][1](param)
