# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila

import tests.cleanup


def test_run_cleanup(monkeypatch):
    tests.cleanup.run('--help', monkeypatch=monkeypatch)


def test_cleanup_bachelor56(testdir, monkeypatch):
    source = power.link(power.BACHELOR056_PDF)
    utila.copy_content(
        source,
        testdir.tmpdir,
        pattern='(rawmaker__text|rawmaker__fonts)_*.yaml',
    )
    tests.cleanup.run(
        '-i . -o . --postfix=cleaned --pages=0',
        monkeypatch=monkeypatch,
    )
    assert len(utila.file_list(testdir.tmpdir)) == 8


@pytest.mark.parametrize('pages', [
    pytest.param('0:10,20:25', id='partial'),
    pytest.param('15', id='fifteen'),
    pytest.param('27', id='27'),
    pytest.param('5,6,7', id='fiveSixSeven'),
    pytest.param(':', id='all'),
])
def test_cleanup_bachelor56_compare_reduction(pages, testdir, monkeypatch):
    source = power.link(power.BACHELOR056_PDF)
    utila.copy_content(
        source,
        testdir.tmpdir,
        pattern='(rawmaker__text|rawmaker__fonts)_*.yaml',
    )
    tests.cleanup.run(
        f'-i . -o . --postfix=cleaned --pages={pages}',
        monkeypatch=monkeypatch,
    )
    pages = utila.parse_pages(pages)
    ptn = serializeraw.create_pagetextnavigators_frompath(
        testdir.tmpdir,
        pages=pages,
    )
    ptn_dumped = serializeraw.create_pagetextnavigators_frompath(
        testdir.tmpdir,
        prefix='cleaned',
        pages=pages,
    )
    assert ptn_dumped == ptn
    fontstore = serializeraw.create_fontstore_frompath(
        testdir.tmpdir,
        pages=pages,
    )
    fontstore_dumped = serializeraw.create_fontstore_frompath(
        testdir.tmpdir,
        prefix='cleaned',
        pages=pages,
    )
    assert fontstore_dumped.pages == fontstore.pages
    assert fontstore_dumped.header == fontstore.header
