from CacheLevel import CacheLevel
from CacheRepository import CacheRepository
from collections import deque

DATA_LIMIT_COUNT = 5

class CacheManager:
    def __init__(self):
        self.cache_repository = CacheRepository()
        self.read_times = deque()
        self.write_times = deque()
    
    def initialize_cache(self, capacity, read_time, write_time):
        try:
            level = f"L{self.cache_repository.get_level_count()+1}"
            cache = CacheLevel(level, capacity, read_time, write_time)
            self.cache_repository.save(cache)
        except Exception as err:
            raise err
    
    def read(self, key):
        try:
            levels = sorted(self.cache_repository.list_levels())
            passed_levels = []
            found = False
            time_taken = 0

            for level in levels:
                current_cache_level = self.cache_repository.get(level)
                found, val = current_cache_level.key_found(key)
                time_taken += current_cache_level.get_read_time()
                if not found:
                    passed_levels.append(current_cache_level)
                    continue
                else:
                    break
            
            if found and val != -1:
                for p_level in passed_levels:
                    p_level.key_written(key, val)
                    time_taken += p_level.get_write_time()
            
            self.populate_times(read_time=time_taken)
            return val, time_taken

        except Exception as err:
            raise err

    def write(self, key, value):
        try:
            levels = sorted(self.cache_repository.list_levels())
            found = False
            time_taken = 0

            for level in levels:
                current_cache_level = self.cache_repository.get(level)
                found, old_val = current_cache_level.key_found(key)
                time_taken += current_cache_level.get_read_time()
                if found and old_val == value:
                    break
                else:
                    current_cache_level.key_written(key, value)
                    time_taken += current_cache_level.get_write_time()
                    
            self.populate_times(write_time=time_taken)
            return time_taken
        except Exception as err:
            raise err
    
    def populate_times(self, read_time=None, write_time=None):
        try:
            if read_time is not None:
                if len(self.read_times) == DATA_LIMIT_COUNT:
                    _ = self.read_times.popleft()
                self.read_times.append(read_time)
            if write_time is not None:
                if len(self.write_times) == DATA_LIMIT_COUNT:
                    _ = self.write_times.popleft()
                self.write_times.append(write_time)

        except Exception as err:
            raise err
        
    def filled(self):
        try:
            levels = sorted(self.cache_repository.list_levels())
            for level in levels:
                current_cache_level = self.cache_repository.get(level)
                print(f"{level} = {current_cache_level.get_fill_status() * 100}%")
        except Exception as err:
            raise err
    
    def average_reads(self):
        try:
            if not self.read_times:
                return 0
            return sum(self.read_times)/len(self.read_times)
        except Exception as err:
            raise err
    
    def average_writes(self):
        try:
            if not self.write_times:
                return 0
            return sum(self.write_times)/len(self.write_times)
        except Exception as err:
            raise err
        

if __name__ == '__main__':
    cacheManager = CacheManager()
    cacheManager.initialize_cache(2, 1, 2)
    cacheManager.initialize_cache(3, 5, 8)
    cacheManager.initialize_cache(10, 10, 15)
    cacheManager.filled()


    print("\n--- TEST 1: Basic WRITE ---")
    cacheManager.write("A", 10)
    cacheManager.write("B", 20)

    print("\n--- TEST 2: READ from L1 (fast hit) ---")
    print(cacheManager.read("A"))

    print("\n--- TEST 3: WRITE new key ---")
    cacheManager.write("C", 30)

    print("\n--- TEST 4: Trigger L1 eviction ---")
    cacheManager.write("D", 40)  # L1 capacity=2 should evict LRU

    print("\n--- TEST 5: READ key evicted from L1 but present in L2 ---")
    print(cacheManager.read("A"))  # should promote back to L1

    print("\n--- TEST 6: READ missing key ---")
    print(cacheManager.read("Z"))  # key does not exist

    print("\n--- TEST 7: WRITE same value (should stop early) ---")
    cacheManager.write("A", 10)

    print("\n--- TEST 8: WRITE overwrite value ---")
    cacheManager.write("A", 999)
    print(cacheManager.read("A"))

    print("\n--- TEST 9: Fill cache to trigger multiple evictions ---")
    cacheManager.write("E", 50)
    cacheManager.write("F", 60)
    cacheManager.write("G", 70)

    print("\n--- TEST 10: READ from deepest level promotion ---")
    print(cacheManager.read("B"))

    print("\n--- TEST 11: Multiple reads to test average read stats ---")
    cacheManager.read("A")
    cacheManager.read("B")
    cacheManager.read("C")
    cacheManager.read("D")
    cacheManager.read("E")

    print("\n--- TEST 12: Multiple writes to test average write stats ---")
    cacheManager.write("H", 80)
    cacheManager.write("I", 90)
    cacheManager.write("J", 100)
    cacheManager.write("K", 110)
    cacheManager.write("L", 120)

    print("\n--- TEST 13: STAT ---")
    cacheManager.filled()
    print(cacheManager.average_reads())
    print(cacheManager.average_writes())
