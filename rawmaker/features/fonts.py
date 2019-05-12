#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Extract test out of pdf document to gather information"""

from functools import lru_cache
from typing import Tuple

from iamraw import Font
from iamraw import Stretch
from iamraw import Style
from iamraw import TextContainer
from iamraw import Weight
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from serializeraw import dump_fonts
from serializeraw import dump_fontstore
from utila import Command

from rawmaker.miner.mining import IAmRawConverter


def work(document: PDFDocument):
    """Extract structured text out of document

    Args:
        document: pdf-document to run parsing
    Returns:
        parsed document as yaml output
    """
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()

    device = IAmRawConverter(rsrcmgr, laparams=laparams)
    device.new_document()
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Processing layout
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
    document = device.finish_document()

    fontstore = FontStore(font_fromraw)

    result = []
    for page in document.pages:
        result.append(process_page(page, fontstore))

    header = dump_fontstore(fontstore.fonts)
    content = dump_fonts(result)
    return {
        'header': header,
        'content': content,
    }


def process_page(page, fontstore):
    assert page
    container_index, line_index, char_index, font, scale, = 0, 0, 0, None, None
    result = []
    font_cur, scale_cur = None, None
    for item in page.children:
        if not isinstance(item, TextContainer):
            continue
        for line_index, line in enumerate(item.lines):
            for char_index, char in enumerate(line):
                try:
                    font = char.font
                except AttributeError:
                    # Virtual chars have no fonts
                    continue

                # fontscale = y1 - y0
                scale = round((char.box[3] - char.box[1]), 1)
                # No font type or size is selected
                if font_cur is None:
                    font_cur, scale_cur = font, scale
                    continue

                # Font type or size changed
                if font_cur != font or scale_cur != scale:
                    result.append((determine_font(
                        font,
                        scale,
                        container_index,
                        line_index,
                        char_index,
                        fontstore,
                    )))
                    # Reset current front
                    font_cur, scale_cur = None, None
        container_index += 1
    if font_cur:
        result.append((determine_font(
            font,
            scale,
            container_index,
            line_index,
            char_index,
            fontstore,
        )))

    return result


def determine_font(font, scale, container, line, char, fontstore):
    fontkey = fontstore.font_key(font, scale)
    return (container, line, char, fontkey)


class FontStore:

    def __init__(self, parser):
        self.fonts = []
        self.fast = {}
        self.parser = parser

    @lru_cache(maxsize=128)
    def font_key(self, raw_font: str, scale: float) -> int:
        # parsed = font_fromraw(raw_font, scale)
        parsed = self.parser(raw_font, scale)
        hashed = '%s' % parsed
        try:
            return self.fast[hashed]
        except KeyError:
            self.fast[hashed] = len(self.fonts)
            self.fonts.append(parsed)
        return self.fast[hashed]

    def font(self, index: int) -> Font:
        return self.fonts[index]


def font_fromraw(font: str, scale: float) -> Font:
    """Parse `Font` from pdfminer representation"""
    weight, style, stretch = Weight.LIGHT, Style.NORMAL, Stretch.REGULAR

    try:
        fontname, raw_style = font.split('-')
    except ValueError:
        # No extra style
        fontname, raw_style = font, ''
    if 'Regu' in raw_style:
        stretch = Stretch.REGULAR
        raw_style = raw_style.replace('Regu', '')
    if 'Bold' in raw_style:
        weight = Weight.BOLD
        raw_style = raw_style.replace('Bold', '')
    if 'Ital' in raw_style:
        style = Style.ITALIC
        raw_style = raw_style.replace('Ital', '')
    if 'Medi' in raw_style:
        weight = Weight.MEDIUM
        raw_style = raw_style.replace('Medi', '')

    if raw_style:  # TODO: Remove before going live
        raise ValueError('Unsupported format %s' % raw_style)

    font = Font(
        name=fontname,
        scale=scale,
        stretch=stretch,
        style=style,
        weight=weight,
    )
    return font


def commandline():
    return Command('-fo', '--%s' % name(), 'Extract fonts of document.')


def name():
    return 'fonts'
