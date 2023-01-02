# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw
import utilatest

import tests.resources
import tests.spacestation_


# yapf:disable
@pytest.mark.parametrize('source, expected', [
    pytest.param(
        tests.resources.FONTS_SCALED_PERCENT033,
        ({}, {}, {}),
        id='percent033',
    ),
    pytest.param(
        tests.resources.FONTS_SCALED_PERCENT050,
        ({12.0: 1.41}, {12.0: 1.511}, {12.0: 1.67}),
        id='percent050',
    ),
    pytest.param(
        tests.resources.FONTS_SCALED_PERCENT200,
        ({12.0: 6.0}, {12.0: 10.88}, {12.0: 29.35}),
        id='percent200',
    ),
])
# yapf:enable
@utilatest.requires(tests.resources.FONTS_SCALED_PERCENT033)
@utilatest.requires(tests.resources.FONTS_SCALED_PERCENT050)
@utilatest.requires(tests.resources.FONTS_SCALED_PERCENT200)
def test_scaled_font_chardist(source, expected, td, mp):
    cmd = f'-i {source}'
    tests.spacestation_.run(cmd, mp=mp)
    worddist = serializeraw.load_document_worddist(td.tmpdir)
    current = worddist.minn, worddist.mean, worddist.maxx
    assert current == expected
