# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import rawmaker.converter.basic
import rawmaker.miner.text
import rawmaker.parameter
import rawmaker.patch.ltchar


class CharPDFConvert(rawmaker.miner.text.PrecisePDFConverter):

    def __init__(
            self,
            config: rawmaker.parameter.ParsingConfiguration = None,
            imagewriter: callable = None,
            strip: bool = None,
    ):
        super().__init__()
        self.laparams = None  # disable layout analysis

    def receive_layout(self, ltpage):
        rawmaker.converter.basic.FlippedLayoutAnalyzer.receive_layout(
            self, ltpage)
        chars = [
            char for char in ltpage
            if isinstance(char, rawmaker.patch.ltchar.PatchedLTChar)
        ]
        chars = sorted(chars, key=lambda x: x.bbox[0])  # x0
        chars = sorted(chars, key=lambda x: x.bbox[3])  # y1

        page = iamraw.Page(ltpage.pageid, iamraw.BoundingBox(*ltpage.bbox))

        for item in chars:
            page.append(item)
        self.document.pages.append(page)  # pylint:disable=E1101
