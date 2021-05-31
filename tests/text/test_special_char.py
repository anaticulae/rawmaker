# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import rawmaker.features.text


def test_text_mining_convert_special_chars():
    parsed = rawmaker.features.text.work(
        power.BACHELOR090_PDF,
        boxes_flow=1.0,
        pages=(1,),
    )
    document = serializeraw.load_document(parsed[0])
    # first page, fourth line
    text = document[0][3].text
    expected = 'für die Anwendung auf einem Embedded System\n'
    assert text == expected


def test_text_mining_convert_special_whitespace_between_special():
    """A white space between expected vowel and '¨' requires to remove
    small white space before merging both chars.

    Normal:
    text u¨ hello -> textü hello
    Here:
    textu ¨ hello -> textü hello

    Solution remove small white spaces before merging.
    """
    parsed = rawmaker.features.text.work(
        power.BACHELOR090_PDF,
        boxes_flow=1.0,
        pages=(5,),
    )
    document = serializeraw.load_document(parsed[0])
    # page, line
    text = document[0][8].text
    expected = '3.4.3. Vollständige Automatisierung . .'
    assert expected in text
    assert expected in text
