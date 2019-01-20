import operator
from unittest import TestCase

from streamer import stream


class StreamTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._array1 = [1, 2, 3, 4, 5]
        self._array2 = [2, 4, 2, 0, 1, 10]

    def test_iterator(self):
        s = stream(self._array1)
        iterator = s.iterator
        self.assertListEqual(self._array1, list(iterator))

    def test_concat(self):
        self.assertListEqual(self._array1 + self._array2,
                             stream(self._array1).concat(stream(self._array2)).take())

    def test_add(self):
        self.assertListEqual(self._array1 + self._array2,
                             (stream(self._array1) + stream(self._array2)).take())
        self.assertListEqual(self._array1 + self._array2,
                             (stream(self._array1) + self._array2).take())
        self.assertListEqual(self._array1 + self._array2,
                             (self._array2 + stream(self._array1)).take())

    def test_enumerate(self):
        self.assertListEqual(list(enumerate(self._array2)),
                             stream(self._array2).enumerate().take())

    def test_sorted(self):
        self.assertListEqual(sorted(self._array2), stream(self._array2).sorted())

    def test_min_max(self):
        self.assertEqual(max(self._array2), stream(self._array2).max())
        self.assertEqual(min(self._array1), stream(self._array1).min())

    def test_map(self):
        self.assertListEqual([x ** 2 for x in self._array1], stream(self._array1).map(lambda x: x ** 2).take())

    def test_flat_map(self):
        self.assertListEqual([y for x in self._array1 for y in [x, x]],
                             stream(self._array1).flat_map(lambda x: [x, x]).take())

    def test_filter_drop(self):
        self.assertListEqual([x for x in self._array1 if x % 2 == 1],
                             stream(self._array1).filter(lambda x: x % 2 == 1).take())
        self.assertListEqual([x for x in self._array1 if not x % 2 == 1],
                             stream(self._array1).drop(lambda x: x % 2 == 1).take())

    def test_zip(self):
        from itertools import zip_longest
        self.assertListEqual(list(zip(self._array1, self._array2)), stream(self._array1).zip(self._array2).take())
        self.assertListEqual(list(zip_longest(self._array1, self._array2)),
                             stream(self._array1).zip_longest(self._array2).take())

    def test_skip(self):
        self.assertListEqual(self._array1[1:], stream(self._array1).skip(1).take())

    def test_reduce(self):
        self.assertEqual(sum(self._array1), stream(self._array1).reduce(operator.add))
