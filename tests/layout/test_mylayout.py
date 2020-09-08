# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.path
import power
import serializeraw

import tests


def test_mylayout_bachelor90_page53(testdir, monkeypatch):
    source = power.BACHELOR090_PDF
    cmd = f'-i {source} --text --pages=53'
    tests.run(cmd, monkeypatch=monkeypatch)

    document = serializeraw.load_document(iamraw.path.text(testdir.tmpdir))

    page53_second_line = document[0][1].text.strip()
    assert page53_second_line == '4.3. Übersicht der praktischen Entwicklung'
