# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import rawmaker.text.chars


def test_chars_extract():
    extracted = rawmaker.text.chars.extract_chars(
        power.BACHELOR090_PDF,
        pages=(12,),
    )
    assert len(extracted) == 1
