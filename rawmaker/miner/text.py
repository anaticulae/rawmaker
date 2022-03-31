#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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
import pdfminer.utils
import utila

import rawmaker.converter.basic
import rawmaker.miner.rawchar
import rawmaker.parameter
import rawmaker.patch.ltchar

# all rises lower this threshold are treated as noise, therefore zero.
FONT_RISE_MIN = configo.HV_FLOAT_PLUS(default=0.5)

FIX_FONTRISE_OCCURENCE_MAX = configo.HolyTable(items=[
    (1, 1),
    (20, 5),
    (40, 10),
    (60, 15),
])


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
    ):
        """Create converter instance.

        Args:
            config(ParsingConfiguration): layout to define maximum
                                          spacing between chars, words
                                          and lines.
            imagewriter(callable): listener to recive extract images
        """
        super().__init__()
        self.laparams, self.second = configure_layout_processor(config)
        self.imagewriter = imagewriter
        self.strip = config.strip if config else rawmaker.parameter.STRIP
        self.page = 0
        self.document = None

        # TODO: Remove after upgrading pdfminer
        PrecisePDFConverter.render_char = rawmaker.patch.ltchar.render_char
        self.done = utila.Single()

    def new_document(self):
        """Clear the current `Document` and initialze a new one"""
        self.document = iamraw.Document()
        self.done = utila.Single()

    def finish_document(self) -> iamraw.Document:
        """Return the current `Document` and clear the current one"""
        document = self.document
        document.dimension = page_size(document)
        self.document = None
        return document

    def end_page(self, page):
        self.cur_item = run_layout(  # pylint:disable=attribute-defined-outside-init
            self.cur_item,
            self.laparams,
            self.second,
        )
        self.pageno += 1
        self.receive_layout(self.cur_item)

    def receive_layout(self, ltpage):
        super().receive_layout(ltpage)
        page = render(ltpage, strip=self.strip)
        self.document.pages.append(page)  # pylint:disable=E1101

    def render_string(self, textstate, seq, ncs, graphicstate):
        # HACK: PDFMINER READS SOME PDF WITH IMAGES ON PAGE WRONG
        # THE BUG PRODUCES DUPLICATED OR TRIPPLED STRINGS. THE EXTRACTION
        # DOES NOT FAIL BUT THE RESULT IS USELESS.
        matrix = pdfminer.utils.mult_matrix(textstate.matrix, self.ctm)
        hashed = hash(f'{self.pageno}{textstate}{matrix}{seq}{ncs}{graphicstate}')  # yapf:disable
        if self.done.contains(hashed):
            return
        super().render_string(textstate, seq, ncs, graphicstate)


def run_layout(page, layout, layout_vertical):
    if not layout:
        # no layout analyzation
        return page
    if not layout_vertical:
        page.analyze(layout)
        return page
    horizontals, verticals, rest = [], [], []
    for item in page._objs:  # pylint:disable=W0212
        with contextlib.suppress(AttributeError):
            # process horizontal and vertical chars separately
            if item.upright:
                horizontals.append(item)
            else:
                verticals.append(item)
            continue
        rest.append(item)
    # pylint:disable=W0212
    # horizontal
    page._objs = horizontals
    page.analyze(layout)
    horizontals = page._objs
    # vertical
    page._objs = verticals
    page.analyze(layout_vertical)
    verticals = page._objs
    # unite result
    page._objs = horizontals + verticals + rest
    return page


def configure_layout_processor(config):
    """Detecting horizonal and vertical text container requires to
    layout object twice. In further releases of pdfminer this is may not
    required anymore.
    """
    laparams = rawmaker.parameter.from_config(config)
    if not laparams.detect_vertical:
        return laparams, None
    layout_vertical = rawmaker.parameter.from_config(config)
    # disable vertical a first layout processing
    laparams.detect_vertical = False
    return laparams, layout_vertical


