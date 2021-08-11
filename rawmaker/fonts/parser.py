# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

    uses compact encoding for glyph description and additional hints to print
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
import iamraw.fonts
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


def font_fromraw(font: str, scale: float = 0.0, flags: int = 0) -> iamraw.Font:
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
    # remove white spaces to avoid missing PostScript 14 language cause of
    # containg white spaces, for example `Times - Roman` instead of
    # `Times-Roman`.
    font = font.replace(' ', '')
    # parse different fonts
    basefont = parse_basefont(font)
    cidfont = parse_cidfont(font)
    default = parse_default(font)
    styled = parse_font_styled(font)
    simple = parse_font_simple(font)
    # select best font parsing
    fontname, style = None, None
    if cidfont is not None:
        # cidfont at first, cause cidfont selector is the clearest and not
        # ambigous.
        fontname, style = cidfont
    elif simple:
        fontname, style = simple
    elif styled:
        fontname, style = styled
    elif basefont is not None:
        fontname, style = basefont
    elif default is not None:
        fontname, style = default
    # use default style if no style is given
    weight, style, stretch = style if style else (None, None, None)
    # inform about parsing problem
    if fontname is None or '+' in fontname or ',' in fontname:
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
    """\
    >>> parse_basefont('Arial,Bold')
    ('Arial',...Weight.BOLD...)
    >>> parse_basefont('WTUVLZ+NimbusRomNo9L-Regu') is None
    True
    """
    if '+' in font:
        return None
    # Example: Arial,Bold
    fontname, raw_style = font, ''
    with contextlib.suppress(ValueError):
        fontname, raw_style = font.split(',')
    style = parse_style(raw_style)
    if not style:
        return None
    return fontname, style


def parse_cidfont(font: str):
    """\
    >>> parse_cidfont('CIDFont+F1')
    ('F1', None)
    """
    cidfont = font.startswith('CIDFont+')
    if not cidfont:
        return None
    # Example: CIDFont+F1
    # remove cid tag and plus sign
    fontname = font[8:]
    return fontname, None


def parse_postscript14(fontname: str):
    if fontname not in POSTSCRIPT_14_DEFAULT:
        return None
    if '-' not in fontname:
        # Courier
        return fontname, None
    # 'Courier-Oblique',
    fontname, style = fontname.split('-')
    style = parse_style(style)
    return fontname, style


def parse_default(font: str):
    # Example: LGAZPG + SegoeUI, Bold
    # remove base tag and plus sign
    font = font[7:]
    fontname, raw_style = font, ''

    parsed = parse_postscript14(font)
    if parsed:
        # 'AIDZQU+Times-Roman' no style parsing is required
        return parsed

    style = None
    with contextlib.suppress(ValueError):
        fontname, raw_style = font.split(',')
    with contextlib.suppress(ValueError):
        fontname, raw_style = font.split('-')
    style = parse_style(raw_style)
    if not raw_style:
        parsed = parse_font_simple(fontname)
        if parsed:
            fontname, style = parsed
    if not style:
        # TODO: FONT STYLE PARSER
        return fontname, None
    return fontname, style


def parse_font_styled(font: str):
    if not font.count('-') == 1 or '+' in font:
        return None
    name, style = font.split('-')
    style = parse_style(style)

    if not style:
        return None
    name = named(name)
    return name, style


def parse_font_simple(font: str):
    if any(char in font for char in ['+', '-', ',']):
        return None
    styles = []
    for item in STYLES:
        if item[0] not in font:
            continue
        styles.append((item[1], item[2], item[3]))
        font = font.replace(item[0], '')

    weight, style, stretch = MEDIUM, NORMAL, REGULAR
    for item in styles:
        if item[0]:
            weight = item[0]
        if item[1]:
            style = item[1]
        if item[2]:
            stretch = item[2]
    return font, (weight, style, stretch)


def named(font: str):
    for item in STYLES:
        font = font.replace(item[0], '')
    return font


def font_toraw(font: iamraw.Font) -> str:
    result = font.name
    selected = {font.weight, font.style, font.stretch}
    if not any(selected):
        # no style given, do not use default style
        return f'CIDFont+{result}'
    styles = [
        ('Bd', BOLD, None, None),
        ('Italic', None, ITALIC, None),
        ('Medium', MEDIUM, None, None),
        ('Oblique', None, OBLIQUE, None),
        ('Regular', None, None, REGULAR),
        ('Light', LIGHT, None, None),
    ]
    for raw, *items in styles:
        if not any(item for item in items if item in selected):
            continue
        result += raw
    return result


def parse_style(raw_style):  # pylint:disable=R1260,R0912
    save = raw_style
    weight, style, stretch = LIGHT, NORMAL, REGULAR
    for item in STYLES:
        if item[0] not in raw_style:
            continue
        raw_style = raw_style.replace(item[0], '')
        if item[1]:
            weight = item[1]  # pylint:disable=R0204
        if item[2]:
            style = item[2]
        if item[3]:
            stretch = item[3]
    if raw_style:  # TODO: Remove before going live
        # at the end, everything must be replaced
        utila.error(f'unsupported style {save}, maybe a name: {raw_style}')
    if raw_style:
        return None
    return weight, style, stretch


BOLD = iamraw.Weight.BOLD
ITALIC = iamraw.Style.ITALIC
LIGHT = iamraw.Weight.LIGHT
MEDIUM = iamraw.Weight.MEDIUM
NORMAL = iamraw.Style.NORMAL
OBLIQUE = iamraw.Style.OBLIQUE
REGULAR = iamraw.Stretch.REGULAR

# TODO: INVESTIGATE MT
# BOLD = BOLD
# MT = MEDIUM
# HOW TO DEAL WITH BOLD MT?

STYLES = [
    ('Bd', BOLD, None, None),
    ('Italic', None, ITALIC, None),
    ('Ital', None, ITALIC, None),
    # ('MI', MEDIUM, ITALIC, None),
    ('Medium', MEDIUM, None, None),
    ('Medi', MEDIUM, None, None),
    # ('M', MEDIUM, None, None),  # HOW TO DEAL WITH ?BOLDMT?
    ('MT', None, None, None),  # HOW TO DEAL WITH ?BOLDMT? TODO: DECIDE LATER
    ('Bold', BOLD, None, None),  # HOW TO DEAL WITH ?BOLDMT?
    ('Oblique', None, OBLIQUE, None),
    ('Obli', None, OBLIQUE, None),
    ('PSMT', MEDIUM, None, None),
    ('PS', MEDIUM, None, None),
    ('Regular', None, None, REGULAR),
    ('Regu', None, None, REGULAR),
    ('Rg', None, None, REGULAR),
    ('Light', LIGHT, None, None),
]
#  TODO: Roman converts TimesNewRoman to TimesNew. I could not verify if
#  that is a smart necessary option or it will introduce more problems?
# ('Roman', None, None, None),
