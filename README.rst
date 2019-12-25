circular-buffer
===============
   
|Tests| |PyPi|

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

Remember to install `numba` JIT compiler package to get a small extra speedup. `numba` can be 
automatically installed if you install this package via :code:`pip install circular-buffer[numba]`.

.. |Tests| image:: https://github.com/leftys/circular-buffer/workflows/Tests/badge.svg
.. |PyPi| image:: https://badge.fury.io/py/circular-buffer.svg
   :target: https://pypi.python.org/pypi/circular-buffer/