def page_size(document: iamraw.Document) -> iamraw.PageSize:
    """Determine maximum bounding of document. Iterate throw the page and
    determine the largest page"""
    # TODO ?support multiple page sizes in document?
    width, height = -utila.INF, -utila.INF
    for page in document.pages:
        width = max(width, page.dimension[2])
        height = max(height, page.dimension[3])
    return iamraw.PageSize(width, height)


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
    # recive text
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
    if math.fabs(fontsize) <= FONT_RISE_MIN:
        # add threshold to avoid noise in char-fontrise
        fontrise = 0.0  # pylint:disable=R0204
    char = None
    replaced = rawmaker.miner.rawchar.special_char(
        value,
        fontname=item.fontname,
    )
    if replaced is not None:
        # Unicode character
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


WHITE = (1, 1, 1)
BLACK = (0, 0, 0)


def transparent(char) -> bool:
    try:
        char = char.ltchar
    except AttributeError:
        # VirtualChar
        return False
    colorspace = char.graphicstate
    stroking = colorspace.scolor
    non_storking = colorspace.ncolor
    if stroking == non_storking == WHITE:
        return True
    return False


def render_textline(
    item: pdfminer.layout.LTTextBox,
    strip: bool = False,
    remove_horizontals: bool = True,
) -> iamraw.Line:
    """Determine character Bounding and split character if required
    cause layout parser puts two character together.

    Args:
        item: LTTextBox with list of containg LTChar's
        strip: remove white spaces at begin and end of text line
        remove_horizontals: if True remove horizontal lines build out of
                            characters
    Returns:
        iamraw.Line with converted iamraw.Character
    """
    result = iamraw.Line(box=item.bbox)
    baseline = item.bbox.y1
    for char in item._objs:  # pylint: disable=protected-access
        # pylint:disable=E1101
        character = render_char(char, baseline=baseline)
        if transparent(character):
            # TODO: WRITE TO DEBUG FILE TO INFORM USER ABOUT BAD PRINTED PDF
            utila.debug(f'white char, skip: {character}')
            continue
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
    result.chars = merge_small_whitespaces(result.chars)
    result.chars = merge_special_char(result.chars)
    result.chars = fix_fontrise(result.chars)
    if remove_horizontals and ishorizontal(result.text):
        return None
    if not strip:
        return result
    result = textline_strip(result)
    return result


def textline_strip(result):
    # remove left
    lstrip = len(result.text) - len(result.text.lstrip())
    result.chars = result.chars[lstrip:]
    # remove right
    # +1 to preserve virtual newline char
    # rstrip = len(result.text.rstrip()) +1
    rstrip = len(result.text.rstrip())
    result.chars = result.chars[:rstrip]
    if result.chars:
        # TODO: ENSURE THAT ONLY A SINGLE LINE IS RENDERED?
        # IF MORE THAN ONE LINE IS RENDERED, LAST CHAR MUST NOT BE THE
        # MOST RIGHT CHAR.
        # fix bounding box of line rectangle ensure to end with newline
        # result.chars[-1].value = ' '
        x0 = result.chars[0].box.x0
        try:
            x1 = result.chars[-1].box.x1
        except AttributeError:
            # VirtualChar has no BoundingBox, use one Char before
            # TODO: THIS MAY NOT HAPPEN ANYMORE CAUSE OF THE STRIP ABOVE
            x1 = result.chars[-2].box.x1
        result.box.x0 = x0
        result.box.x1 = x1
        # TODO: VERIFY <=
        assert result.box.x0 <= result.box.x1, str(vars(result))
    return result


def ishorizontal(text: str, mincount=10) -> bool:
    """Check if text line is a char based horizontal line.

    >>> ishorizontal('--------------')
    True
    >>> ishorizontal('_______________________')
    True
    >>> ishorizontal('this is a text')
    False
    """
    shorten = text.replace('_', '').replace('-', '').replace('=', '').strip()
    if shorten:
        return False
    counted = text.count('_') + text.count('-') + text.count('=')
    if counted < mincount:
        return False
    return True


