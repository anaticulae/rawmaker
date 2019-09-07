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


PDF Font description:

9.5. Introduction into Font Data Structures

Font types

    Type0
    Type1           Type1
                    MMType1: MultiMaster Font
    Type3           stream of pdf graphic operators
    TrueType        Based on TrueType font format
    CIDFont         CIDFontType0
                    CIDFontType2

9.6.2.2 Standard Type 1 Fonts

    uses compact encoding for glyph description and additonal hints to print
    on small sizes and solutions well.

    PostScript 14 standard types:
        Times-Roman, Helvectica, Courier, Symbol, Times-Bold,
        Helvetica-Bold, Courier-Bold, ZapfDingbats, Times-Italic,
        Helvetica-Oblique, Courier-Oblique, Times-BoldItalic,
        Helvetica-BoldOblique, Courier-BoldOblique.

9.6.2.3 MultiMasterFonts

9.6.3. TrueTypeFonts

9.6.4. Font Subsets

    BaseFont
    FontName

    Tag(6 chars) +

    Example: EOODIA+Poetica - name of a subset of Poetica, a Type 1 font.

9.6.5 Type 3 Fonts

    Defined by a stream of pdf graphic commands, no special support or hint
    for very small characters.

9.7.4 CIDFonts

    CIDFont program contains glyph descriptions that are accessed using a CID
    as a character selector.

Summary:

    Font Type 0
        ('Helvetica - Bold', 16.70),
        ('Times - Roman', 13.40),
    Font Type 1, TrueType Fonts:
        ('ZTJCPR + NimbusRomNo9L - MediItal', 11.60),
        ('KCXMNX + TeX - feymr10', 10.70),
