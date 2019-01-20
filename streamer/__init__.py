import functools
import itertools
from typing import Iterable, Iterator, Union, Callable, List


class Stream:
    def __init__(self, x: Union[Iterable, Iterator]):
        if isinstance(x, Iterable):
            self._iterator = iter(x)
        elif isinstance(x, Iterator):
            self._iterator = x

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iterator)

    def __add__(self, other):
        self._iterator = itertools.chain(self._iterator, other)
        return self

    def __radd__(self, other):
        return self + other

    @property
    def iterator(self):
        return self._iterator

    def concat(self, other):
        return self + other

    def enumerate(self):
        self._iterator = enumerate(self._iterator)
        return self

    def sorted(self, key=None, reverse=False):
        return sorted(self, key=key if key else lambda x: x, reverse=reverse)

    def max(self, key=None, default=None):
        return max(self, key=key if key else lambda x: x, default=default)

    def min(self, key=None, default=None):
        return min(self, key=key if key else lambda x: x, default=default)

    def map(self, f: Callable[[object], object]):
        self._iterator = map(f, self._iterator)
        return self

    def flat_map(self, f: Callable[[object], List[object]]):
        self._iterator = (y for x in self._iterator for y in f(x))
        return self

    def filter(self, f: Callable[[object], bool]):
        self._iterator = filter(f, self._iterator)
        return self

    def zip(self, *other):
        self._iterator = zip(self._iterator, *other)
        return self

    def zip_longest(self, *other, fillvalue=None):
        self._iterator = itertools.zip_longest(self._iterator, *other, fillvalue=fillvalue)
        return self

    def drop(self, f: Callable[[object], bool]):
        self._iterator = itertools.filterfalse(f, self._iterator)
        return self

    def skip(self, n: int = 0):
        for _ in range(n):
            next(self)
        return self

    def reduce(self, f: Callable[[object, object], Iterable], initial=None):
        if initial is not None:
            return functools.reduce(f, self, initial)
        return functools.reduce(f, self)

    def take(self, n: int = None, as_list=True):
        if n is None:
            return list(self)
        if not as_list:
            def generator():
                for _ in range(n):
                    yield next(self._iterator)

            return generator()
        result = []
        for i in range(n):
            result.append(next(self))
        return list(result)


stream = Stream
pipe = Stream

__version__ = '0.1'
__all__ = [
    'stream',
    'pipe',
    'Stream'
]
