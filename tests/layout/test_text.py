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


def test_bachelor63_text_extraction(testdir, monkeypatch):
    """This is a regression test, which ensure that a `pdfminer` bug
    does no occurs again. There was a problem that some text was parsed
    twice and more."""
    root = testdir.tmpdir
    source = power.BACHELOR063_PDF
    config = ''
    cmd = f'-i {source} --text --pages=0 {config}'
    tests.run(cmd, monkeypatch=monkeypatch)

    navigator = serializeraw.create_pagetextnavigators_frompath(root)[0]
    text = [str(item).strip() for item in navigator]
    unique = utila.make_unique(text)
    assert len(unique) == len(text), str(text)
