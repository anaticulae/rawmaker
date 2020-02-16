#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
    """Parsing PDF-files based on given layout definition `laparams`.

    The `PrecisePDFConverter` parses every single page and run the
    `recive_layout` method for extracted page. Based on this method
    every Character, Textbox and TextContainer is converted from
    `pdfminer` to own format. The y-coordiante is flipped cause pdf uses
    bottom -> up and we want to use top -> bottom"""

    def __init__(
            self,
            rsrcmgr,
            laparams=None,
            imagewriter=None,
    ):
        """Create converter instance.

        Args:
            rsrcmg: resource manager to cache multiple file access
            laparams(pdfminer.layout.LAParams): layout to define maximum
                                                spacing between chars,
                                                words and lines.
            imagewrite: listener to recive extract images
        """
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
    '\uFB00': 'ff',
    '\uFB01': 'fi',
    '\uFB02': 'fl',
    '\uFB03': 'ffi',
    '\xC4': 'Ä',
    '\xDC': 'Ü',
    '\xE4': 'ä',
    '\xF6': 'ö',
    '\xFC': 'ü',
}

FAST_KEY = set(SPECIAL_CHAR_TABLE.keys())


def render_char(
        item: pdfminer.layout.LTChar,
        baseline: float,
        pageheight: float,
) -> iamraw.Char:
    """Convert character and determine `fontrise` based on parent `baseline`

    NOTE: Unicode character creates 2 single chars. This can affect
    Bounding-Computation

    Args:
        item(LTChar):
        baseline(float): bottom y-coordinate of parent text line
        pageheight(float): height of current pdf page to flip coordinate
    Returns:
        Converted `iamraw.Char` with `fontsize` and `fontrise`.
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
    # distance to bottom y-coodinate
    fontrise = baseline - bounding.y1
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
    """Determine character Bounding and split character if required
    cause layout parser puts two character together.

    Args:
        item: LTTextBox with list of containg LTChar's
        pageheight: height of page to flip y-coordiante of BoundingBox
    Returns:
        iamraw.Line with converted iamraw.Character
    """
    bounding = convert_bounding(*item.bbox, pageheight=pageheight)
    line = iamraw.Line(box=bounding)
    baseline = bounding.y1
    for char in item._objs:  # pylint: disable=protected-access
        # pylint:disable=E1101
        character = render_char(
            char,
            baseline=baseline,
            pageheight=pageheight,
        )
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
    """Split character which contains multiple chars. Split given
    BoundingBox and give every splitted character the same space.

    Args:
        char with multiple character in `char.value`
    Returns:
        list with splitted character
    """
    result = []
    charbounding = char.box
    charstep = charbounding.x1 - charbounding.x0
    assert charstep > 0, charstep
    for index, text in enumerate(char.value):
        copied = copy.deepcopy(char)
        copied.value = text
        # split common BoundingBox of multiple chars to single
        # BoundingBoxes.
        # NOTE: This does not work hundert percent correctly. Imagine if
        # you have the character Z and I togester. Z is bigger than I. But
        # that accurarcy is fine.
        bounding = iamraw.BoundingBox.from_list([
            charbounding.x0 + index * charstep,
            charbounding.y1,
            charbounding.x0 + (index + 1) * charstep,
            charbounding.y1,
        ])
        copied.box = bounding
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
        # TODO: ENSURE ROTATED PAGES?
        pageheight = item.bbox[3]
        for child in item:
            # pylint:disable=E1101
            rendered = render(child, pageheight=pageheight)
            if rendered is None:
                continue
            page.children.append(rendered)
        return page
    if isinstance(item, pdfminer.layout.LTTextBox):
        textcontainer = render_textcontainer(item, pageheight=pageheight)
        return textcontainer
    return None


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
