#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Textminer
=========

Parses pdf document and extracts layouted text components.
"""
import copy
import sys

import iamraw
import pdfminer.converter
import pdfminer.layout
import pdfminer.pdfinterp
import utila

import rawmaker.parameter
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
            config: rawmaker.parameter.ParsingConfiguration = None,
            imagewriter: callable = None,
            strip: bool = None,
    ):
        """Create converter instance.

        Args:
            config(ParsingConfiguration): layout to define maximum
                                          spacing between chars, words
                                          and lines.
            imagewriter(callable): listener to recive extract images
            strip(bool): remove holy white spaces which are a result of
                         bad pdf printer or bad pdf parsing.
        """
        super().__init__(
            # Create a PDF resource manager object that stores shared resources.
            rsrcmgr=pdfminer.pdfinterp.PDFResourceManager(),
            outfp=sys.stdout.buffer,
            codec=utila.UTF8,
            pageno=0,
            laparams=rawmaker.parameter.from_config(config),
        )
        self.imagewriter = imagewriter
        self.strip = rawmaker.parameter.STRIP if strip is None else strip
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
        page = render(ltpage, strip=self.strip)
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
        item(LTChar): single character
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

    char = None
    # controlling chars
    if not bounding:
        # Example VirtualChar: <LTAnno ' '>
        virtual = iamraw.VirtualChar(value=value)
        return virtual
    # chars with content
    fontsize = utila.roundme(item.fontsize)
    # distance to bottom y-coodinate
    fontrise = utila.roundme(baseline - bounding.y1)
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


def render_textline(
        item: pdfminer.layout.LTTextBox,
        pageheight: float,
        strip: bool = False,
) -> iamraw.Line:
    """Determine character Bounding and split character if required
    cause layout parser puts two character together.

    Args:
        item: LTTextBox with list of containg LTChar's
        pageheight: height of page to flip y-coordiante of BoundingBox
        strip: remove white spaces at begin and end of text line
    Returns:
        iamraw.Line with converted iamraw.Character
    """
    bounding = convert_bounding(*item.bbox, pageheight=pageheight)
    result = iamraw.Line(box=bounding)
    baseline = bounding.y1
    for char in item._objs:  # pylint: disable=protected-access
        # pylint:disable=E1101
        character = render_char(
            char,
            baseline=baseline,
            pageheight=pageheight,
        )
        if len(character.value) == 1:
            result.chars.append(character)
        else:
            # in some case the layout parser matches to chars together.
            # Therefore we have to split the character by content and fix
            # the bounding.
            for splitted in split_characters(character):
                assert len(splitted.value) == 1, splitted
                result.chars.append(splitted)
    # ensure that chars are sorted from left to right
    # TODO: CHECK VERTICAL TEXT?
    result.chars = ensure_leftright(result.chars)
    if strip:
        # remove left
        lstrip = len(result.text) - len(result.text.lstrip())
        result.chars = result.chars[lstrip:]
        # remove right
        # +1 to preserve virtual newline char
        rstrip = len(result.text.rstrip()) + 1
        result.chars = result.chars[:rstrip]

        if result.chars:
            # TODO: ENSURE THAT ONLY A SINGLE LINE IS RENDERED?
            # IF MORE THAN ONE LINE IS RENDERED, LAST CHAR MUST NOT BE THE
            # MOST RIGH CHAR.
            # fix bounding box of line rectangle
            # ensure to end with newline
            result.chars[-1].value = '\n'
            x0 = result.chars[0].box.x0
            try:
                x1 = result.chars[-1].box.x1
            except AttributeError:
                # VirtualChar has no BoundingBox, use one Char before
                x1 = result.chars[-2].box.x1
            bounding.x0 = x0
            bounding.x1 = x1
            assert bounding.x0 < bounding.x1, str(bounding)
    return result


def ensure_leftright(items):
    """Fix layout parser misdetection. Ensure that more left x0
    coordinates comes before higher x0 cooridinate."""
    # map bounding cause virtual chars has no bounding
    if not items:
        return items
    current = items[0].box[2]  # x1
    boundings = []
    for item in items:
        try:
            boundings.append((item.box[0], item))  # x0 left border
            current = item.box[2]  # x1 right border
        except AttributeError:
            boundings.append((current, item))
            # more than one virtual char in a row, don't know if possible
            current += 0.1
            current = utila.roundme(current)
    # sort from left to right
    boundings = sorted(boundings, key=lambda x: x[0])
    # remove mapped coordiante
    items = [item[1] for item in boundings]
    return items


def split_characters(char) -> list:
    """Split character which contains multiple chars. Split given
    BoundingBox and give every splitted character the same space.

    Args:
        char with multiple character in `char.value`
    Returns:
        List of splitted character.
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


def render_textcontainer(
        item: pdfminer.layout.LTTextBox,
        pageheight: float,
        strip: bool = False,
) -> iamraw.TextContainer:
    bounding = convert_bounding(*item.bbox, pageheight=pageheight)
    container = iamraw.TextContainer(box=bounding)
    for line in item:
        # pylint:disable=E1101
        rendered = render_textline(line, pageheight=pageheight, strip=strip)
        if not rendered:
            continue
        container.lines.append(rendered)
    if len(container.lines) == 1:
        # update parent box
        # TODO: ENSURE TO UPDATE MULTILINE BOXES CORRECTLY
        # TODO: COMPUTE BOXES OUT OF MEMBER/CHILDREN/LINES
        container.box = container[0].box
    return container


def render(item, pageheight: float = None, strip: bool = False):
    if isinstance(item, pdfminer.layout.LTPage):
        pagenumber = item.pageid
        page = iamraw.Page(pagenumber, iamraw.BoundingBox(*item.bbox))
        # TODO: ENSURE ROTATED PAGES?
        pageheight = item.bbox[3]
        for child in item:
            # pylint:disable=E1101
            rendered = render(child, pageheight=pageheight, strip=strip)
            if rendered is None:
                continue
            page.children.append(rendered)
        return page
    if isinstance(item, pdfminer.layout.LTTextBox):
        textcontainer = render_textcontainer(
            item,
            pageheight=pageheight,
            strip=strip,
        )
        if strip:
            textcontainer.lines = [
                line for line in textcontainer.lines if line.text.strip()
            ]
            if not textcontainer.lines:
                # ignore stripped line
                return None
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
    # developer friendly debugging
    x0, y0, x1, y1 = utila.roundme([x0, y0, x1, y1])
    bounding = iamraw.BoundingBox(x0=x0, y0=y0, x1=x1, y1=y1)
    return bounding
