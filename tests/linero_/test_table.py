# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import pytest

import linero.cluster
import linero.features.table
import rawmaker.features.line
import tests
import tests.resources


def test_run_table(testdir, monkeypatch):  #pylint: disable=W0613
    cmd = f'-i {tests.resources.BOOK} --line'
    tests.run_success(cmd, monkeypatch=monkeypatch)


@pytest.mark.parametrize('source, expected', [
    pytest.param(
        tests.resources.VIM_GENERATED,
        (1, 3, 3, 5, 2, 5, 6, 4, 5, 3, 1),
        id='vim',
    ),
])
def test_table_extract(source, expected):
    source = os.path.join(source, 'rawmaker__line_line.yaml')

    loaded = rawmaker.features.line.load_lines(source)
    grouped = linero.features.table.locate_tables(loaded)
    tables = linero.features.table.judge_tables(grouped)
    assert len(tables) == len(expected), f'{len(tables)} != {len(expected)}'


def test_table_dump_and_load():
    source = os.path.join(
        tests.resources.VIM_GENERATED,
        'rawmaker__line_line.yaml',
    )
    loaded = rawmaker.features.line.load_lines(source, pages=(0, 1, 2))
    grouped = linero.features.table.locate_tables(loaded)
    tables = linero.features.table.judge_tables(grouped)

    dumped = linero.features.table.dump_tables(tables)
    loaded = linero.features.table.load_tables(dumped)
    assert loaded == tables