def fix_fontrise(items):
    """Workaround for font rise extraction bug.

    In some cases the layout is extracted with font rises which are not
    necessary. There is a single char without font rise and the other
    are layouted with different y1 position and a font rise.
    """
    if not items:
        return items
    non_virtual = [
        item for item in items if not isinstance(item, iamraw.VirtualChar)
    ]
    rises = [item for item in non_virtual if item.rise]
    if not rises:
        # no fix is required
        return items
    zero, non_zero = utila.partition(
        key=lambda item: utila.near(
            item.rise,
            0.0,
            diff=FONT_RISE_MIN,
        ),
        items=non_virtual,
    )
    fix_fontrise_occurence_max = FIX_FONTRISE_OCCURENCE_MAX(len(items))
    if len(non_zero) > fix_fontrise_occurence_max:
        # disable font rise for too many false detection?
        # TODO: VERIFY LATER
        for item in items:
            item.rise = 0.0
    if len(zero) != 1:
        return items
    if not non_zero:
        return items
    mode = utila.mode(item.rise for item in non_zero)
    for item in non_zero:
        item.rise = item.rise - mode
        item.box.y1 = item.box.y1 + mode
    return items


def ensure_leftright(items):
    """Fix layout parser miss detection. Ensure that more left x0
    coordinates comes before higher x0 coordinate.
    """
    # TODO: ENSURE TOP TO DOWN, LOOK AT FONT RISE PROBLEM
    # map bounding cause virtual chars has no bounding
    if not items:
        return items

    def first_box(items):
        with contextlib.suppress(AttributeError):
            return items[0].box[2]  # x1
        # TODO: WHY X1 AND NOT X0?
        # TODO: CATCH OUT OF BOUNDS
        return first_box(items[1:])

    current = first_box(items)
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


MERGES = {
    'A': 'Ä',
    'a': 'ä',
    'O': 'Ö',
    'o': 'ö',
    'U': 'Ü',
    'u': 'ü',
}


def merge_special_char(items):  # pylint:disable=R1260
    """Convert `A¨` to `Ä` etc.

    See bachelor90 example.
    """
    if not items:
        return []
    result = [items[0]]
    for item in items[1:]:
        if result[-1].value == '¨':
            # try merge
            try:
                replaced = MERGES[item.value]
                result.pop()
                item.value = replaced
                result.append(item)
            except KeyError:
                utila.error(f'could not merge with after {item}')
                result.append(item)
            continue
        try:
            special = item.special
        except AttributeError:
            special = None
        if special != '¨':
            result.append(item)
            continue
        # merge with before
        try:
            replaced = MERGES[result[-1].value]
        except KeyError:
            # TODO: REMOVE ERROR LOG LATER
            utila.debug(f'could not merge with before {item}')
            result.append(item)
            continue
        result[-1].value = replaced
    return result


def merge_small_whitespaces(items):
    """Removed unnescessary bad printed white spaces.

    See bachelor90 example.
    """
    if len(items) < 3:
        return items
    result = [items[0]]
    for current, after in zip(items[1:-1], items[2:]):
        if not isinstance(current, iamraw.VirtualChar):
            result.append(current)
            continue
        try:
            before_x0 = result[-1].box.x0
            before_x1 = result[-1].box.x1
            after_x0 = after.box.x0
        except AttributeError:
            # TODO: INVESTIGATE LATER
            # whitespace before or after
            result.append(current)
            continue
        if before_x0 <= after_x0 <= before_x1:
            # ensure to overlap and not merge hthan required
            # remove unnecessary virtual char
            continue
        # add required virtual char
        result.append(current)
    result.append(items[-1])
    return result


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
            charbounding.y0,
            charbounding.x0 + (index + 1) * charstep,
            charbounding.y1,
        ])
        copied.box = bounding
        result.append(copied)
    return result


