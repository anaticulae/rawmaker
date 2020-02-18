# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import pytest
import utila

import rawmaker.features.line
import rawmaker.reader
import tests
import tests.resources


def test_line_run_cli(testdir, monkeypatch):  #pylint: disable=W0613
    root = str(testdir)
    cmd = f'-i {tests.resources.BOOK} --line'
    with utila.increased_filecount(root, ext='yaml'):
        tests.run_success(cmd, monkeypatch=monkeypatch)


@pytest.mark.parametrize('source, expected', [
    pytest.param(
        tests.resources.VIM_PDF,
        (0, 1, 1, 3, 3, 5, 2, 5, 6, 4, 5, 3, 2),
        id='vim',
    ),
])
def test_line_extract(source, expected):
    with rawmaker.reader.read(source) as pdf:
        lines = rawmaker.features.line.determine_lines(pdf)
    assert len(lines) == len(expected), f'{len(lines)} != {len(expected)}'

    validated = [
        len(page.content) >= page_expected
        for page, page_expected in zip(lines, expected)
    ]
    assert all(validated), str(validated)


def test_line_dump_load():
    with rawmaker.reader.read(tests.resources.HOW_TO_CPORTING_PDF) as pdf:
        lines = rawmaker.features.line.determine_lines(pdf)

    dumped = rawmaker.features.line.dump_lines(lines)
    assert dumped, str(dumped)

    loaded = rawmaker.features.line.load_lines(dumped)
    assert loaded

    assert loaded == lines
