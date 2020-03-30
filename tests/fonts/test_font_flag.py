# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import rawmaker.features.fonts
import tests.resources


def test_extract_font_flag():
    header, content = rawmaker.features.fonts.work(
        tests.resources.PDF2008,
        pages=(291,),
    )
    header = serializeraw.load_font_header(header)
    content = serializeraw.load_font_content(content)
    # TODO: EXTEND AFTER UPGRADING IAMRAW
