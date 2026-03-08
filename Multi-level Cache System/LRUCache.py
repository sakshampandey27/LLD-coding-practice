from Node import Node
from EvictionStrategy import EvictionStrategy

class LRUCache(EvictionStrategy):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.storage = {}

        self.head = Node(0,0)
        self.tail = Node(0,0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def count_items(self):
        return len(self.storage)
    
    def get(self, key: int) -> int:
        if key in self.storage:
            target_node = self.storage[key]
            self.remove(target_node)
            self.insert(target_node)
            return target_node.value
        return -1

    def put(self, key: int, value: int) -> None:
        insert_node = Node(key, value)

        if key in self.storage:
            target_node = self.storage[key]
            self.remove(target_node)
            del target_node

        elif len(self.storage) == self.capacity:
            node_to_remove = self.tail.prev
            self.remove(node_to_remove)
            del self.storage[node_to_remove.key]

        self.insert(insert_node)
        self.storage[key] = insert_node
    
    def remove(self, node_to_remove):
        prev_node = node_to_remove.prev
        next_node = node_to_remove.next
        prev_node.next = next_node
        next_node.prev = prev_node
        node_to_remove.prev = None
        node_to_remove.next = None

    def insert(self, node_to_insert):
        first = self.head.next
        self.head.next = node_to_insert
        node_to_insert.prev = self.head
        node_to_insert.next = first
        first.prev = node_to_insert
