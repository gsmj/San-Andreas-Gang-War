import functools
from dataclasses import dataclass
from functools import wraps
from typing import Callable

from pysamp.commands import cmd

commands: dict[str, list[str, int]] = {}
_NO_DESC: str = "Нет описания"


@dataclass(frozen=True)
class CommandType:
    all_types: int = 1
    vip_type: int = 2
    admin_type: int = 3
    gangwar_type: int = 4
    freeroam_type: int = 5
    deathmatch_type: int = 6


def cmd_ex(func: Callable, description: str = _NO_DESC, mode: int = CommandType.all_types) -> Callable:
    @wraps(func)
    def wrapper(*args: tuple, **kwargs) -> Callable:
        if isinstance(func, functools.partial):
            if not func.keywords["use_function_name"]:
                args[0].__name__ = func.keywords["aliases"][0] # Overwrite function name

        commands[f"/{args[0].__name__}"] = [description, mode]
        return func(*args, **kwargs)
    return wrapper