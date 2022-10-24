from hash_table import HashTable
from symbol_types import SymbolTypes


class SymbolTable:
    def __init__(self):
        self.hash_table = HashTable()

    def add(self, value, symbol_type):
        if self.search(value):
            return False
        self.hash_table.add((value, symbol_type))
        return True

    def search(self, value):
        for symbol_type in SymbolTypes:
            data = (value, symbol_type)
            if data in self.hash_table:
                return data
        return None

    def clear(self):
        self.hash_table.clear()

    def __str__(self):
        return str(self.hash_table)
