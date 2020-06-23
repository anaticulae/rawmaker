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
import tests
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
    source = iamraw.path.line(source)

    tables = linero.features.table.work(source)

    loaded = serializeraw.load_tables(tables)
    assert not loaded, str(loaded)
