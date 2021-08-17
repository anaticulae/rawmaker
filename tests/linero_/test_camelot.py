# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import linero.camelox.fork
import linero.table.camelox


def test_camelot_run():
    source = power.DOCU013_PDF
    parsed = linero.table.camelox.run(source, pages=2)
    assert len(parsed) == 1


@utilatest.longrun
@pytest.mark.xfail(reason='adjust camelot strategy')
def test_camelot_forked():
    source = power.DOCU013_PDF
    parsed = linero.camelox.fork.run(source, worker=4)
    flatten = utila.flatten_content(parsed)
    assert len(flatten) == 38


def test_camelot_latex():
    source = power.BACHELOR090_PDF
    parsed = linero.table.camelox.run(source, pages=76)
    assert len(parsed) == 1
