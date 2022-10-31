from functools import reduce
from hash_table import HashTable


class SymbolTableItem:
    def __init__(self, value, _id, symbol_type):
        self.__value = value
        self.__id = _id
        self.__symbol_type = symbol_type

    @property
    def value(self):
        return self.__value

    @property
    def id(self):
        return self.__id

    @property
    def symbol_type(self):
        return self.__symbol_type

    def __str__(self):
        return str(self.__value) + ' ' * max(1, 14 - len(str(self.__value))) + \
               str(self.__symbol_type) + ' ' * (14 - len(str(self.__symbol_type))) + \
               str(self.__id)


class SymbolTable:
    def __init__(self):
        self.hash_table = HashTable()
        self.__id = 0

    @property
    def id(self):
        self.__id += 1
        return self.__id

    def add(self, value, symbol_type):
        if self.search(value):
            return False
        self.hash_table.add(SymbolTableItem(value, self.id, symbol_type))
        return True

    def search(self, value):
        for data in self.hash_table.data:
            if data.value == value:
                return data
        return None

    def clear(self):
        self.__id = 0
        self.hash_table.clear()

    def __str__(self):
        return "Sym" + " " * 11 + "Type" + " " * 10 + "Id\n" + \
            reduce(
                lambda a, b: a + b + '\n',
                map(lambda x: str(x), self.hash_table.data),
                ''
            ) + '-' * 30
