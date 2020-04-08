# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

import tests
import tests.resources


def test_layout_fine_master72_page3_horizontal_problem(testdir, monkeypatch):
    """Ensure that horizontal line is parsed before first footer text
    line. There was a problem, cause the position of the first line was
    parsed with a to low y0 coordinate."""
    source = testdir.tmpdir
    cmd = f'-i {tests.resources.MASTER72} --text --boxes --pages=3'
    tests.run_success(cmd, monkeypatch=monkeypatch)

    navigators = serializeraw.create_pagetextnavigators_frompath(source)
    horizontal = serializeraw.load_horizontals(source)[0][0][0]
    firstpage = navigators[0]
    first_footer_line = firstpage[32]
    text = normalize_whitespaces(first_footer_line.text)
    assert text.startswith('1 Aus Gründen'), text
    msg = f'{first_footer_line} {horizontal}'
    assert first_footer_line.bounding.y0 > horizontal.box.y1, msg


@utila.refactor(major=1, minor=18, description='replace with utila code')
def normalize_whitespaces(text: str) -> str:
    """Remove unnecessary white spaces.

    >>> normalize_whitespaces(' make    me happy' + utila.NEWLINE)
    'make me happy'
    """
    return ' '.join(text.strip().split())
