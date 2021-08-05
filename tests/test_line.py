# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import rawmaker.features.line
import rawmaker.reader
import tests


def test_line_run_cli(testdir, monkeypatch):  #pylint: disable=W0613
    root = str(testdir)
    cmd = f'-i {power.BOOK007_PDF} --line --annotation'
    with utilatest.increased_filecount(root, ext='yaml'):
        tests.run(cmd, monkeypatch=monkeypatch)


@utilatest.longrun
@pytest.mark.parametrize('source, expected', [
    pytest.param(
        power.DOCU13_PDF,
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
    with rawmaker.reader.read(power.DOCU09_PDF) as pdf:
        lines = rawmaker.features.line.determine_lines(pdf)

    dumped = serializeraw.dump_lines(lines)
    assert dumped, str(dumped)

    loaded = serializeraw.load_lines(dumped)
    assert loaded

    # TODO: MOVE THIS METHOD TO IAMRAW?
    # select content pages, cause dumping removes empty pages
    content_only = [item for item in lines if item.content]
    assert loaded == content_only


def test_line_merge_horizontals_bachelor90(testdir):
    pages = (13, 14)
    with rawmaker.reader.read(power.BACHELOR090_PDF) as pdf:
        lines = rawmaker.features.line.determine_lines(pdf, pages=pages)
    lines = utila.flatten([item.content for item in lines])
    assert len(lines) == 2


def test_curve_lines_bachelor90_page39(testdir):
    with rawmaker.reader.read(power.BACHELOR090_PDF) as pdf:
        lines = rawmaker.features.line.determine_lines(pdf, pages=39)
    lines = utila.flatten([item.content for item in lines])
    assert len(lines) == 8
