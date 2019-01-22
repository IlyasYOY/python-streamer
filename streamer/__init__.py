import functools
import itertools
from typing import Iterable, Iterator, Union, Callable, List


class Stream:
    """
    This class provides a way to apply functions to a collection in a fluent way.
    Just wrap your iterator or iterable with it, and you are all set up.

    Library tries to do everything in a lazy manner.
    Terminal operations marked as TERMINAL, they cause data to be fully loaded into memory.
    """

    def __init__(self, x: Union[Iterable, Iterator]):
        """
        Creates only-one-traversable instance.
        :param x: You can pass here an iterable or iterator.
        """
        if isinstance(x, Iterable):
            self._iterator = iter(x)
        elif isinstance(x, Iterator):
            self._iterator = x

    def __iter__(self):
        """
        :return: self, because self is already an iterator.
        :rtype: Stream
        """
        return self

    def __next__(self):
        """
        Takes the first element from stream.
        :return: next element with applied operations.
        """
        return next(self.iterator)

    def __add__(self, other):
        """
        concat iterators.
        :param other: iterator that will be attached to the end.
        :return: self
        """
        self._iterator = itertools.chain(self._iterator, other)
        return self

    def __radd__(self, other):
        """
        concat iterators.
        :param other: iterator that will be attached to the end.
        :return: self
        """
        return self + other

    @property
    def iterator(self):
        """
        Returns inner iterator, please don't use this directly.
        :return: iterator
        """
        return self._iterator

    def concat(self, other):
        """
        concat iterators.
        :param other: iterator that will be attached to the end.
        :return: self
        """
        return self + other

    def enumerate(self, start=0):
        """
        Indexes elements of the iterator.
        :return: self
        """
        self._iterator = enumerate(self._iterator, start=start)
        return self

    def map(self, f: Callable[[object], object]):
        """
        Applies map to every element.
        :param f: function to apply.
        :return: self
        """
        self._iterator = map(f, self._iterator)
        return self

    def flat_map(self, f: Callable[[object], List[object]]):
        """
        Your function should return [].
        List will be flattened and iterator will iterate through elements of a flattened collection
        :param f: function to apply
        :return: self
        """
        self._iterator = (y for x in self._iterator for y in f(x))
        return self

    def filter(self, f: Callable[[object], bool]):
        """
        Only elements that fit predicate will be left.
        :param f: predicate
        :return: self
        """
        self._iterator = filter(f, self._iterator)
        return self

    def zip(self, *other):
        """
        Zips collections with wrapped collection.
        :param other: collection to be zipped.
        :return: self
        """
        self._iterator = zip(self._iterator, *other)
        return self

    def zip_longest(self, *other, fillvalue=None):
        """
        Alternative to zip, but resultin list will be max(map(len, [*others, self]))
        :param other: collections to zip with.
        :param fillvalue: value that will be placed as a empty block.
        :return: self
        """
        self._iterator = itertools.zip_longest(self._iterator, *other, fillvalue=fillvalue)
        return self

    def drop(self, f: Callable[[object], bool]):
        """
        Works as filter, but removes items that fit predicate.
        :param f: predicate
        :return: self
        """
        self._iterator = itertools.filterfalse(f, self._iterator)
        return self

    def skip(self, n: int = 0):
        """
        Skips n elements, CAUSES CALCULATIONS, all elements will be calculated and then dropped.
        :param n: number of items to skip.
        :return: self
        """
        for _ in range(n):
            next(self)
        return self

    def take(self, n: int = None, as_list=True):
        """
        TERMINAL by default, can be configured.

        Runs calculations.
        :param n: how many items to take.
        :param as_list: if false, then iterator will be returned, else list.
        :return:
        """
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

    def max(self, key=None, default=None):
        """
        TERMINAL

        Finds max element.
        :param key: function to map element to a comparable item.
        :param default: default result.
        :return: max element
        """
        return max(self, key=key if key else lambda x: x, default=default)

    def min(self, key=None, default=None):
        """
        TERMINAL

        Find min element.
        :param key: function to map element to a comparable item.
        :param default: default result.
        :return: min element
        """
        return min(self, key=key if key else lambda x: x, default=default)

    def sorted(self, key=None, reverse=False):
        """
        TERMINAL

        Returns sorted list.
        :param key: key: function to map element to a comparable item.
        :param reverse: True if desc order.
        :return: sorted list.
        """
        return sorted(self, key=key if key else lambda x: x, reverse=reverse)

    def reduce(self, f: Callable[[object, object], Iterable], initial=None):
        """
        Has the same semantics as default functools.reduce
        :param f: reduce function
        :param initial: initial value.
        :return: result.
        """
        if initial is not None:
            return functools.reduce(f, self, initial)
        return functools.reduce(f, self)


stream = Stream
pipe = Stream

__version__ = '0.2'
__all__ = [
    'stream',
    'pipe',
    'Stream'
]
