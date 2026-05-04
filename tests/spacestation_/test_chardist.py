# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import tests.spacestation_


# yapf:disable
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(hoverpower.BACHELOR051_PDF, '3', (12.0, 0.0), id='bachelor51'),
    pytest.param(hoverpower.BACHELOR056_PDF, '4', (11.25, -0.198), id='bachelor56'),
    pytest.param(hoverpower.MASTER116_PDF, '20:50', (10.91, -0.022), id='master116', marks=utilotest.nightly),
    pytest.param(hoverpower.MASTER116_PDF, '8', (10.91, -0.022), id='shormaster116'),
])
@utilotest.longrun
# yapf:enable
def test_chardist(source, pages, expected, td, mp):
    cmd = f'-i {source} --pages={pages} --wspace --chardist'
    # run
    tests.spacestation_.run(cmd, mp=mp)
    # load
    loaded = serializeraw.load_document_chardist(td.tmpdir)
    # verify
    fontsize, chardist = expected
    assert utilo.near(loaded.mean[fontsize], chardist, diff=0.01), str(loaded)
