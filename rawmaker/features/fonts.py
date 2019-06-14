#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
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

from functools import lru_cache

from iamraw import Document
from iamraw import Font
from iamraw import Stretch
from iamraw import Style
from iamraw import TextContainer
from iamraw import Weight
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from serializeraw import dump_fonts
from serializeraw import dump_fontstore
from utila import Flag
from utila import logging_error

from rawmaker.miner.mining import IAmRawConverter
from rawmaker.parameter import create_layout


def work(document: PDFDocument, parameter: dict = None):
    """Extract structured text out of document

    Args:
        document: pdf-document to run parsing
    Returns:
        parsed document as yaml output
    """
    document = parse_document(document, parameter)

    header, content = parse_fonts(document)
    header, content = dump_fontstore(header), dump_fonts(content)
    return {
        'header': header,
        'content': content,
    }


def parse_document(pdf: PDFDocument, parameter: dict = None) -> Document:
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    parameter = {} if parameter is None else parameter
    layout = create_layout(parameter)

    device = IAmRawConverter(rsrcmgr, laparams=layout)
    device.new_document()
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Processing layout
    for page in PDFPage.create_pages(pdf):
        interpreter.process_page(page)
    document = device.finish_document()
    return document


def parse_fonts(document: Document):
    fontstore = FontStore(font_fromraw)

    content = [process_page(page, fontstore) for page in document.pages]
    header = fontstore.fonts

    return header, content


def process_page(page, fontstore):
    assert page
    container_index, line_index, char_index, font, scale, = 0, 0, 0, None, None
    result = []
    font_cur, scale_cur = None, None
    # TODO: use TextPageIter from groupme/hey! to iterate only over text boxes
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
                assert scale, 'negative font size'
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
    # save origin type to display on error
    save = raw_style
    if 'Regular' in raw_style:
        stretch = Stretch.REGULAR
        raw_style = raw_style.replace('Regular', '')
    if 'Regu' in raw_style:
        stretch = Stretch.REGULAR
        raw_style = raw_style.replace('Regu', '')
    if 'Bold' in raw_style:
        weight = Weight.BOLD
        raw_style = raw_style.replace('Bold', '')
    if 'Italic' in raw_style:
        style = Style.ITALIC
        raw_style = raw_style.replace('Italic', '')
    if 'Ital' in raw_style:
        style = Style.ITALIC
        raw_style = raw_style.replace('Ital', '')
    if 'Medi' in raw_style:
        weight = Weight.MEDIUM
        raw_style = raw_style.replace('Medi', '')
    if 'Oblique' in raw_style:
        style = Style.OBLIQUE
        raw_style = raw_style.replace('Oblique', '')
    if 'Obli' in raw_style:
        style = Style.OBLIQUE
        raw_style = raw_style.replace('Obli', '')

    if raw_style:  # TODO: Remove before going live
        logging_error(save)
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
    return Flag(longcut=name(), message='Extract fonts of document.')


def name():
    return 'fonts'
