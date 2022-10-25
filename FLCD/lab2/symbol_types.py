from enum import Enum


class SymbolTypes(Enum):
    ID = 1
    STRING_CONST = 2
    INT_CONST = 3

    def __str__(self):
        return self.name

