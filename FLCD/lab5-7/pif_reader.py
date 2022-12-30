class PifField:
    def __init__(self, key, token_index, table_index) -> None:
        self.key = key
        self.token_index = token_index
        self.table_index = table_index

class PifReader:
    def __init__(self) -> None:
        self.__pif = []

    def readPIF(self, filename):
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                key, val = line.split(':')
                val = val.strip('() \n')
                token_index, table_index = val.split(',')
                token_index = int(token_index)
                table_index = int(table_index)

                self.__pif.append(PifField(key, token_index, table_index))

    def get_keys(self):
        return ['CONST' if x.token_index == 1 else 'IDENT' if x.token_index == 0 else x.key for x in self.__pif]

    def __str__(self) -> str:
        s = ''
        for field in self.__pif:
            s += f'{field.key} -> ({field.token_index}, {field.table_index})\n'

        return s