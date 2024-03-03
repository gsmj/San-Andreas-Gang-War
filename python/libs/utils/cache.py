from typing import Any
weak_cache: dict[Any] = {}

def to_cache(**kwargs: dict[Any]) -> dict:
    for key, value in kwargs.items():
        weak_cache[key] = value

    return weak_cache

def free_by_key(key: Any) -> None:
    del weak_cache[key]

def free() -> None:
    weak_cache.clear()