def split_container(
    item: pdfminer.layout.LTTextBox,
    strip: bool = False,
) -> list:
    grouped = [[]]
    for line in item:
        split = not line.get_text().strip() and strip
        vertical_change = False
        if grouped[-1]:
            vertical_change = vertical(grouped[-1]) != vertical(line)
        if split or vertical_change:
            grouped.append([])
        else:
            grouped[-1].append(line)
    grouped = [item for item in grouped if item]
    # add bounding
    result = []
    for index, group in enumerate(grouped):
        item = pdfminer.layout.LTTextBoxHorizontal()
        if vertical(group):
            item = pdfminer.layout.LTTextBoxVertical()  # pylint:disable=R0204
        for line in group:
            item.add(line)
        item.index = index
        item.bbox = iamraw.BoundingBox(*item.bbox)
        result.append(item)
    return result


def render_textcontainer(
    item: pdfminer.layout.LTTextBox,
    strip: bool = False,
) -> iamraw.TextContainer:
    splitted = split_container(item, strip=strip)
    rendered = [
        render_vertical_textcontainer(item, strip=strip) if vertical(item) else
        render_horizontal_textcontainer(item, strip=strip) for item in splitted
    ]
    # Ensure that all TextContainer have only one line. Prepare to remove
    # lines concept and handle everything as a single line.
    result = []
    for container in rendered:
        if len(container) == 1:
            result.append(container)
            continue
        splitted = [
            container.__class__(box=line.box, lines=[line])
            for line in container
        ]
        result.extend(splitted)
    return result


def render_horizontal_textcontainer(
    item: pdfminer.layout.LTTextBox,
    strip: bool = False,
) -> iamraw.TextContainer:
    container = iamraw.TextContainer(box=item.bbox)
    for line in item:
        rendered = render_textline(line, strip=strip)
        if not rendered:
            continue
        container.append(rendered)
    if len(container.lines) == 1:
        # update parent box
        # TODO: ENSURE TO UPDATE MULTILINE BOXES CORRECTLY
        # TODO: COMPUTE BOXES OUT OF MEMBER/CHILDREN/LINES
        container.box = container[0].box
    if container:
        # fix start of container
        # pdfminer extracts the TextContainer bigger than the chars really
        # are. In top(y0) direction, therefore we replace the top boundary
        # with first line boundary.
        container.box.y0 = container[0].box.y0
    return container


def render_vertical_textcontainer(
    item: pdfminer.layout.LTTextBox,
    strip: bool = False,
) -> iamraw.VerticalTextContainer:
    container = iamraw.VerticalTextContainer(box=item.bbox)
    for line in item:
        rendered = render_textline(line, strip=strip)
        if not rendered:
            continue
        container.append(rendered)
    return container


def vertical(item: pdfminer.layout.LTTextBox):
    """Check LTChar.upright flag."""
    if isinstance(item, (pdfminer.layout.LTTextLine)):
        # enable checking single lines
        item = [item]
    for line in item:
        for char in line._objs:  # pylint: disable=protected-access
            with contextlib.suppress(AttributeError):
                if rawmaker.patch.ltchar.vertical(char):
                    return True
    return False


def render(item, strip: bool = False):  # pylint:disable=R1260,too-many-branches
    if isinstance(item, pdfminer.layout.LTPage):  # pylint:disable=too-many-nested-blocks
        pagenumber = item.pageid
        page = iamraw.Page(pagenumber, iamraw.BoundingBox(*item.bbox))
        # TODO: ENSURE ROTATED PAGES?
        for child in item:
            # pylint:disable=E1101
            rendered = render(child, strip=strip)
            if rendered is None:
                continue
            if isinstance(rendered, list):
                for single in rendered:
                    if isinstance(single, list):
                        for pageitem in single:
                            page.append(pageitem)
                    else:
                        page.append(single)
            else:
                page.append(rendered)
        page = mylayout(page)
        return page
    if isinstance(item, pdfminer.layout.LTTextBox):
        textcontainers = render_textcontainer(item, strip=strip)
        result = []
        for container in textcontainers:
            if strip:
                container.lines = [
                    line for line in container.lines if line.text.strip()
                ]
                if not container.lines:
                    # ignore stripped line
                    continue
            container = ensure_bounding(container)
            result.append(container)
        return result
    return None


