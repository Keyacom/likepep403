from collections.abc import Callable
from typing import overload

from .missing import MISSING


class Caller:
    def __init__(self, fn, /, *args, **kwargs):
        self.fn = fn
        self.args = list(args)
        self.kwargs = kwargs

    @overload
    def register(self, idx: str | int, item=MISSING, /) -> Callable:
        ...

    @overload
    def register(self, idx: str | int, item: object, /) -> None:
        ...

    def register(self, idx: str | int, item: object = MISSING, /):
        def wrap(i):
            match idx:
                case int():
                    if idx == len(self.args):
                        self.args.append(i)
                    else:
                        self.args[idx] = i
                case str():
                    self.kwargs[idx] = i
                case _:
                    raise TypeError(
                        f"Expected type of index to be int or str, got {type(idx).__qualname__!r}"
                    )
            return i

        if item is MISSING:
            return wrap
        wrap(item)

    def __call__(self):
        return self.fn(*self.args, **self.kwargs)

    call = exec = __call__
