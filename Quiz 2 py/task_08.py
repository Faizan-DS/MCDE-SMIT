# Task 08 | Cache Decorator with Expiration
import time
from functools import wraps

def ttl_cache(seconds):
   
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or seconds <= 0:
        raise ValueError("seconds must be a number greater than zero")

    def decorator(func):
        cache = {}
        stats = {"hits": 0, "misses": 0}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()

            try:
                hash(key)
            except TypeError:                    
                stats["misses"] += 1
                return func(*args, **kwargs)

            if key in cache:
                result, saved_at = cache[key]
                if now - saved_at < seconds:
                    stats["hits"] += 1
                    return result
                del cache[key]                  

            stats["misses"] += 1
            result = func(*args, **kwargs)
            cache[key] = (result, time.monotonic())
            return result

        def cache_info():
            return {"hits": stats["hits"], "misses": stats["misses"], "size": len(cache)}

        def cache_clear():
            cache.clear()
            stats["hits"] = 0
            stats["misses"] = 0

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper

    return decorator


if __name__ == "__main__":
    @ttl_cache(0.3)
    def add(x, y):
        """Add two numbers."""
        return x + y

    print(add(x=2, y=3))
    print(add(y=3, x=2))         
    print(add.cache_info())  
    time.sleep(0.4)
    print(add(x=2, y=3))        
    print(add.cache_info())    
    print(add.__name__, "-", add.__doc__)

    @ttl_cache(5)
    def length(items):
        return len(items)
    print(length([1, 2, 3]), length([1, 2, 3]), length.cache_info())