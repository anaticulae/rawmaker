# =============================================================================j
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

import spacestation.serialize
import tests.spacestation_


# yapf:disable
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR051_PDF, '3', (12.0, 3.939), id='bachelor51'),
    pytest.param(power.BACHELOR056_PDF, '3:40', (12.0, 7.481), id='bachelor56', marks=utilatest.longrun),
])
# yapf:enable
def test_worddist(source, pages, expected, testdir, monkeypatch):
    cmd = f'-i {source} --pages={pages} --wspace --worddist'
    # run
    tests.spacestation_.run(cmd, monkeypatch=monkeypatch)
    # load
    loaded = spacestation.serialize.load_document_worddist(testdir.tmpdir)
    # verify
    fontsize, chardist = expected
    # TODO: REPLACE WITH VERY NEAR
    assert utila.near(loaded.mean[fontsize], chardist, diff=0.01), str(loaded)
