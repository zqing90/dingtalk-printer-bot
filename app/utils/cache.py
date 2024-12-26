class Cache:
    c = None
    c_lock = None

    def __init__(self,g_cache,g_cache_lock):
        self.c = g_cache
        self.c_lock = g_cache_lock

    def set_cache_key(self,cache_key,value):
        with self.c_lock:
            self.c[cache_key] = value
    def get_cache_key(self,cache_key):
        if not cache_key in self.c:
            return None
        return self.c.get(cache_key)