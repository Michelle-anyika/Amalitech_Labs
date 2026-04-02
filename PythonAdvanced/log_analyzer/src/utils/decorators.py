import time
from functools import wraps, lru_cache

def timer_decorator(func):
    """Measures precise operation execution deltas"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time of {func.__name__}: {end - start}s")
        return result
    return wrapper

def cache_decorator(func):
    """Hooks python's native cache algorithm into analytical pipelines"""
    return lru_cache(maxsize=128)(func)

def log_call(func):
    """Hooking interceptors to dump payload logs per execution"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling function '{func.__name__}' with args: {args}")
        return func(*args, **kwargs)
    return wrapper
