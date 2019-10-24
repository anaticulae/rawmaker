#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""
Parses the pdf-document and determine the layout of the different
components.
"""
import sys
from re import compile as re_compile

import utila
from iamraw import BoundingBox
from iamraw import Char
from iamraw import Document
from iamraw import Line
from iamraw import Page
from iamraw import PageObject
from iamraw import PageSize
from iamraw import TextContainer
from iamraw import UnicodeChar
from iamraw import VirtualChar
from pdfminer.converter import PDFConverter
from pdfminer.layout import LTChar
from pdfminer.layout import LTPage
from pdfminer.layout import LTTextBox
from utila import INF


class IAmRawConverter(PDFConverter):

    CONTROL = re_compile(u'[\x00-\x08\x0b-\x0c\x0e-\x1f]')

    def __init__(
            self,
            rsrcmgr,
            laparams=None,
            imagewriter=None,
    ):
        PDFConverter.__init__(
            self,
            rsrcmgr,
            outfp=sys.stdout.buffer,
            codec='utf-8',
            pageno=0,
            laparams=laparams,
        )
        self.imagewriter = imagewriter
        self.page = 0
        self.document = None

    def new_document(self):
        """Clear the current `Document` and initialze a new one"""
        self.document = Document()

    def finish_document(self) -> Document:
        """Return the current `Document` and clear the current one"""
        document = self.document
        document.dimension = page_size(document)
        self.document = None
        return document

    def receive_layout(self, ltpage):
        page = render(ltpage)
        self.document.pages.append(page)


def page_size(document: Document) -> PageSize:
    """Determine maximum bounding of document. Iterate throw the page and
    determine the largest page"""

    # TODO ?support multiple page sizes in document?
    width, height = -INF, -INF
    for page in document.pages:
        width = max(width, page.dimension[2])
        height = max(height, page.dimension[3])
    return PageSize(width, height)


SPECIAL_CHAR_TABLE = {
    '\uFB01': 'fi',
}

FAST_KEY = set(SPECIAL_CHAR_TABLE.keys())


def render_char(item: LTChar, pageheight: float) -> Char:
    char = None
    try:
        value = item.get_text()
        bounding = convert_bounding(*item.bbox, pageheight=pageheight)
        if value in FAST_KEY:
            # Unicode character
            replaced = SPECIAL_CHAR_TABLE[value]
            char = UnicodeChar(
                box=bounding,
                font=item.fontname,
                special=value,
                value=replaced,
            )
        else:
            char = Char(
                box=bounding,
                font=item.fontname,
                value=value,
            )
    except AttributeError:
        # VirtualChar has no `BoundingBox`
        char = VirtualChar(value=item.get_text())
    return char


def render_textline(item: LTTextBox, pageheight: float):
    bounding = convert_bounding(*item.bbox, pageheight=pageheight)
    line = Line(box=bounding)
    for char in item._objs:  # pylint: disable=protected-access
        # pylint:disable=E1101
        line.chars.append(render_char(char, pageheight=pageheight))
    return line


def render_textcontainer(item: LTTextBox, pageheight: float):
    bounding = convert_bounding(*item.bbox, pageheight=pageheight)
    container = TextContainer(box=bounding)
    for line in item:
        # pylint:disable=E1101
        container.lines.append(render_textline(line, pageheight=pageheight))
    return container


def render(item, pageheight: float = None):
    if isinstance(item, LTPage):
        pagenumber = item.pageid
        page = Page(pagenumber, BoundingBox(*item.bbox))
        pageheight = item.bbox[3]
        for child in item:
            # pylint:disable=E1101
            rendered = render(child, pageheight=pageheight)
            page.children.append(rendered)
        return page
    if isinstance(item, LTTextBox):
        textcontainer = render_textcontainer(item, pageheight=pageheight)
        return textcontainer

    pageobject = PageObject(
        box=convert_bounding(*item.bbox, pageheight=pageheight),
        content=str(item),
    )
    return pageobject


def convert_bounding(*bounding, pageheight: float) -> BoundingBox:
    """Flip vertical y-component.

    Args:
        bounding(tuple(4)): tuple with computed location of `pdfminer`
        pageheight(float): pageheight from bottom to top
    Returns:
        flipped `BoundingBox`
    """
    xbottom, ybottom, xtop, ytop = bounding
    height = ytop - ybottom
    assert height >= 0
    x0 = utila.roundme(xbottom)
    y0 = utila.roundme(pageheight - ytop)
    x1 = utila.roundme(xtop)
    y1 = utila.roundme(y0 + height)
    bounding = BoundingBox(x0=x0, y0=y0, x1=x1, y1=y1)
    return bounding