"""

from contextlib import suppress
from functools import lru_cache
from typing import Tuple

from iamraw import Document
from iamraw import Font
from iamraw import Page
from iamraw import PageFontContent
from iamraw import Stretch
from iamraw import Style
from iamraw import TextContainer
from iamraw import Weight
from serializeraw import dump_font_content
from serializeraw import dump_font_header
from utila import Flag
from utila import call
from utila import debug
from utila import error

from rawmaker.features import extract_content
from rawmaker.parameter import create_layout
from rawmaker.reader import read


def work(
        document: str,
        boxes_flow: float = 0.5,
        char_margin: float = 2.0,
        line_margin: float = 0.5,
        line_overlap: float = 0.5,
        word_margin: float = 0.1,
        pages: list = None,
) -> Tuple[str, str]:
    """Extract structured text out of document

    Args:
        document: pdf-document to run parsing
        char_margin(float): XXX:5.0 why?
        pages: limit analyzed area, if None every page is analyzed
    Returns:
        parsed document as yaml output
    """
    assert isinstance(document, str), str(document)
    layout = create_layout(
        boxes_flow=boxes_flow,
        char_margin=char_margin,
        line_margin=line_margin,
        line_overlap=line_overlap,
        word_margin=word_margin,
    )
    with read(document) as pdf:
        document = extract_content(pdf, layout_parameter=layout, pages=pages)

    header, content = parse_fonts(document)
    header, content = dump_font_header(header), dump_font_content(content)
    return header, content


class FontStore:

    def __init__(self, parser=None):
        parser = parser if parser else font_fromraw
        self.data = {}
        self.parser = parser

    @lru_cache(maxsize=128)
    def font_key(self, raw_font: str, scale: float) -> int:
        # parsed = font_fromraw(raw_font, scale)
        parsed = self.parser(raw_font, scale)
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


def process_page(page: Page, fontstore: FontStore) -> PageFontContent:
    """Iterate throw text container and save the different fonts and positions

    Args:
        page(Page): current pdf page
        fontstore(): fontstore to save new fonts

    """
    assert isinstance(page, Page), type(page)
    container_index, line_index, char_index = 0, 0, 0
    font, scale = None, None
    font_cur, scale_cur = None, None
    result = []
    # TODO: use TextPageIter from groupme/hey! to iterate only over text boxes

    textcontainer = [
        # remove non TextContainer items
        item for item in page.children if isinstance(item, TextContainer)
    ]
    for item in textcontainer:
        for line_index, line in enumerate(item.lines):
            for char_index, char in enumerate(line):
                try:
                    font = char.font
                except AttributeError:
                    # Virtual chars have no fonts
                    continue

                # fontscale = y1 - y0
                scale = round((char.box[3] - char.box[1]), 1)
                assert scale > 0, 'negative font size'
                # No font type or size is selected
                if font_cur is None:
                    font_cur, scale_cur = font, scale
                    continue

                # Font type or size changed
                if font_cur != font or scale_cur != scale:
                    result.append(
                        determine_font(
                            font_cur,
                            scale_cur,
                            container_index,
                            line_index,
                            char_index,
                            fontstore,
                        ))
                    # Reset current front
                    font_cur, scale_cur = font, scale
        container_index += 1
    # add last text line of a page, because there is nothing changing
    if font_cur:
        result.append(
            determine_font(
                font,
                scale,
                container_index - 1,  # revert last index incrementation
                line_index,
                char_index,
                fontstore,
            ))

    return PageFontContent(content=result, page=page.page)


def parse_fonts(document: Document):
    fontstore = FontStore(font_fromraw)

    content = [process_page(page, fontstore) for page in document.pages]
    header = fontstore.fonts()

    return header, content


def determine_font(font, scale, container, line, char, fontstore):
    fontkey = fontstore.font_key(font, scale)
    return (container, line, char, fontkey)


POSTSCRIPT_14_DEFAULT = {
    'Courier',
    'Courier-Bold',
    'Courier-BoldOblique',
    'Courier-Oblique',
    'Helvectica',
    'Helvetica-Bold',
    'Helvetica-BoldOblique',
    'Helvetica-Oblique',
    'Symbol',
    'Times-Bold',
    'Times-BoldItalic',
    'Times-Italic',
    'Times-Roman',
    'ZapfDingbats',
}


def font_fromraw(font: str, scale: float) -> Font:
    """Parse `Font` from pdf representation, read the description above.

    Args:
        font(str): pdf standard font definition
        scale(float): size of font(unit?)
    Returns:
        returns internal `Font` object with detected style and scale
    """
    call('font_fromraw')
    debug('%s %.2f' % (str(font), scale))

    def remove_whitespaces(content):
        # remove whitespaces to avoid missing PostScript 14 language cause of
        # containg whitespaces, for example `Times - Roman` instead of
        # `Times-Roman`.
        return content.replace(' ', '')

    font = remove_whitespaces(font)

    basefont = True
    with suppress(IndexError):
        # see above
        # ('WTUVLZ+NimbusRomNo9L-Regu', 9.60),
        basefont = font[6] != '+'

    cidfont = font.startswith('CIDFont+')

    # save origin type to display on error
    save = font

    weight, style, stretch = None, None, None
    if cidfont:
        # Example: CIDFont+F1
        # remove cid tag and plus sign
        font = font[8:]
        fontname = font
    elif basefont:
        # Example: Arial,Bold
        fontname, raw_style = font, ''
        with suppress(ValueError):
            fontname, raw_style = font.split(',')
        weight, style, stretch = parse_style(raw_style)
    else:
        # Example: LGAZPG + SegoeUI, Bold
        # remove base tag and plus sign
        font = font[7:]
        fontname, raw_style = font, ''
        # 'AIDZQU+Times-Roman' no style parsing is required
        if not font in POSTSCRIPT_14_DEFAULT:
            with suppress(ValueError):
                fontname, raw_style = font.split(',')
            with suppress(ValueError):
                fontname, raw_style = font.split('-')
            weight, style, stretch = parse_style(raw_style)

    msg = 'detected fontname %s; input material %s' % (fontname, save)
    assert '+' not in fontname, msg
    assert ',' not in fontname, msg

    font = Font(
        name=fontname,
        scale=scale,
        stretch=stretch,
        style=style,
        weight=weight,
    )
    return font


def parse_style(raw_style):
    save = raw_style
    weight, style, stretch = Weight.LIGHT, Style.NORMAL, Stretch.REGULAR
    if 'Regular' in raw_style:
        stretch = Stretch.REGULAR
        raw_style = raw_style.replace('Regular', '')
    if 'Regu' in raw_style:
        stretch = Stretch.REGULAR
        raw_style = raw_style.replace('Regu', '')

    if 'Italic' in raw_style:
        style = Style.ITALIC
        raw_style = raw_style.replace('Italic', '')
    if 'Ital' in raw_style:
        style = Style.ITALIC
        raw_style = raw_style.replace('Ital', '')
    if 'Oblique' in raw_style:
        style = Style.OBLIQUE
        raw_style = raw_style.replace('Oblique', '')
    if 'Obli' in raw_style:
        style = Style.OBLIQUE
        raw_style = raw_style.replace('Obli', '')

    if 'Bold' in raw_style:
        weight = Weight.BOLD
        raw_style = raw_style.replace('Bold', '')
    if 'Medium' in raw_style:
        weight = Weight.MEDIUM
        raw_style = raw_style.replace('Medium', '')
    if 'Medi' in raw_style:
        weight = Weight.MEDIUM
        raw_style = raw_style.replace('Medi', '')

    if raw_style:  # TODO: Remove before going live
        # at the end, everything must be replaced
        error(save)
        raise ValueError('Unsupported format %s' % raw_style)
    return weight, style, stretch


def commandline():
    return Flag(longcut=name(), message='Extract fonts of document.')


def name():
    return 'fonts'
