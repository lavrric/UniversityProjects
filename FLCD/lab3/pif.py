from functools import reduce

from linked_list import LinkedList


class PifItem:
    def __init__(self, token, _id, symbol_data=None):
        self.__token = token
        self.__id = _id
        # separator -> -1, symbol -> ()
        self.__symbol_data = symbol_data

    @property
    def token(self):
        return self.__token

    @property
    def id(self):
        return self.__id

    @property
    def symbol_data(self):
        return self.__symbol_data

    @property
    def is_symbol(self):
        return self.__symbol_data is not None

    def __str__(self):
        return self.__token + max(1, 15-len(self.__token)) * ' ' + '->    id:   ' \
               + str(self.__id) + ',' + max(0, 3 - len(str(self.__id))) * ' ' +  \
               ('  symbol data:    ' + str(self.__symbol_data[0]) + ',  ' + str(self.__symbol_data[1])
                if self.is_symbol else '')


class Pif:
    def __init__(self):
        self.__linked_list = LinkedList()
        self.__id = 0

    @property
    def id(self):
        self.__id += 1
        return self.__id

    def add(self, token, symbol_id=None, symbol_type=None):
        if symbol_id is not None and symbol_type is not None:
            self.__linked_list.add(PifItem(token, self.id, (symbol_id, symbol_type)))
        else:
            self.__linked_list.add(PifItem(token, self.id))

    @property
    def data(self):
        return self.__linked_list.data

    def clear(self):
        self.__id = 0
        self.__linked_list.clear()

    def __str__(self):
        data = self.data
        return reduce(lambda acc, cur: acc + '\n' + cur, map(lambda x: str(x), data), '')
