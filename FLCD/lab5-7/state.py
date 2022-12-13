class State:
    def __init__(self, _prod, _index):
        self.prod = _prod
        self.index = _index  # [0 .. len] - the index before the "point" in the kernel is

    @property
    def string_after_point(self):
        if self.index < len(self.prod.rhs) and self.prod.rhs[self.index] == ' ':
            self.index += 1
        r_index = self.prod.rhs.find(' ', self.index)
        if r_index == -1: 
            return self.prod.rhs[self.index:] 
        return self.prod.rhs[self.index:r_index]

    def shift_dot_right(self):
        if self.index < len(self.prod.rhs) and self.prod.rhs[self.index] == ' ':
            self.index += 1
        r_index = self.prod.rhs.find(' ', self.index) + 1

        r_index = r_index if r_index != self.index and r_index != 0 else len(self.prod.rhs)
        return State(self.prod, r_index)

    def __str__(self):
        return f"[{self.prod.lhs} -> {self.prod.rhs[:self.index].strip()} . {self.prod.rhs[self.index:].strip()}]"

    def __eq__(self, other):
        return self.prod == other.prod and self.index == other.index

