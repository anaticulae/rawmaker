# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

import tests


def test_horizontals_master110page19(td, mp):
    """Ensure that lines in figures are accepted as correct horizontal
    lines."""
    cmd = f'-i {power.MASTER110_PDF} --pages=19 --line --horizontals --annotation'
    tests.run(cmd, mp=mp)
    horizontals = serializeraw.load_horizontals(td.tmpdir)
    horizontals = utila.select_content(horizontals, page=19)
    assert len(horizontals) == 2, str(horizontals)


def test_horizontals_master155page1(td, mp):
    cmd = f'-i {power.MASTER155_PDF} --pages=1 --line --horizontals --annotation'
    tests.run(cmd, mp=mp)
    horizontals = serializeraw.load_horizontals(td.tmpdir)
    horizontals = utila.select_content(horizontals, page=1)
    assert len(horizontals) == 1, str(horizontals)


def test_horizontals_rotated_master116(td, mp):
    cmd = f'-i {power.MASTER116_PDF} --pages=102 --line --horizontals'
    tests.run(cmd, mp=mp)
    horizontals = serializeraw.load_horizontals(td.tmpdir, pages=(102,))
    horizontals = horizontals[0].content
    assert len(horizontals) == 2, str(horizontals)


def test_horizontals_not_rotated_bachelor026p16(td, mp):
    """Do not detect vertical lines as horizontals."""
    cmd = f'-i {power.BACHELOR026_PDF} --pages=16 --line --horizontals'
    tests.run(cmd, mp=mp)
    horizontals = serializeraw.load_horizontals(td.tmpdir, pages=(16,))
    # TODO: VERIFY WHY REAL HORIZONAL ARE NOT HANDELD AS HORIZONTAL
    assert not horizontals


@utilatest.longrun
def test_lines_bachelor63page10(td, mp):
    cmd = f'-i {power.BACHELOR063_PDF} --pages=10 --line --annotation'
    tests.run(cmd, mp=mp)
    lines = serializeraw.load_lines(iamraw.path.line(td.tmpdir))
    lines = utila.select_content(lines, page=10)
    assert len(lines) == 46


def test_lines_master72_hyperlinks_as_line(td, mp):
    cmd = f'-i {power.MASTER072_PDF} --pages=65 --line --annotation'
    tests.run(cmd, mp=mp)
    lines = serializeraw.load_lines(td.tmpdir)
    assert not lines, 'hyperlink underlines missparsed as lines'


def test_lines_master75_hyperlinks_as_line(td, mp):
    cmd = f'-i {power.MASTER075_PDF} --pages=6 --line --annotation'
    tests.run(cmd, mp=mp)
    lines = serializeraw.load_lines(td.tmpdir)[0].content
    assert len(lines) == 2, 'header and footer line, but no underline'


def test_lines_bachelor028p2_hyperlinks_as_line(td, mp):
    cmd = f'-i {power.BACHELOR028_PDF} --pages=2 --line --annotation'
    tests.run(cmd, mp=mp)
    lines = serializeraw.load_lines(td.tmpdir)[0].content
    assert len(lines) == 1, 'footer line, but no underline'


def test_lines_master099c(td, mp):
    """Ensure that text and horizontals are not merged together."""
    cmd = f'-i {power.MASTER099C_PDF} --pages=7,8,9,10,80,81,82 --line --horizontals'
    tests.run(cmd, mp=mp)
    lines = serializeraw.load_horizontals(td.tmpdir)
    boundings = []
    for page in lines:
        boundings.append((page.page, page.content[0].box[3]))
    # page, horizontal y1 bounding
    expected = [
        (7, 618.6),
        (8, 630.12),
        (9, 590.34),
        (10, 709.44),
        (80, 699.12),
        (81, 728.22),
        (82, 641.64),
    ]
    assert boundings == expected


@pytest.mark.xfail(reason='not feasible in the moment')
def test_lines_bachelor032p3(td, mp):
    """Black line under black hyperlink is not feasible with current
    technique.
    """
    cmd = f'-i {power.BACHELOR032_PDF} --pages=3 --line'
    tests.run(cmd, mp=mp)
    lines = serializeraw.load_lines(td.tmpdir)[0].content
    assert len(lines) == 2, 'footer line, and marked error line from teacher'
