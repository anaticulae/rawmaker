# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import rawmaker.cleanup.translate.lines
import tests


@utilatest.longrun
def test_translate_lines(testdir, monkeypatch):
    prepare(testdir, monkeypatch)
    # do not cache load_documents, do not use tests.cleanup.run
    utila.run('rawmaker_cleanup --cleanup --backup '
              f'-i {testdir.tmpdir} -o {testdir.tmpdir}')
    ptn = serializeraw.ptn_frompath(testdir.tmpdir)
    backup = serializeraw.ptn_frompath(testdir.tmpdir, backup=True)
    assert ptn != backup, 'cached load_documents? check backup=False'
    translated = rawmaker.cleanup.translate.lines.translates(backup, ptn)
    # changes on two pages, no change on page 22
    assert len(translated) == 2


def test_cleanup_translate(testdir, monkeypatch):
    prepare(testdir, monkeypatch)
    tests.cleanup.run(
        f'-i {testdir.tmpdir} -o {testdir.tmpdir}',
        monkeypatch=monkeypatch,
    )
    done = utila.file_list(
        testdir.tmpdir,
        recursive=False,
    )
    assert len(done) == 8


def prepare(testdir, monkeypatch):
    source = power.BACHELOR037_PDF
    pages = '--pages=22,23,24'
    # run rawmaker
    tests.run(
        f'-i {source} {pages} --text --fonts --images',
        monkeypatch=monkeypatch,
    )
    utila.run(f'figureo -i {source} '
              f'-i {testdir.tmpdir} -o {testdir.tmpdir} {pages}')
