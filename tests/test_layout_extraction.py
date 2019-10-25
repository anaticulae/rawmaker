# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import serializeraw

import rawmaker.features.text
import tests.examples.single


def test_layout_extraction_mine_mini_numbers():
    example = tests.examples.single.HEADLINE_MOVINGFOOTER_FOOTNOTES_PDF
    worker = rawmaker.features.text.work

    text, position = worker(document=example)

    text = serializeraw.load_document(text)
