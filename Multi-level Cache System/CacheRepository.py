class CacheRepository:
    def __init__(self):
        self.cache_levels = {}
    
    def save(self, cache):
        self.cache_levels[cache.level] = cache
    
    def get(self, cache_level):
        if cache_level not in self.cache_levels:
            raise KeyError("Cache Level not found")
        return self.cache_levels[cache_level]

    def list_levels(self):
        return list(self.cache_levels.keys())

    def get_level_count(self):
        return len(self.cache_levels)
