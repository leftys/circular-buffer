import pytest
import numpy as np

from .. import circular_buffer



@pytest.fixture(scope = 'module')
def buffer_of_int_type():
    return circular_buffer.for_instances_like(123)

def test_buffer(buffer_of_int_type):
    b = buffer_of_int_type(size = 10, autoexpand = False)
    for i in range(12):
        b.push_back(i)
    assert b.pushed_count == 10
    assert b.pop_front() == 2
    assert b.front() == 3
    assert b.back() == 11
    assert b.pushed_count == 9
    assert b.size == 10
    assert list(b._buffer) == [10, 11,  2,  3,  4,  5,  6,  7,  8,  9]

def test_buffer_autoexpand(buffer_of_int_type):
    b = buffer_of_int_type(size = 10, autoexpand = True)
    for i in range(12):
        b.push_back(i)
    assert b.pop_front() == 0
    assert b.front() == 1
    assert b.back() == 11
    assert b.size == 20
    assert list(b._buffer) == [0, 1, 2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 0, 0, 0, 0, 0, 0, 0, 0]

def test_buffer_explicit_expand(buffer_of_int_type):
    b = buffer_of_int_type(size = 10, autoexpand = False)
    for i in range(12):
        b.push_back(i)
    b.expand(30)
    assert b.front() == 2
    assert b.back() == 11
    assert list(b._buffer) == [ 0,  0,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
