from typing import Any
import warnings

import numpy as np
try:
    from numba import jitclass, types, typeof
    NUMBA = True
except ImportError:
    from .numba_mock import jitclass, types, typeof
    NUMBA = False


 
def for_instances_like(instance_example: Any, warn_if_not_compiled: bool = False) -> 'CircularBuffer':
    @jitclass([
        ('_buffer', types.Array(typeof(instance_example), ndim = 1, layout = 'C')),
        ('_first_position', types.int64),
        ('_last_position', types.int64),
        ('pushed_count', types.int64),
        ('size', types.int64),
        ('autoexpand', types.boolean),
    ])
    class CircularBuffer:
        ''' 
        Efficient implementation of circular buffer for numeric types.

        Cache friendly implementation. Support for fixed size or automatic expanson and memory reallocation.
        '''
        # TODO: ability to shrink after contents were very short for a long time (amount of pushes)
        def __init__(self, size: int = 10, *, autoexpand: bool = True) -> None:
            if size >= 2**32:
                raise ValueError()
            self._buffer = np.zeros(size, dtype = type(instance_example))
            self._first_position = 0
            self._last_position = -1
            self.pushed_count = 0
            self.size = size
            self.autoexpand = autoexpand

        def push_back(self, value: Any) -> None:
            if self.autoexpand and self.pushed_count == self.size:
                self.expand(2 * self.size)

            self._last_position += 1
            self._last_position %= self.size
            self._buffer[self._last_position] = value
            self.pushed_count += 1
            if self.pushed_count > self.size:
                self.pushed_count = self.size
            if self._last_position == self._first_position and self.pushed_count != 1:
                self._first_position += 1
            self._first_position %= self.size

        def pop_front(self) -> Any:
            if self.pushed_count == 0:
                raise ValueError()

            value = self._buffer[self._first_position]
            self._first_position += 1
            self.pushed_count -= 1
            return value

        def get(self, position: int) -> Any:
            if position > self.pushed_count:
                raise KeyError()
            buffer_position = position
            if position < 0:
                buffer_position += self.pushed_count
            if position < 0:
                raise KeyError()
            buffer_position += self._first_position
            if buffer_position > self.size:
                buffer_position -= self.size

            return self._buffer[buffer_position]

        def back(self) -> Any:
            return self._buffer[self._last_position]

        def front(self) -> Any:
            return self._buffer[self._first_position]

        def expand(self, new_size: int) -> None:
            ''' Only expansion when the buffer is full and to at least twice the size is supported. '''
            # Old state (F = first, L = last):
            # |xxxxxxLFxxxxxxxxx| or
            # |FxxxxxxxxxxxxxxxL|
            # New state:
            # |       FxxxxxxxxxxxxxxxL            | or
            # |FxxxxxxxxxxxxxxxL                   |
            assert new_size >= 2 * self.size, \
                'Only expansion to at least twice the size is supported'
            assert (
                self._first_position - 1 == self._last_position 
                or self._last_position == self.size - 1
            ), 'Buffer must be full before expansion'
            # self._buffer.resize(new_size) # Resize is not supported by Numba
            new_buffer = np.zeros(new_size, dtype = type(instance_example))
            if self._first_position == 0:
                new_buffer[:self.size] = self._buffer[:]
            else:
                new_buffer[self.size:self.size + self._first_position] = self._buffer[:self._first_position]
                new_buffer[self._first_position:self.size] = self._buffer[self._first_position:self.size]
            self._buffer = new_buffer
            self._last_position = self.size + self._first_position - 1
            self.size = new_size

    if not NUMBA and warn_if_not_compiled:
        warnings.warn('Numba not installed, install it or set warn_if_not_compiled=False to use non-compiled Python version')
    return CircularBuffer

