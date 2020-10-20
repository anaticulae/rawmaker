# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila

import tests


def test_horizontals_master110_page19(testdir, monkeypatch):
    """Ensure that lines in figures are accepted as correct horizontal
    lines."""
    cmd = f'-i {power.MASTER110_PDF} --pages=19 --horizontals'
    tests.run(cmd, monkeypatch=monkeypatch)
    horizontals = serializeraw.load_horizontals(testdir.tmpdir)
    horizontals = utila.select_content(horizontals, page=19)
    assert len(horizontals) == 2, str(horizontals)


def test_horizontals_master155_page1(testdir, monkeypatch):
    cmd = f'-i {power.MASTER155_PDF} --pages=1 --horizontals'
    tests.run(cmd, monkeypatch=monkeypatch)
    horizontals = serializeraw.load_horizontals(testdir.tmpdir)
    horizontals = utila.select_content(horizontals, page=1)
    assert len(horizontals) == 1, str(horizontals)
