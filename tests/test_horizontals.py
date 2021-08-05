# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import serializeraw
import utila

import tests


def test_horizontals_master110_page19(testdir, monkeypatch):
    """Ensure that lines in figures are accepted as correct horizontal
    lines."""
    cmd = f'-i {power.MASTER110_PDF} --pages=19 --line --horizontals --annotation'
    tests.run(cmd, monkeypatch=monkeypatch)
    horizontals = serializeraw.load_horizontals(testdir.tmpdir)
    horizontals = utila.select_content(horizontals, page=19)
    assert len(horizontals) == 2, str(horizontals)


def test_horizontals_master155_page1(testdir, monkeypatch):
    cmd = f'-i {power.MASTER155_PDF} --pages=1 --line --horizontals --annotation'
    tests.run(cmd, monkeypatch=monkeypatch)
    horizontals = serializeraw.load_horizontals(testdir.tmpdir)
    horizontals = utila.select_content(horizontals, page=1)
    assert len(horizontals) == 1, str(horizontals)


def test_lines_bachelor63_page10(testdir, monkeypatch):
    cmd = f'-i {power.BACHELOR063_PDF} --pages=10 --line --annotation'
    tests.run(cmd, monkeypatch=monkeypatch)
    lines = serializeraw.load_lines(iamraw.path.line(testdir.tmpdir))
    lines = utila.select_content(lines, page=10)
    assert len(lines) == 46


def test_lines_master72_hyperlinks_as_line(testdir, monkeypatch):
    cmd = f'-i {power.MASTER072_PDF} --pages=65 --line --annotation'
    tests.run(cmd, monkeypatch=monkeypatch)
    lines = serializeraw.load_lines(testdir.tmpdir)
    assert not lines, 'hyperlink underlines missparsed as lines'


def test_lines_master75_hyperlinks_as_line(testdir, monkeypatch):
    cmd = f'-i {power.MASTER075_PDF} --pages=6 --line --annotation'
    tests.run(cmd, monkeypatch=monkeypatch)
    lines = serializeraw.load_lines(testdir.tmpdir)[0].content
    assert len(lines) == 2, 'header and footer line, but no underline'
