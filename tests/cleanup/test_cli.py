# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila

import rawmaker.cli_cleanup
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


@pytest.mark.parametrize('source, pages', [
    pytest.param(power.BACHELOR056_PDF, '0:10,20:25', id='partial'),
    pytest.param(power.BACHELOR056_PDF, '15', id='fifteen'),
    pytest.param(power.BACHELOR056_PDF, '27', id='27'),
    pytest.param(power.BACHELOR056_PDF, '5,6,7', id='fiveSixSeven'),
    pytest.param(power.BACHELOR056_PDF, ':', id='all'),
    pytest.param(power.BACHELOR051_PDF, ':', id='bachelor51_all'),
    pytest.param(power.HOME040_PDF, ':', id='home40'),
])
def test_cleanup_source_compare_reduction(
    source,
    pages,
    testdir,
    monkeypatch,
):
    """Ensure that resource is loaded and dumped correctly. This is
    required before we can test that cleanup reduces some data out of
    ptn."""
    source = power.link(source)
    utila.copy_content(
        source,
        testdir.tmpdir,
        pattern='(rawmaker__text|rawmaker__fonts)_*.yaml',
    )
    tests.cleanup.run(
        f'-i {testdir.tmpdir} -o {testdir.tmpdir} --postfix=cleaned --pages={pages}',
        monkeypatch=monkeypatch,
    )
    pages = utila.parse_pages(pages)
    ptn = serializeraw.ptn_frompath(
        testdir.tmpdir,
        pages=pages,
    )
    ptn_dumped = serializeraw.ptn_frompath(
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


def test_cleanup_figures(testdir, monkeypatch):
    """Remove text in figure area."""
    source = power.link(power.BACHELOR051_PDF)
    tests.cleanup.run(
        f'-i {source} -o {testdir.tmpdir}',
        monkeypatch=monkeypatch,
    )
    ptn = serializeraw.ptn_frompath(source)
    ptn_dumped = serializeraw.ptn_frompath(testdir.tmpdir)
    assert ptn_dumped != ptn
    before = utila.select_page(ptn, page=29)
    clean = utila.select_page(ptn_dumped, page=29)
    # remove 4 lines on page 29
    assert len(clean) + 4 == len(before)


def test_cleanup_tables(testdir, monkeypatch):
    """Verify multiple input soruces and tablero cleanup."""
    source = power.link(power.BACHELOR051_PDF)
    page = 25
    # create table to verify removing table content
    tables = [
        iamraw.PageContentTableBounding(
            page=page,
            content=[iamraw.TableBounding(bounding=(0, 0, 300, 300))],
        )
    ]
    dumped = serializeraw.dump_tables(tables)
    utila.file_create('tablero__decide_decide.yaml', dumped)
    # run cleanup
    tests.cleanup.run(
        f'-i {source} -i {testdir.tmpdir} -o {testdir.tmpdir} --pages={page}',
        monkeypatch=monkeypatch,
    )
    # load result
    ptn = serializeraw.ptn_frompath(source)
    ptn_dumped = serializeraw.ptn_frompath(testdir.tmpdir)
    assert ptn_dumped != ptn
    before = utila.select_page(ptn, page=page)
    clean = utila.select_page(ptn_dumped, page=page)
    # remove some lines due tablero
    assert len(before) == 55
    assert len(clean) == 42


def test_cleanup_backup(testdir, monkeypatch):
    """Copy source files as backup files(change data type)."""
    source = power.link(power.BACHELOR051_PDF)
    tests.cleanup.run(
        f'-i {source} -o {testdir.tmpdir} --backup',
        monkeypatch=monkeypatch,
    )
    # four backup files written
    backupfiles = utila.file_list(
        testdir.tmpdir,
        include=rawmaker.cli_cleanup.BACKUP_EXT,
    )
    assert len(backupfiles) == 6
