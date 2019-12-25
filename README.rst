circular-buffer
===============

Efficient circular buffer implementation in Python with optional Numba JIT compilation


Usage
-----

.. code-block:: python

    import circular_buffer

    buffer_of_int_type = circular_buffer.for_instances_like(123)
    buf = buffer_of_int_type(size = 10, autoexpand = True)
    for i in range(12):
        buf.push_back(i)
    assert buf.pop_front() == 0
    assert buf.front() == 1
    assert buf.back() == 11

Remember to install `numba` JIT compiler package to get a significant speedup.
