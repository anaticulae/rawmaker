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
import utilatest

import spacestation
import spacestation.serialize
import spacestation.wspace
import tests.spacestation_


def test_wspace_extract_bachelor56_page0():
    source = power.BACHELOR056_PDF
    extracted = spacestation.wspace.extract(source, (0,))
    extracted = extracted[0].content
    assert len(extracted) == 42  # VALIDATED!


@pytest.mark.parametrize('page, expected', [
    (7, 300),
    (9, 287),
])
def test_wspace_extract_diss266_pagex(page, expected):
    source = power.DISS266_PDF
    extracted = spacestation.wspace.extract(source, (page,))
    extracted = extracted[0].content
    assert len(extracted) == expected  # VALIDATED!


@utilatest.longrun
def test_wspace_cli_bachelor56(testdir, monkeypatch):
    source = power.BACHELOR056_PDF
    cmd = f'-i {source}'
    tests.spacestation_.run(cmd, monkeypatch=monkeypatch)
    path = spacestation.path.wspace(testdir.tmpdir)
    loaded = spacestation.serialize.load_wspaces(path)
    assert loaded
