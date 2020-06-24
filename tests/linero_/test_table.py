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
import utilatest

import linero.cluster
import linero.features.table
import linero.path
import tests
import tests.linero_
import tests.resources


def test_run_table(testdir, monkeypatch):  #pylint: disable=W0613
    cmd = f'-i {tests.resources.BOOK} --line'
    tests.run(cmd, monkeypatch=monkeypatch)


@pytest.mark.parametrize('source, expected', [
    pytest.param(
        power.link(power.DOCU13_PDF),
        (1, 3, 3, 5, 2, 5, 6, 4, 5, 3, 1),
        id='vim',
    ),
])
@utilatest.skip_nightly
def test_table_extract(source, expected):
    source = iamraw.path.line(source)
    loaded = serializeraw.load_lines(source)
    grouped = linero.features.table.locate_tables(loaded)
    tables = linero.features.table.judge_tables(grouped)
    assert len(tables) == len(expected), f'{len(tables)} != {len(expected)}'


def test_table_dump_and_load():
    source = iamraw.path.line(power.link(power.DOCU13_PDF))
    loaded = serializeraw.load_lines(source, pages=(0, 1, 2))
    grouped = linero.features.table.locate_tables(loaded)
    tables = linero.features.table.judge_tables(grouped)

    dumped = serializeraw.dump_tables(tables)
    loaded = serializeraw.load_tables(dumped)
    assert loaded == tables


def test_table_extract_negative():
    source = power.link(power.BOOK007_PDF)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    horizontals = iamraw.path.horizontals(source)

    tables = linero.features.table.work(
        text,
        textposition,
        horizontals=horizontals,
    )

    loaded = serializeraw.load_tables(tables)
    assert not loaded, str(loaded)


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(
        power.link(power.BACHELOR090_PDF),
        '75:80',
        [1, 3, 3, 3],
        id='bachelor90',
    ),
    pytest.param(
        power.link(power.DOCU13_PDF),
        '2:7',
        [1, 3, 3, 5, 2],
        id='vimguide',
        marks=pytest.mark.xfail(reason='improve horizontal check'),
    ),
    pytest.param(
        power.link(power.BACHELOR056_PDF),
        '15',
        [1],
        id='bachelor56',
        marks=pytest.mark.xfail(reason='improve horizontal check'),
    ),
])
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
