from Node import Node
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}

        self.head = Node(0,0)
        self.tail = Node(0,0)
        self.head.next = self.tail
        self.tail.prev = self.head    

    def get(self, key: int) -> int:
        if key in self.cache:
            target_node = self.cache[key]
            self.remove(target_node)
            self.insert(target_node)
            return target_node.value
        return -1

    def put(self, key: int, value: int) -> None:
        insert_node = Node(key, value)

        if key in self.cache:
            target_node = self.cache[key]
            self.remove(target_node)
            del target_node

        elif len(self.cache) == self.capacity:
            node_to_remove = self.tail.prev
            self.remove(node_to_remove)
            del self.cache[node_to_remove.key]

        self.insert(insert_node)
        self.cache[key] = insert_node
    
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

if __name__ == '__main__':
    cache = LRUCache(3)
