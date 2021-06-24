# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hardcore
import pytest
import serializeraw

import tests

P50_SPD = """\
Sammelmappe2.pdf
    Europa
    Respekt
    Titel
    Zukunft\
"""


@pytest.mark.parametrize(
    'source, expected',
    [
        pytest.param(hardcore.H000_IMAGETEXT_6_PDF, 6, id='figuretext'),
        pytest.param(hardcore.P50_SPD, P50_SPD, id='spdfile'),
        pytest.param(hardcore.P100_GRUENE, None, id='gruene'),
        pytest.param(hardcore.P0_DRUCKSACHE1900302, None, id='drucksache19302'),
    ],
)
def test_imagetext_outlines(source, expected, testdir, monkeypatch):
    """Regression test to load outlines `FitH` correctly."""
    cmd = f'-i {source} --outlines'
    tests.run(cmd, monkeypatch=monkeypatch)
    source = os.path.join(testdir.tmpdir, 'rawmaker__outlines_outlines.yaml')
    assert os.path.exists(source)
    loaded = serializeraw.load_toc(source)
    assert any((
        len(loaded) == expected,
        str(loaded) == expected,
        expected is None,
    ))
