# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import iamraw
import serializeraw
import utila

import rawmaker.features.text
import tests.examples.single


def test_layout_extraction_mine_mini_numbers():
    example = tests.examples.single.HEADLINE_MOVINGFOOTER_FOOTNOTES_PDF
    worker = rawmaker.features.text.work

    text, _ = worker(
        document=example,
        boxes_flow=1.0,
        char_margin=10.0,
        line_margin=1.0,
    )

    text = serializeraw.load_document(text)
    firstpage = text[0]
    containers = utila.select(firstpage, iamraw.TextContainer)
    lines = utila.flatten([item.lines for item in containers])
    footnotes = lines[-9:-2]

    first_rises = [item[0].rise for item in footnotes]
    # skip second line of first foot note
    first_rises = [first_rises[0]] + first_rises[2:]
    # ensure to parse rised number of footnotes
    assert all([item > 5.0 for item in first_rises]), first_rises
