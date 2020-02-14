#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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

import contextlib
import functools
import typing

import iamraw
import serializeraw
import utila

import rawmaker.features
import rawmaker.reader


def work(
        document: str,
        boxes_flow: float = 0.5,
        char_margin: float = 2.0,
        line_margin: float = 0.5,
        line_overlap: float = 0.5,
        word_margin: float = 0.1,
        pages: list = None,
) -> typing.Tuple[str, str]:
    """Extract structured text out of document

    Args:
        document: pdf-document to run parsing
        char_margin(float): XXX:5.0 why?
        pages: limit analyzed area, if None every page is analyzed
    Returns:
        parsed document as yaml output
    """
    assert isinstance(document, str), str(document)
    layout = rawmaker.parameter.create_layout(
        boxes_flow=boxes_flow,
        char_margin=char_margin,
        line_margin=line_margin,
        line_overlap=line_overlap,
        word_margin=word_margin,
    )
    with rawmaker.reader.read(document) as pdf:
        document = rawmaker.features.extract_content(
            pdf,
            layout_parameter=layout,
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
        self.parser = parser if parser else font_fromraw
        self.data = {}

    @functools.lru_cache(maxsize=128)
    def font_key(self, raw_font: str, scale: float) -> int:
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


def process_page(
        page: iamraw.Page,
        fontstore: FontStore,
) -> iamraw.PageFontContent:
    """Iterate throw text container and save the different fonts and positions

    Args:
        page(Page): current pdf page
        fontstore(FontStore): fontstore to store full information of used font
    Returns:
        Page with content information.
    """
    assert isinstance(page, iamraw.Page), type(page)
    container_index, line_index, char_index = 0, 0, 0
    font, scale = None, None
    font_cur, scale_cur = None, None
    result = []

    # TODO: use TextPageIter from groupme/hey! to iterate only over text boxes
    textcontainer = [
        # remove non TextContainer items
        item for item in page.children if isinstance(item, iamraw.TextContainer)
    ]
    for item in textcontainer:
        for line_index, line in enumerate(item.lines):
            for char_index, char in enumerate(line):
                try:
                    font = char.font
                except AttributeError:
                    # Virtual chars have no fonts
                    continue

                # TODO: INVESTIGATE 1.34??
                # NOTE: This works for POSTSCRIPT_14_DEFAULT's but not for
                # Calibri.
                scale = round(char.size / 1.34005)
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

    return iamraw.PageFontContent(content=result, page=page.page)


def parse_fonts(document: iamraw.Document):
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


def parse_basefont(font: str):
    basefont = False
    with contextlib.suppress(IndexError):
        # see above
        # ('WTUVLZ+NimbusRomNo9L-Regu', 9.60),
        basefont = font[6] != '+'
    if basefont:
        # Example: Arial,Bold
        fontname, raw_style = font, ''
        with contextlib.suppress(ValueError):
            fontname, raw_style = font.split(',')
        style = parse_style(raw_style)
        return fontname, style
    return None


def parse_cidfont(font: str):
    cidfont = font.startswith('CIDFont+')
    if cidfont:
        # Example: CIDFont+F1
        # remove cid tag and plus sign
        fontname = font[8:]
        return fontname, None
    return None


def parse_default(font: str):
    # Example: LGAZPG + SegoeUI, Bold
    # remove base tag and plus sign
    font = font[7:]
    fontname, raw_style = font, ''
    # 'AIDZQU+Times-Roman' no style parsing is required
    style = None
    if font not in POSTSCRIPT_14_DEFAULT:
        with contextlib.suppress(ValueError):
            fontname, raw_style = font.split(',')
        with contextlib.suppress(ValueError):
            fontname, raw_style = font.split('-')
        try:
            style = parse_style(raw_style)
        except ValueError:
            fontname = font
    return fontname, style


def font_fromraw(font: str, scale: float) -> iamraw.Font:
    """Parse `Font` from pdf representation, read the description above.

    Args:
        font(str): pdf standard font definition
        scale(float): size of font(unit?)
    Returns:
        returns internal `Font` object with detected style and scale
    """
    utila.call('font_fromraw')
    utila.debug('%s %.2f' % (str(font), scale))
    # remove whitespaces to avoid missing PostScript 14 language cause of
    # containg whitespaces, for example `Times - Roman` instead of
    # `Times-Roman`.
    font = font.replace(' ', '')

    basefont = parse_basefont(font)
    cidfont = parse_cidfont(font)
    default = parse_default(font)

    fontname, style = None, None
    if cidfont is not None:
        # cidfont at first, cause cidfont selector is the clearest and not
        # ambigous.
        fontname, style = cidfont
    elif basefont is not None:
        fontname, style = basefont
    elif default is not None:
        fontname, style = default

    weight, style, stretch = style if style else (None, None, None)

    if '+' in fontname or ',' in fontname:
        utila.error(f'detected fontname {fontname};' 'input material {font}')

    font = iamraw.Font(
        name=fontname,
        scale=scale,
        stretch=stretch,
        style=style,
        weight=weight,
    )
    return font


def parse_style(raw_style):
    save = raw_style
    weight = iamraw.Weight.LIGHT
    style = iamraw.Style.NORMAL
    stretch = iamraw.Stretch.REGULAR
    if 'Regular' in raw_style:
        stretch = iamraw.Stretch.REGULAR
        raw_style = raw_style.replace('Regular', '')
    elif 'Regu' in raw_style:
        stretch = iamraw.Stretch.REGULAR
        raw_style = raw_style.replace('Regu', '')

    if 'Italic' in raw_style:
        style = iamraw.Style.ITALIC
        raw_style = raw_style.replace('Italic', '')
    elif 'Ital' in raw_style:
        style = iamraw.Style.ITALIC
        raw_style = raw_style.replace('Ital', '')
    elif 'Oblique' in raw_style:
        style = iamraw.Style.OBLIQUE
        raw_style = raw_style.replace('Oblique', '')
    elif 'Obli' in raw_style:
        style = iamraw.Style.OBLIQUE
        raw_style = raw_style.replace('Obli', '')

    if 'Bold' in raw_style:
        weight = iamraw.Weight.BOLD
        raw_style = raw_style.replace('Bold', '')
    elif 'Medium' in raw_style:
        weight = iamraw.Weight.MEDIUM
        raw_style = raw_style.replace('Medium', '')
    elif 'Medi' in raw_style:
        weight = iamraw.Weight.MEDIUM
        raw_style = raw_style.replace('Medi', '')

    if raw_style:  # TODO: Remove before going live
        # at the end, everything must be replaced
        utila.error(save)
        raise ValueError('Unsupported format %s' % raw_style)
    return weight, style, stretch
