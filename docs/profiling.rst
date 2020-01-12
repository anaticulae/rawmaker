profiling
=========

Profiling rawmaker aims to reduces execution time. As a result of
profiling we can asume that improving `pdfminer` makes no sense.

Therefore we decide to run rawmaker multiple times with smaller chunks
to reduce execution time.

how to profile
--------------

run profiler
~~~~~~~~~~~~

.. code-block:: none

    python -m cProfile -o result.bin -m rawmaker -i
    tests/resources/master/page_116_images_toc_formular.pdf --text

view result
~~~~~~~~~~~

.. code-block:: python

    import pstats

    result = pstats.Stats('result.bin')
    result.sort_stats('tottime')
    result.print_stats()
