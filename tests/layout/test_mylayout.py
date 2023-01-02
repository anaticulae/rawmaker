# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hardcore
import power
import serializeraw
import utilatest

import tests


def test_mylayout_bachelor90page53(td, mp):
    source = power.BACHELOR090_PDF
    cmd = f'-i {source} --text --pages=53'
    tests.run(cmd, mp=mp)
    # load
    document = serializeraw.load_document(td.tmpdir)
    # verify
    page53_second_line = document[0][1].text.strip()
    assert page53_second_line == '4.3. Übersicht der praktischen Entwicklung'


@utilatest.longrun
def test_mylayout_bounding_extraction_bug(td, mp):
    """Without sorting the boundings before connecting them by mylayout,
    the result is that the left x0 is greater than right x1. This is a
    result of merging non neighbored boundings."""
    source = td.tmpdir
    cmd = f'-i {hardcore.H300_SPHINX_397_PDF} --text --pages=2'
    tests.run(cmd, mp=mp)

    # load page which invoked an bounding box assertion error
    serializeraw.load_textpositions(source, pages=(2,))
