import functools
import time
from typing import Any, Callable


def exec_time(function: Callable[..., Any]) -> Any:
    functools.wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        function(*args, **kwargs)
        print(f"Function: {function}: {time.time() - start}")

    return wrapper
