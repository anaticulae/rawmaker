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
