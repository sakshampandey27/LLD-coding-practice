from LRUCache import LRUCache

class CacheLevel:
    def __init__(self, level, capacity, read_time, write_time):
        self.level = level
        self.capacity = capacity
        self.read_time = read_time
        self.write_time = write_time
        self.cache = LRUCache(capacity)
    
    def set_strategy(self, strategy):
        self.cache = strategy

    def get_read_time(self):
        return self.read_time

    def get_write_time(self):
        return self.write_time
    
    def get_fill_status(self):
        return self.cache.count_items() / self.capacity
    
    def get(self, key):
        val = self.cache.get(key)
        if val == -1:
            return False, val
        return True, val
    
    def put(self, key, val):
        self.cache.put(key, val)