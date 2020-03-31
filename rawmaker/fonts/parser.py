# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Font Parser

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

import iamraw
import serializeraw
import utila

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


def font_fromraw(font: str, scale: float, flags: int = 0) -> iamraw.Font:
    """Parse `Font` from pdf representation, read the description above.

    Args:
        font(str): pdf standard font definition
        scale(float): size of font(unit?)
        flags(int): style of rendered font
    Returns:
        returns internal `Font` object with detected style and scale
    """
    utila.call('rawmaker.fonts.parser.font_fromraw')
    utila.debug('%s %.2f' % (str(font), scale))
    flags = serializeraw.load_flags(flags)
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
        utila.error(f'detected fontname {fontname}; input: {font}')

    font = iamraw.Font(
        name=fontname,
        scale=scale,
        stretch=stretch,
        style=style,
        weight=weight,
        flags=flags,
    )
    return font


def parse_basefont(font: str):
    basefont = True
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
    if fontname in POSTSCRIPT_14_DEFAULT:
        return fontname, None

    style = None
    with contextlib.suppress(ValueError):
        fontname, raw_style = font.split(',')
    with contextlib.suppress(ValueError):
        fontname, raw_style = font.split('-')
    style = parse_style(raw_style)
    return fontname, style


def parse_style(raw_style):  # pylint:disable=R1260,R0912
    save = raw_style
    if 'Regular' in raw_style:
        stretch = iamraw.Stretch.REGULAR
        raw_style = raw_style.replace('Regular', '')
    elif 'Regu' in raw_style:
        stretch = iamraw.Stretch.REGULAR
        raw_style = raw_style.replace('Regu', '')
    else:
        stretch = iamraw.Stretch.REGULAR

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
    else:
        style = iamraw.Style.NORMAL

    if 'Bold' in raw_style:
        weight = iamraw.Weight.BOLD
        raw_style = raw_style.replace('Bold', '')
    elif 'Medium' in raw_style:
        weight = iamraw.Weight.MEDIUM
        raw_style = raw_style.replace('Medium', '')
    elif 'Medi' in raw_style:
        weight = iamraw.Weight.MEDIUM
        raw_style = raw_style.replace('Medi', '')
    else:
        weight = iamraw.Weight.LIGHT

    if raw_style:  # TODO: Remove before going live
        # at the end, everything must be replaced
        utila.error(f'unsupported style {save}, maybe a name: {raw_style}')
    return weight, style, stretch
