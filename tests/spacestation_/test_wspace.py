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
import utilotest

import spacestation
import spacestation.features.wspace
import tests.spacestation_


def test_wspace_extract_bachelor56page0():
    source = hoverpower.BACHELOR056_PDF
    extracted, _ = spacestation.features.wspace.extract(source, (0,))
    extracted = extracted[0].content
    assert len(extracted) == 42  # VALIDATED!


@pytest.mark.parametrize('page, expected', [
    (7, 300),
    (9, 287),
])
def test_wspace_extract_diss266pagex(page, expected):
    source = hoverpower.DISS266_PDF
    extracted, _ = spacestation.features.wspace.extract(source, (page,))
    extracted = extracted[0].content
    assert len(extracted) == expected  # VALIDATED!


@utilotest.nightly
def test_wspace_cli_bachelor56(td, mp):
    source = hoverpower.BACHELOR056_PDF
    cmd = f'-i {source}'
    tests.spacestation_.run(cmd, mp=mp)
    loaded = serializeraw.load_wspaces(td.tmpdir)
    assert loaded
