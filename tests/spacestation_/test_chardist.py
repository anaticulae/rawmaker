# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila

import spacestation.serialize
import tests.spacestation_


def test_chardist(testdir, monkeypatch):
    source = power.BACHELOR051_PDF
    cmd = f'-i {source} --pages=3'
    tests.spacestation_.run(cmd, monkeypatch=monkeypatch)

    normal = spacestation.serialize.load_document_chardist(testdir.tmpdir)
    assert utila.near(normal.mean[12.0], 0.0, diff=0.01)

    source = power.BACHELOR056_PDF
    cmd = f'-i {source} --pages=4'
    tests.spacestation_.run(cmd, monkeypatch=monkeypatch)

    tide = spacestation.serialize.load_document_chardist(testdir.tmpdir)
    assert utila.near(tide.mean[11.25], -0.198, diff=0.01)
