# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower

import rawmaker.text.chars


def test_chars_extract():
    extracted = rawmaker.text.chars.extract_chars(
        hoverpower.BACHELOR090_PDF,
        pages=(12,),
    )
    assert len(extracted) == 1
