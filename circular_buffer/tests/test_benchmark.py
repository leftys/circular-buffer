import pytest
import numpy as np

from .. import circular_buffer



def buffer_of_int_type():
    return circular_buffer.for_instances_like(123)

def benchmark_body(buffer_of_int_type):
    b = buffer_of_int_type(size = 10, autoexpand = False)
    for i in range(1000):
        b.push_back(i)
        if i % 10 == 0:
            b.pop_front()

def test_benchmark(benchmark):
    benchmark(benchmark_body, buffer_of_int_type())

