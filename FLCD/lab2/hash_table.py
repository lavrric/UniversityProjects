from functools import reduce


class HashTable:
    def __init__(self):
        self.__mod = 257
        self.__data = [[] for _ in range(257)]

    def add(self, value):
        curr_hash = hash(value) % self.__mod
        self.__data[curr_hash].append(value)

    def __contains__(self, value):
        curr_hash = hash(value) % self.__mod
        if value in self.__data[curr_hash]:
            return True
        return False

    def clear(self):
        self.__data = [[] for _ in range(257)]

    @property
    def data(self):
        return reduce(lambda acc, curr: acc + curr, self.__data, [])
