# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import rawmaker.text.chars
import rawmaker.text.wordbox
import tests.resources


def test_wordbox_extract_hello_word_4lines():
    parsed = rawmaker.text.wordbox.parses(
        tests.resources.HELLO_WORLD_PDF,
        pages=(0,),
    )
    assert len(parsed[0]) == 8


def test_wordbox_extract_pagelines_helloworld():
    page = rawmaker.text.chars.extract_chars(
        tests.resources.HELLO_WORLD_PDF,
        pages=(0,),
    )
    pagelines = rawmaker.text.wordbox.extract_page(page[0])
    assert len(pagelines) == 4
    assert len(pagelines[0]) == 2
    assert len(pagelines[1]) == 2
