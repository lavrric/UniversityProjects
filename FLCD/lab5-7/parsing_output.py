from grammar import Production
from collections import deque


class Node:
    next_id = 0

    def __init__(self, child, right_sibling, value, depth) -> None:
        self.__child: Node = child
        self.__right_sibling: Node = right_sibling
        self.__value = value
        self.__depth = depth
        self.__id = Node.next_id
        Node.next_id += 1

    @property
    def child(self):
        return self.__child

    @child.setter
    def child(self, val):
        self.__child = val

    @property
    def right_sibling(self):
        return self.__right_sibling

    @right_sibling.setter
    def right_sibling(self, val):
        self.__right_sibling = val

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        self.value = val

    @property
    def depth(self):
        return self.__depth

    @depth.setter
    def depth(self, val):
        self.depth = val

    def __str__(self) -> str:
        return f"{self.__value}(id: {self.__id}, child: { self.child.__id if self.child else '-'}, " \
               f"right id: {self.right_sibling.__id  if self.right_sibling else '-'}, depth: {self.depth})"


class ParsingOutput:
    def __init__(self) -> None:
        self.__head = None

    def search_parent(self, node: Node, value):
        if node.right_sibling:
            obtained = self.search_parent(node.right_sibling, value)
            if obtained:
                return obtained
        if node.value == value and node.child is None:
            return node
        if node.child:
            obtained = self.search_parent(node.child, value)
            if obtained:
                return obtained
        return None

    def add_production(self, production: Production):
        parent = production.lhs
        children = production.rhs.split()
        print(f"Parent: {parent}, children: {children}")
        parent = self.search_parent(self.__head, parent) if self.__head is not None else Node(None, None, parent, 0)
        self.__head = parent if self.__head is None else self.__head

        right_sibling = None
        for i in range(len(children) - 1, -1, -1):
            right_sibling = Node(None, right_sibling, children[i], parent.depth + 1)
        parent.child = right_sibling

    def process_parser_output(self, production_list):
        for production in production_list:
            self.add_production(production)

    def print_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))
        f.close()

    def __str__(self) -> str:
        s = ''
        q = deque()
        q.append(self.__head)
        while len(q):
            node = q.pop()
            s += str(node) + '\n'
            if node.right_sibling:
                q.append(node.right_sibling)
            if node.child:
                q.append(node.child)
        return s
