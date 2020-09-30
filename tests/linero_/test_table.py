# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utila
import utilatest

import linero.cluster
import linero.features.table
import linero.path
import linero.table.crossed
import linero.table.word
import tests
import tests.linero_


def test_run_table(testdir, monkeypatch):  #pylint: disable=W0613
    cmd = f'-i {power.BOOK007_PDF} --line'
    tests.run(cmd, monkeypatch=monkeypatch)


@pytest.mark.parametrize('source, expected', [
    pytest.param(
        power.link(power.DOCU13_PDF),
        [0, 0, 1, 3, 3, 5, 2, 5, 6, 4, 5, 3, 1],
        id='vim',
    ),
])
def test_table_extract(source, expected):
    source = iamraw.path.line(source)
    loaded = serializeraw.load_lines(source)
    # add empty lines, cause pages without lines will be ignored, we
    # require this to check extraction result properly.
    loaded.insert(0, iamraw.PageContentLine(page=0, content=[]))
    tables = linero.table.crossed.run(loaded)

    flat = [len(item.content) for item in tables]
    assert flat == expected


def test_table_dump_and_load():
    source = iamraw.path.line(power.link(power.DOCU13_PDF))
    loaded = serializeraw.load_lines(source, pages=(0, 1, 2))
    grouped = linero.table.word.locate_tables(loaded)
    tables = linero.table.word.judge_tables(grouped)

    dumped = serializeraw.dump_tables(tables)
    loaded = serializeraw.load_tables(dumped)
    assert loaded == tables


def test_table_extract_negative():
    source = power.link(power.BOOK007_PDF)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    lines = iamraw.path.line(source)

    tables = linero.features.table.work(text, textposition, lines=lines)

    loaded = serializeraw.load_tables(tables)
    loaded = [item for item in loaded if item.content]
    assert not loaded, str(loaded)


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(
        power.link(power.BACHELOR090_PDF),
        '75:80',
        [1, 3, 3, 3],
        id='bachelor90',
        marks=pytest.mark.xfail(reason='improve horizontal check'),
    ),
    pytest.param(
        power.link(power.DOCU13_PDF),
        '2:7',
        [1, 3, 3, 5, 2],
        id='vimguide',
    ),
    pytest.param(
        power.link(power.DOCU13_PDF),
        '5',
        [5],
        id='vimguide_page5',
    ),
    pytest.param(
        power.link(power.BACHELOR056_PDF),
        '15,18',
        [1, 1],
        id='bachelor56_page15',
    ),
    pytest.param(
        power.link(power.BACHELOR056_PDF),
        '31',
        [2],
        id='bachelor56_page31',
    ),
    pytest.param(
        power.link(power.DOCU07_PDF),
        '0,1,2',
        [],
        id='notable_howto_pyporting',
    ),
    pytest.param(
        power.link(power.BACHELOR063_PDF),
        '25',
        [1],
        id='bachelor63_singletable',
    ),
])
@utilatest.skip_longrun
def test_detect_table(source, pages, expected, testdir, monkeypatch):
    tests.linero_.run(
        f'-i {source} --pages={pages} --table',
        monkeypatch=monkeypatch,
    )
    tables = linero.path.table(testdir.tmpdir)
    loaded = serializeraw.load_tables(tables)

    current = [len(item) for item in loaded]
    assert current == expected


def test_detect_table_bachelor90_page80(testdir, monkeypatch):
    """The table header contains only one connected textual string."""
    source = power.link(power.BACHELOR090_PDF)
    pages = '80'
    tests.linero_.run(
        f'-i {source} --pages={pages} --table',
        monkeypatch=monkeypatch,
    )

    tables = linero.path.table(testdir.tmpdir)
    loaded = serializeraw.load_tables(tables)[0].content

    assert len(loaded) == 1


def test_detect_table_master98_page54_60(testdir, monkeypatch):
    source = power.link(power.MASTER098_PDF)
    pages = '54:62'
    tests.linero_.run(
        f'-i {source} --pages={pages} --table',
        monkeypatch=monkeypatch,
    )

    tables = linero.path.table(testdir.tmpdir)

    loaded = serializeraw.load_tables(tables)

    assert len(utila.select_content(loaded, 54)) == 1
    assert len(utila.select_content(loaded, 55)) == 1

    assert len(utila.select_content(loaded, 58)) == 1
    assert len(utila.select_content(loaded, 59)) == 1
