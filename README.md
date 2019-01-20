# Streamer

Simple package that provides a simple way to interact with iterable objects in more fluent way.

Example:

```python
from streamer import stream

stream([1, 2, 3, 4]) \
    .map(lambda x: x ** 2) \
    .take()
```