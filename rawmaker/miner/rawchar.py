# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""RawCharacter
============

The concept of `RawItem`s aims to store the full pdf information by
current items to use them for further analysis. This information are
`rawmaker` internal and will be removed before serializing the data.
"""

import contextlib

import iamraw
import pdfminer.layout


class RawChar(iamraw.Char):

    def __init__(self, ltchar: pdfminer.layout.LTChar, **kwargs):
        super().__init__(**kwargs)
        self.ltchar = ltchar


class RawUnicodeChar(iamraw.UnicodeChar):

    def __init__(self, ltchar: pdfminer.layout.LTChar, **kwargs):
        super().__init__(**kwargs)
        self.ltchar = ltchar


def special_char(item: str):
    with contextlib.suppress(KeyError):
        return SPECIAL_CHAR_TABLE[item]
    return None


# TODO: REQUIRE BETTER APPROACH OF REPLACING `LEGATURES`
SPECIAL_CHAR_TABLE = {
    '\uFB00': 'ff',
    '\uFB01': 'fi',
    '\uFB02': 'fl',
    '\uFB03': 'ffi',
    '\xA8': '¨',
    '\xC4': 'Ä',
    '\xDC': 'Ü',
    '\xE4': 'ä',
    '\xF6': 'ö',
    '\xFC': 'ü',
    '\u0161': 's',  # š
    '\xE9': 'e',  # é
}

FAST_KEY = set(SPECIAL_CHAR_TABLE.keys())
