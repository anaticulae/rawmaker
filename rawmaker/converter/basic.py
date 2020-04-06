# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import iamraw
import pdfminer.converter
import utila


class FlippedLayoutAnalyzer(pdfminer.converter.PDFLayoutAnalyzer):

    def __init__(self, rsrcmgr, pageno=0, laparams=None):
        super().__init__(rsrcmgr=rsrcmgr, pageno=pageno, laparams=laparams)

    def receive_layout(self, ltpage):
        for item in ltpage:
            flip_object(item, ltpage)


def flip_object(item, page):
    try:
        box = list(item.bbox)
    except AttributeError:
        # VirtualChar for example
        return
    pageheight = page.height
    box[1], box[3] = pageheight - box[3], pageheight - box[1]
    box = utila.roundme(box)  # pylint:disable=R0204
    try:
        item.bbox = iamraw.BoundingBox(*box)
    except AssertionError:
        utila.error(f'invalid bounding on page {page}: {box}')
        utila.error(item)
    item.x0, item.y0, item.x1, item.y1 = box
    with contextlib.suppress(AttributeError):
        for obj in item._objs:  # pylint:disable=W0212
            flip_object(obj, page)
