# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import tests.spacestation_


# yapf:disable
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR051_PDF, '3', (12.0, 0.0), id='bachelor51'),
    pytest.param(power.BACHELOR056_PDF, '4', (11.25, -0.198), id='bachelor56'),
    pytest.param(power.MASTER116_PDF, '20:50', (10.91, -0.022), id='master116', marks=utilatest.nightly),
    pytest.param(power.MASTER116_PDF, '8', (10.91, -0.022), id='shormaster116'),
])
@utilatest.longrun
# yapf:enable
def test_chardist(source, pages, expected, td, mp):
    cmd = f'-i {source} --pages={pages} --wspace --chardist'
    # run
    tests.spacestation_.run(cmd, mp=mp)
    # load
    loaded = serializeraw.load_document_chardist(td.tmpdir)
    # verify
    fontsize, chardist = expected
    assert utila.near(loaded.mean[fontsize], chardist, diff=0.01), str(loaded)
