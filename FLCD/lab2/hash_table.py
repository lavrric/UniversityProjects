from functools import reduce


class HashTable:
    def __init__(self):
        self.mod = 257
        self.data = [[] for _ in range(257)]

    def add(self, value):
        curr_hash = hash(value) % self.mod
        self.data[curr_hash].append(value)

    def __contains__(self, value):
        curr_hash = hash(value) % self.mod
        if value in self.data[curr_hash]:
            return True
        return False

    def clear(self):
        self.data = [[] for _ in range(257)]

    def __str__(self):
        return reduce(lambda acc, curr: acc + str(curr) + '\n', reduce(lambda acc, curr: acc + curr, self.data, []), '')
