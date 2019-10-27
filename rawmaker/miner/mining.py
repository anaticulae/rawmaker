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
import copy
import sys

import iamraw
import pdfminer.converter
import pdfminer.layout
import utila

import rawmaker.patch.ltchar


class PrecisePDFConverter(pdfminer.converter.PDFConverter):

    def __init__(
            self,
            rsrcmgr,
            laparams=None,
            imagewriter=None,
    ):
        super().__init__(
            rsrcmgr=rsrcmgr,
            outfp=sys.stdout.buffer,
            codec=utila.UTF8,
            pageno=0,
            laparams=laparams,
        )
        self.imagewriter = imagewriter
        self.page = 0
        self.document = None

        # TODO: Remove after upgrading pdfminer
        PrecisePDFConverter.render_char = rawmaker.patch.ltchar.render_char

    def new_document(self):
        """Clear the current `Document` and initialze a new one"""
        self.document = iamraw.Document()

    def finish_document(self) -> iamraw.Document:
        """Return the current `Document` and clear the current one"""
        document = self.document
        document.dimension = page_size(document)
        self.document = None
        return document

    def receive_layout(self, ltpage):
        page = render(ltpage)
        self.document.pages.append(page)  # pylint:disable=E1101


def page_size(document: iamraw.Document) -> iamraw.PageSize:
    """Determine maximum bounding of document. Iterate throw the page and
    determine the largest page"""

    # TODO ?support multiple page sizes in document?
    width, height = -utila.INF, -utila.INF
    for page in document.pages:
        width = max(width, page.dimension[2])
        height = max(height, page.dimension[3])
    return iamraw.PageSize(width, height)


SPECIAL_CHAR_TABLE = {
    '\uFB01': 'fi',
}

FAST_KEY = set(SPECIAL_CHAR_TABLE.keys())


def render_char(
        item: pdfminer.layout.LTChar,
        pageheight: float,
) -> iamraw.Char:
    """
    NOTE: Unicode character creates 2 single chars.
    This can affect Bounding-Computation
    """
    try:
        bounding = convert_bounding(*item.bbox, pageheight=pageheight)
    except AttributeError:
        # VirtualChar has no `iamraw.BoundingBox`
        bounding = None

    value = item.get_text()
    # controlling chars
    if not bounding:
        # Example VirtualChar: <LTAnno ' '>
        char = iamraw.VirtualChar(value=value)
        return char

    # chars with content
    fontsize = item.fontsize
    fontrise = item.rise
    if value in FAST_KEY:
        # Unicode character
        replaced = SPECIAL_CHAR_TABLE[value]
        char = iamraw.UnicodeChar(
            box=bounding,
            font=item.fontname,
            rise=fontrise,
            size=fontsize,
            special=value,
            value=replaced,
        )
    else:
        char = iamraw.Char(
            box=bounding,
            font=item.fontname,
            rise=fontrise,
            size=fontsize,
            value=value,
        )
    return char


def render_textline(item: pdfminer.layout.LTTextBox, pageheight: float):
    bounding = convert_bounding(*item.bbox, pageheight=pageheight)
    line = iamraw.Line(box=bounding)
    for char in item._objs:  # pylint: disable=protected-access
        # pylint:disable=E1101
        character = render_char(char, pageheight=pageheight)
        if len(character.value) == 1:
            line.chars.append(character)
        else:
            # in some case the layout parser matches to chars together.
            # Therefore we have to split the character by content and fix
            # the bounding.
            for splitted in split_characters(character):
                assert len(splitted.value) == 1, splitted
                line.chars.append(splitted)
    return line


def split_characters(char):
    result = []
    for index, text in enumerate(char.value):
        # TODO: FIX BOUNDING OF EVERY SINGLE CHARACTER
        copied = copy.deepcopy(char)
        copied.value = text
        result.append(copied)
    return result


def render_textcontainer(item: pdfminer.layout.LTTextBox, pageheight: float):
    bounding = convert_bounding(*item.bbox, pageheight=pageheight)
    container = iamraw.TextContainer(box=bounding)
    for line in item:
        # pylint:disable=E1101
        container.lines.append(render_textline(line, pageheight=pageheight))
    return container


def render(item, pageheight: float = None):
    if isinstance(item, pdfminer.layout.LTPage):
        pagenumber = item.pageid
        page = iamraw.Page(pagenumber, iamraw.BoundingBox(*item.bbox))
        pageheight = item.bbox[3]
        for child in item:
            # pylint:disable=E1101
            rendered = render(child, pageheight=pageheight)
            page.children.append(rendered)
        return page
    if isinstance(item, pdfminer.layout.LTTextBox):
        textcontainer = render_textcontainer(item, pageheight=pageheight)
        return textcontainer

    pageobject = iamraw.PageObject(
        box=convert_bounding(*item.bbox, pageheight=pageheight),
        content=str(item),
    )
    return pageobject


def convert_bounding(*bounding, pageheight: float) -> iamraw.BoundingBox:
    """Flip vertical y-component.

    Args:
        bounding(tuple(4)): tuple with computed location of `pdfminer`
        pageheight(float): pageheight from bottom to top
    Returns:
        flipped `iamraw.BoundingBox`
    """
    xbottom, ybottom, xtop, ytop = bounding
    height = ytop - ybottom
    assert height >= 0
    x0 = utila.roundme(xbottom)
    y0 = utila.roundme(pageheight - ytop)
    x1 = utila.roundme(xtop)
    y1 = utila.roundme(y0 + height)
    bounding = iamraw.BoundingBox(x0=x0, y0=y0, x1=x1, y1=y1)
    return bounding
