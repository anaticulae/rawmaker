#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Extract fonts out of pdf document to gather information

Stored format:

    (
        container,
        line,
        char,
        fontkey
    )

Stored item is the first different item.

The font container indexing indexes only on text-container, other pages
objects are ignored.
"""

import functools
import math

import iamraw
import serializeraw
import utila

import rawmaker.features
import rawmaker.features.text
import rawmaker.fonts.parser
import rawmaker.miner.rawchar
import rawmaker.parameter
import rawmaker.reader


def work(  # pylint:disable=W9015,W0613
    document: str,
    boxes_flow: float = 0.5,
    char_margin: float = 2.0,
    line_margin: float = 0.5,
    line_overlap: float = 0.5,
    word_margin: float = 0.1,
    nostrip: bool = not rawmaker.parameter.STRIP,
    detect_vertical: bool = False,
    pages: list = None,
) -> tuple[str, str]:
    """Extract structured text out of document

    Args:
        document: pdf-document to run parsing
        char_margin(float): XXX:5.0 why?
        pages: limit analyzed area, if None every page is analyzed
    Returns:
        parsed document as yaml output
    """
    # TODO: CHANGE BEHAVIOR OF --detect_vertical. Convert to PARAMETER
    # with True as default.
    detect_vertical = True
    assert isinstance(document, str), str(document)
    config = rawmaker.parameter.ParsingConfiguration.from_dict(**locals())
    document = rawmaker.features.text.extract_document(
        document,
        config=config,
        pages=pages,
    )
    header, content = parse_fonts(document)
    header, content = (
        serializeraw.dump_font_header(header),
        serializeraw.dump_font_content(content),
    )
    return header, content


class FontStore:

    def __init__(self, parser=None):
        self.parser = parser if parser else rawmaker.fonts.parser.font_fromraw
        self.data = {}

    @functools.lru_cache(maxsize=128)
    def font_key(self, raw_font: str, scale: float, flags: int) -> int:
        parsed = self.parser(raw_font, scale, flags)
        hashed = hash(parsed)
        try:
            self.data[hashed]
        except KeyError:
            self.data[hashed] = parsed
        return hashed

    def font(self, hashed: int):
        return self.data[hashed]

    def fonts(self):
        return list(self.data.values())


def process_page(  # pylint:disable=R0914
    page: iamraw.Page,
    fontstore: FontStore,
) -> iamraw.PageFontContent:
    """Iterate throw text container and extract the different fonts and
    positions.

    There are three indexs describing the position where the font-size
    or font-rises changes. The text container, the line in the
    container, and the char in line. The position of change is oriented
    on python range/indexing. We note the change one char after the
    change. Container and line are equal. Therefore on line endings, the
    change is noted on a char position which does not exists.

    Args:
        page(Page): current pdf page
        fontstore(FontStore): fontstore to store full information of used font
    Returns:
        Page with font information of the page text content.
    """
    assert isinstance(page, iamraw.Page), type(page)
    position = (0, 0, 0)  # container, line, char
    current_font, current_scale = None, None
    current_flags = None
    textcontainer = utila.select_type(page.children, iamraw.TextContainer)
    result = []
    for container_index, container in enumerate(textcontainer):
        rotated = isinstance(container, iamraw.VerticalTextContainer)
        for line_index, line in enumerate(container.lines):
            for char_index, char in enumerate(line):
                try:
                    font = char.font
                except AttributeError:
                    # Virtual chars have no fonts, but newlines are part
                    # of font definition.
                    position = (container_index, line_index, char_index)
                    continue
                scale = scale_fromchar(char, vertical=rotated)
                flags = flags_fromchar(char)
                # No font type or size is selected
                if current_font is None:
                    current_font, current_scale = (font, scale)
                    current_flags = flags
                    continue
                # Font type, size or flags changed
                if any((
                        current_font != font,
                        current_scale != scale,
                        current_flags != flags,
                )):
                    fontid = add_font(
                        current_font,
                        current_scale,
                        flags=current_flags,
                        position=position,
                        fontstore=fontstore,
                    )
                    result.append(fontid)
                    # Reset current front
                    current_font, current_scale = font, scale
                    current_flags = flags
                # update last index of current font
                position = (container_index, line_index, char_index)
    # add last text line of a page, because there is nothing changing
    if current_font:
        fontid = add_font(
            current_font,
            current_scale,
            flags=current_flags,
            position=position,
            fontstore=fontstore,
        )
        result.append(fontid)
    return iamraw.PageFontContent(content=result, page=page.page)


def parse_fonts(document: iamraw.Document):
    fontstore = FontStore(rawmaker.fonts.parser.font_fromraw)
    content = [process_page(page, fontstore) for page in document.pages]
    # Run header after content is important. DO NOT CHANGE ORDER. If
    # running .fonts() first, content will be empty cause no fonts where
    # processed.
    header = fontstore.fonts()
    return header, content


def add_font(font, scale, flags, *, fontstore, position):
    # position = (container, line, chars + 1)
    container, line, char = position
    # store position after the change happend
    char = char + 1
    fontkey = fontstore.font_key(font, scale, flags)
    return (container, line, char, fontkey)


def flags_fromchar(char) -> tuple:
    try:
        # LTChar
        flags = char.ltchar.flags
    except AttributeError:
        # Char
        flags = char.flags
    return flags


def upright_fromchar(char) -> bool:
    try:
        upright = char.ltchar.upright
    except AttributeError:
        upright = True
    return upright


def scale_fromchar(char, vertical: bool = False) -> float:
    # TODO: INVESTIGATE 1.34??
    # NOTE: This works for POSTSCRIPT_14_DEFAULT's but not for
    # Calibri.
    scale = utila.roundme(char.size / 1.34005)
    # TODO: THINK ABOUT VERTICAL HACK
    if scale < 0:
        rotated = not upright_fromchar(char)
        rotated |= vertical
        absolute = math.fabs(scale)
        if rotated and absolute > 4.0:  # TODO: HOLY VALUE
            # rotated char which is printed top down
            return absolute
        utila.debug(f'negative font size: {scale} {char}')
    return scale