def ensure_bounding(textcontainer: iamraw.TextContainer):
    if len(textcontainer) == 1:
        return textcontainer
    if isinstance(textcontainer, iamraw.VerticalTextContainer):
        # TODO: NOT SUPPORTED YET
        return textcontainer
    # check if splitting bounding container is required or container fits
    # already.
    indexed = [[0]]
    for index, item in enumerate(textcontainer[1:], start=1):
        before = textcontainer[indexed[-1][0]].box
        cur = item.box
        if (utila.near(before[0], cur[0]) and utila.near(before[2], cur[2])):
            indexed[-1].append(index)
        else:
            indexed.append([index])
    if len(indexed) == 1:
        # splitting is not required, container fits already
        return textcontainer
    result = []
    for block in indexed:
        # split container into smaller, better fitting containers
        collected = [textcontainer[index] for index in block]
        current = iamraw.TextContainer()
        for item in collected:
            current.append(item)
        current.box = utila.rectangle_max([item.box for item in collected])
        result.append(current)
    return result


def mylayout(page: iamraw.Page) -> iamraw.Page:
    children = page.children
    if not children:
        return page
    verticals, horizontal = utila.partition(
        lambda x: isinstance(x, iamraw.VerticalTextContainer),
        children,
    )
    verticals = merge_neighbors(
        verticals,
        horizontal=False,
        ydiff=15.0,
        xdiff=15.0,
    )
    horizontal = merge_neighbors(horizontal)
    page.children = horizontal + verticals
    return page


def merge_neighbors(
    children: list,
    xdiff: float = 10.0,
    ydiff: float = 5.0,
    horizontal: bool = True,
) -> list:
    # TODO: IMPROVE VERTICAL MERGER
    if not children:
        return []
    # ensure to sort items top to bottom and left to right. It is
    # important to connect only neighbored items to avoid conflicts in
    # bounding computation. See: test_mylayout_bounding_extraction_bug
    # Use y1 as lower text line.
    if horizontal:
        children = sorted(children, key=lambda x: x.box[0])  # leftright
        children = sorted(children, key=lambda x: x.box[3])  # topdown
    else:
        # vertical
        # bottom up
        children = sorted(children, key=lambda x: x.box[1], reverse=True)
        children = sorted(children, key=lambda x: x.box[0])  # leftright
    result = [children[0]]
    for item in children[1:]:
        before = result[-1]
        # TODO: MAKE THIS SIZE DEPENDENT
        ynear = utila.near(item.box[3], before.box[3], diff=ydiff)
        xnear = utila.near(item.box[0], before.box[2], diff=xdiff)
        if ynear and xnear:
            # merge before
            # add virtual char
            before.lines[-1].chars.append(iamraw.VirtualChar(value=' '))
            before.lines[-1].chars.extend(item.lines[0].chars)
            if len(item.lines) >= 2:
                before.lines.extend(item.lines[1:])
            # adjust bounding
            if item.box[2] > before.box[2]:
                # ensure that right border is more right than left border.
                # In some cases, formulas for example, it can happen that
                # this contraint is not given.
                before.box = utila.update_tuple(
                    data=tuple(before.box),  # REMOVE TUPLE LATER
                    value=item.box[2],
                    index=2,
                )
            else:
                utila.debug('HINT: no bounding box update required')
            before.box = iamraw.BoundingBox(*before.box)
        else:
            result.append(item)
    return result
