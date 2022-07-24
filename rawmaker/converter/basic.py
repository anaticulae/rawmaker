# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import iamraw
import pdfminer.converter
import pdfminer.layout
import pdfminer.pdfinterp
import pdfminer.pdfpage
import utila


class FlippedLayoutAnalyzer(pdfminer.converter.PDFLayoutAnalyzer):

    def __init__(self, laparams=None, pageno=0):
        super().__init__(
            rsrcmgr=pdfminer.pdfinterp.PDFResourceManager(),
            pageno=pageno,
            laparams=laparams,
        )

    def receive_layout(self, ltpage):
        if content_inside_single_figure(ltpage):
            # extract content out of a single figure container
            ltpage._objs = ltpage._objs[0]._objs  # pylint:disable=W0212
            params = self.laparams
            if not params:
                # use default layout for image extractor
                params = pdfminer.layout.LAParams()
            ltpage.analyze(params)
        for item in ltpage:
            flip_object(item, ltpage)
        for item in ltpage:
            item.bbox = figure_bounding(item)
        # remove invisible objects
        ltpage._objs = [item for item in ltpage if item.bbox is not None]  # pylint:disable=W0212

    def handle_undefined_char(self, font, cid) -> str:
        # TODO: CHECK AFTER UPGRADING PDFMINER
        # TODO: FIX PAGE NUMBER
        try:
            char = MAPPING[cid]
            utila.debug(f'could not convert: {font!r}, {cid!r} use backup: '
                        f'{char} on page: {self.pageno}')
        except KeyError:
            utila.error(f'could not convert: {font!r}, {cid!r} '
                        f'on page: {self.pageno} no backup char defined')
            # use warning to log only once
            utila.warning(str(vars(font)))
            char = chr(cid)
        return char

    @property
    def resources(self):
        return self.rsrcmgr


def content_inside_single_figure(page) -> bool:
    """Some pdf printer write all page content to a single figure.

    If all content is in a single figure, no text extraction is possible.
    """
    objs = page._objs  # pylint:disable=W0212
    if len(objs) != 1:
        return False
    figure = objs[0]
    if not isinstance(figure, pdfminer.layout.LTFigure):
        return False
    if len(figure._objs) == 1:  # pylint:disable=W0212
        # image container, see master116 page,2,3. This works fine.
        return False
    return True


# REMOVE HACK LATER
# UAZWCW+CMR10
MAPPING = {
    0: '−',
    1: '·',
    12: 'fi',
    13: 'fl',
    14: 'ffi',
    # -Fern´andez,  ´Ecole  may support later, for now removing is a good match
    # for more infos see master110p106
    # 19: '´',
    19: '',
    20: '≤',
    25: 'ß',
    127: '¨',  # Umlaute, oe, ae, ue, use already implemented replace to
    # support umlaute
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
        utila.debug(f'invalid bounding on page {page}: {box}')
        utila.debug(item)
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


def figure_bounding(figure) -> tuple:
    """Bounding of some bad printed figures where too large, we strip
    this bounding to real content.

    Empty figures must return None
    >>> assert figure_bounding(pdfminer.layout.LTFigure('empty', (10, 10, 50, 50),
    ... (1, 1, 1, 1, 1, 1))) is None
    """
    if not isinstance(figure, pdfminer.layout.LTFigure):
        return figure.bbox
    figure = [item for item in figure if visible(item)]
    boundings = []
    for item in figure:
        if isinstance(item, pdfminer.layout.LTFigure):
            # figure inside a figure
            bounding = figure_bounding(item)
        else:
            bounding = item.bbox
        if bounding is None:
            # hidden item
            continue
        boundings.append(bounding)
    if not boundings:
        return None
    result = utila.rectangle_max(boundings)
    return result


def visible(item) -> bool:
    with contextlib.suppress(AttributeError):
        # TODO: INVESTIGATE THIS
        if item.linewidth:
            return True
        if item.fill:
            if not item.evenodd:
                return True
            return False
        if not item.stroking_color and not item.non_stroking_color:
            return False
    return True
