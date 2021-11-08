# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import tests


def prepare(source, pages, testdir, monkeypatch):
    # run rawmaker
    pages = f'--pages={pages}'
    tests.run(
        f'-i {source} -o {testdir.tmpdir} {pages} --text --fonts --images',
        monkeypatch=monkeypatch,
    )
    utila.run(f'figureo -i {source} '
              f'-i {testdir.tmpdir} -o {testdir.tmpdir} {pages}')
