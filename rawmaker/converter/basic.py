# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import iamraw
import pdfminer.converter
import pdfminer.pdfinterp
import utila


class FlippedLayoutAnalyzer(pdfminer.converter.PDFLayoutAnalyzer):

    def __init__(self, laparams=None, pageno=0):
        super().__init__(
            rsrcmgr=pdfminer.pdfinterp.PDFResourceManager(),
            pageno=pageno,
            laparams=laparams,
        )

    def receive_layout(self, ltpage):
        for item in ltpage:
            flip_object(item, ltpage)

    def handle_undefined_char(self, font, cid) -> str:
        # TODO: CHECK AFTER UPGRADING PDFMINER
        # TODO:  FIX PAGE NUMBER
        try:
            char = MAPPING[cid]
            utila.debug(f'could not convert: {font!r}, {cid!r} use backup: '
                        f'{char} on page: {self.pageno}')
        except KeyError:
            utila.debug(f'could not convert: {font!r}, {cid!r} '
                        f'on page: {self.pageno}')
            char = chr(cid)
        return char

    @property
    def resources(self):
        return self.rsrcmgr


# REMOVE HACK LATER
# UAZWCW+CMR10
MAPPING = {
    0: '−',
    1: '·',
    12: 'fi',
    20: '≤',
    25: 'ß',
    127: '',  # Umlaute, oe, ae, ue
}


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


class PageAggregator(FlippedLayoutAnalyzer):

    def __init__(self, laparams=None):
        super().__init__(laparams=laparams)
        self.result = None

    def receive_layout(self, ltpage):
        super().receive_layout(ltpage)
        self.result = ltpage

    def get_result(self):
        return self.result
