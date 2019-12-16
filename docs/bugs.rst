bugs
====

open
----

Run with multiple cores
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

    rawmaker -j8 -i ../2020_Book_BiologicallyInspiredCognitiveA.pdf

    [ERROR] Unhandeld annotation A {'AP': {'N': <PDFObjRef:16052>}, 'Border': [0, 0, 0], 'Dest': b'page.137', 'F': 4, 'Rect': [308.409, 420.151, 321.109, 428.655], 'Subtype': /'Link', 'Type': /'Annot'}
    completed: rawmaker
    [ERROR] CondIt
    [ERROR] Traceback (most recent call last):
      File "C:/usr/python/372/lib/site-packages/utila/feature.py", line 280, in run_hook_safely
        result = hook(pages=pages)
      File "c:/kiwi/kiwi/rawmaker/rawmaker/features/fonts.py", line 136, in work
        header, content = parse_fonts(document)
      File "c:/kiwi/kiwi/rawmaker/rawmaker/features/fonts.py", line 234, in parse_fonts
        content = [process_page(page, fontstore) for page in document.pages]
      File "c:/kiwi/kiwi/rawmaker/rawmaker/features/fonts.py", line 234, in <listcomp>
        content = [process_page(page, fontstore) for page in document.pages]
      File "c:/kiwi/kiwi/rawmaker/rawmaker/features/fonts.py", line 211, in process_page
        fontstore,
      File "c:/kiwi/kiwi/rawmaker/rawmaker/features/fonts.py", line 241, in determine_font
        fontkey = fontstore.font_key(font, scale)
      File "c:/kiwi/kiwi/rawmaker/rawmaker/features/fonts.py", line 151, in font_key
        parsed = self.parser(raw_font, scale)
      File "c:/kiwi/kiwi/rawmaker/rawmaker/features/fonts.py", line 323, in font_fromraw
        assert '+' not in fontname, msg
    AssertionError: detected fontname AdvTTec369687+01; input material ADDAON+AdvTTec369687+01

    [ERROR] while processing rawmaker
    [ERROR] detected fontname AdvTTec369687+01; input material ADDAON+AdvTTec369687+01
    [ERROR] rawmaker failed
    completed: rawmaker
    completed: rawmaker
    Process SpawnProcess-3:
    Traceback (most recent call last):
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 297, in _bootstrap
        self.run()
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 99, in run
        self._target(*self._args, **self._kwargs)
      File "C:\usr\python\372\lib\concurrent\futures\process.py", line 226, in _process_worker
        call_item = call_queue.get(block=True)
      File "C:\usr\python\372\lib\multiprocessing\queues.py", line 92, in get
        with self._rlock:
      File "C:\usr\python\372\lib\multiprocessing\synchronize.py", line 95, in __enter__
        return self._semlock.__enter__()
    KeyboardInterrupt
    Process SpawnProcess-5:
    Traceback (most recent call last):
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 297, in _bootstrap
        self.run()
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 99, in run
        self._target(*self._args, **self._kwargs)
      File "C:\usr\python\372\lib\concurrent\futures\process.py", line 226, in _process_worker
        call_item = call_queue.get(block=True)
      File "C:\usr\python\372\lib\multiprocessing\queues.py", line 92, in get
        with self._rlock:
      File "C:\usr\python\372\lib\multiprocessing\synchronize.py", line 95, in __enter__
        return self._semlock.__enter__()
    KeyboardInterrupt
    Process SpawnProcess-8:
    Traceback (most recent call last):
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 297, in _bootstrap
        self.run()
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 99, in run
        self._target(*self._args, **self._kwargs)
      File "C:\usr\python\372\lib\concurrent\futures\process.py", line 226, in _process_worker
        call_item = call_queue.get(block=True)
      File "C:\usr\python\372\lib\multiprocessing\queues.py", line 92, in get
        with self._rlock:
      File "C:\usr\python\372\lib\multiprocessing\synchronize.py", line 95, in __enter__
        return self._semlock.__enter__()
    KeyboardInterrupt
    Process SpawnProcess-6:
    Traceback (most recent call last):
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 297, in _bootstrap
        self.run()
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 99, in run
        self._target(*self._args, **self._kwargs)
      File "C:\usr\python\372\lib\concurrent\futures\process.py", line 226, in _process_worker
        call_item = call_queue.get(block=True)
      File "C:\usr\python\372\lib\multiprocessing\queues.py", line 92, in get
        with self._rlock:
      File "C:\usr\python\372\lib\multiprocessing\synchronize.py", line 95, in __enter__
        return self._semlock.__enter__()
    KeyboardInterrupt
    Process SpawnProcess-2:
    Traceback (most recent call last):
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 297, in _bootstrap
        self.run()
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 99, in run
        self._target(*self._args, **self._kwargs)
      File "C:\usr\python\372\lib\concurrent\futures\process.py", line 226, in _process_worker
        call_item = call_queue.get(block=True)
      File "C:\usr\python\372\lib\multiprocessing\queues.py", line 93, in get
        res = self._recv_bytes()
      File "C:\usr\python\372\lib\multiprocessing\connection.py", line 216, in recv_bytes
        buf = self._recv_bytes(maxlength)
      File "C:\usr\python\372\lib\multiprocessing\connection.py", line 306, in _recv_bytes
        [ov.event], False, INFINITE)
    KeyboardInterrupt
    Process SpawnProcess-7:
    Traceback (most recent call last):
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 297, in _bootstrap
        self.run()
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 99, in run
        self._target(*self._args, **self._kwargs)
      File "C:\usr\python\372\lib\concurrent\futures\process.py", line 226, in _process_worker
        call_item = call_queue.get(block=True)
      File "C:\usr\python\372\lib\multiprocessing\queues.py", line 93, in get
        res = self._recv_bytes()
      File "C:\usr\python\372\lib\multiprocessing\connection.py", line 216, in recv_bytes
        buf = self._recv_bytes(maxlength)
      File "C:\usr\python\372\lib\multiprocessing\connection.py", line 306, in _recv_bytes
        [ov.event], False, INFINITE)
    KeyboardInterrupt
    Process SpawnProcess-1:
    Traceback (most recent call last):
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 297, in _bootstrap
        self.run()
      File "C:\usr\python\372\lib\multiprocessing\process.py", line 99, in run
        self._target(*self._args, **self._kwargs)
      File "C:\usr\python\372\lib\concurrent\futures\process.py", line 226, in _process_worker
        call_item = call_queue.get(block=True)
      File "C:\usr\python\372\lib\multiprocessing\queues.py", line 93, in get
        res = self._recv_bytes()
      File "C:\usr\python\372\lib\multiprocessing\connection.py", line 216, in recv_bytes
        buf = self._recv_bytes(maxlength)
      File "C:\usr\python\372\lib\multiprocessing\connection.py", line 306, in _recv_bytes
        [ov.event], False, INFINITE)
    KeyboardInterrupt

    Operation cancelled by user

closed
------
