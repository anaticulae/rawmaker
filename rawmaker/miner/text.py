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

import contextlib
import copy
import math

import configo
import iamraw
import pdfminer.converter
import pdfminer.layout
import pdfminer.pdfinterp
import utila

import rawmaker.converter.basic
import rawmaker.miner.rawchar
import rawmaker.parameter
import rawmaker.patch.ltchar

# all rises lower this threshold are threated as noise, therefore zero.
MIN_FONT_RISE = configo.HV_INT_PLUS(default=0.05)


class PrecisePDFConverter(rawmaker.converter.basic.FlippedLayoutAnalyzer):
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
        super().__init__(laparams=rawmaker.parameter.from_config(config))
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
        super().receive_layout(ltpage)
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


# TODO: REQUIRE BETTER APPROACH OF REPLACING `LEGATURES`
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
) -> iamraw.Char:
    """Convert character and determine `fontrise` based on parent `baseline`

    NOTE: Unicode character creates 2 single chars. This can affect
    Bounding-Computation

    Args:
        item(LTChar): single character
        baseline(float): bottom y-coordinate of parent text line
    Returns:
        Converted `iamraw.Char` with `fontsize` and `fontrise`.
    """
    try:
        # layout characher due pdfminer changes removes BoundingBox from
        # item, therefore we have to add this again
        bounding = iamraw.BoundingBox(*item.bbox)
    except AttributeError:
        # VirtualChar has no `iamraw.BoundingBox`
        bounding = None

    value = item.get_text()
    # controlling chars
    if not bounding:
        # Example VirtualChar: <LTAnno ' '>
        virtual = iamraw.VirtualChar(value=value)
        return virtual
    # chars with content
    fontsize = utila.roundme(item.fontsize)

    # distance to bottom y-coodinate
    fontrise = utila.roundme(baseline - bounding.y1)
    if math.fabs(fontsize) <= MIN_FONT_RISE:
        # add threshold to avoid noise in char-fontrise
        fontrise = 0.0  # pylint:disable=R0204

    char = None
    if value in FAST_KEY:
        # Unicode character
        replaced = SPECIAL_CHAR_TABLE[value]
        char = rawmaker.miner.rawchar.RawUnicodeChar(
            ltchar=item,
            box=bounding,
            font=item.fontname,
            rise=fontrise,
            size=fontsize,
            special=value,
            value=replaced,
        )
    else:
        char = rawmaker.miner.rawchar.RawChar(
            ltchar=item,
            box=bounding,
            font=item.fontname,
            rise=fontrise,
            size=fontsize,
            value=value,
        )
    return char


def render_textline(
        item: pdfminer.layout.LTTextBox,
        strip: bool = False,
) -> iamraw.Line:
    """Determine character Bounding and split character if required
    cause layout parser puts two character together.

    Args:
        item: LTTextBox with list of containg LTChar's
        strip: remove white spaces at begin and end of text line
    Returns:
        iamraw.Line with converted iamraw.Character
    """
    result = iamraw.Line(box=item.bbox)
    baseline = item.bbox.y1
    for char in item._objs:  # pylint: disable=protected-access
        # pylint:disable=E1101
        character = render_char(
            char,
            baseline=baseline,
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
            result.box.x0 = x0
            result.box.x1 = x1
            assert result.box.x0 < result.box.x1, str(result.box)
    return result


def ensure_leftright(items):
    """Fix layout parser misdetection. Ensure that more left x0
    coordinates comes before higher x0 cooridinate."""
    # TODO: ENSURE TOP TO DOWN, LOOK AT FONT RISE PROBLEM
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
    if charstep <= 0.0:
        utila.error(f'invalid charstep: {charstep}: {charbounding} - {char}')
    assert charstep >= 0.0, f'{charstep}: {charbounding} - {char}'
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
        strip: bool = False,
) -> iamraw.TextContainer:
    bounding = item.bbox
    if vertical(item):
        container = iamraw.VerticalTextContainer(box=bounding)
    else:
        container = iamraw.TextContainer(box=bounding)
    for line in item:
        # pylint:disable=E1101
        rendered = render_textline(line, strip=strip)
        if not rendered:
            continue
        container.lines.append(rendered)
    if len(container.lines) == 1:
        # update parent box
        # TODO: ENSURE TO UPDATE MULTILINE BOXES CORRECTLY
        # TODO: COMPUTE BOXES OUT OF MEMBER/CHILDREN/LINES
        container.box = container[0].box
    return container


def vertical(item: pdfminer.layout.LTTextBox):
    """Check LTChar.upright flag."""
    for line in item:
        for char in line._objs:  # pylint: disable=protected-access
            with contextlib.suppress(AttributeError):
                if rawmaker.patch.ltchar.vertical(char):
                    return True
    return False


def render(item, strip: bool = False):
    if isinstance(item, pdfminer.layout.LTPage):
        pagenumber = item.pageid
        page = iamraw.Page(pagenumber, iamraw.BoundingBox(*item.bbox))
        # TODO: ENSURE ROTATED PAGES?
        for child in item:
            # pylint:disable=E1101
            rendered = render(child, strip=strip)
            if rendered is None:
                continue
            page.children.append(rendered)
        return page
    if isinstance(item, pdfminer.layout.LTTextBox):
        textcontainer = render_textcontainer(item, strip=strip)
        if strip:
            textcontainer.lines = [
                line for line in textcontainer.lines if line.text.strip()
            ]
            if not textcontainer.lines:
                # ignore stripped line
                return None
        return textcontainer
    return None
