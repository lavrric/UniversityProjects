class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.cnt = 0

    def add(self, value):
        node = Node(value)
        if self.cnt:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self.cnt += 1

    def clear(self):
        self.head = None
        self.tail = None
        self.cnt = 0

    @property
    def data(self):
        data = []
        node = self.head
        while node is not None:
            data.append(node.value)
            node = node.next
        return data


# linked_list = LinkedList()
# linked_list.add(4)
# linked_list.add(3)
# linked_list.add(5)
# print(linked_list.data)
