#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import power

import rawmaker

power.setup(rawmaker.ROOT)

RESOURCES = os.path.join(rawmaker.ROOT, 'tests/resources')
assert os.path.exists(RESOURCES), RESOURCES

EXAMPLES = os.path.join(rawmaker.ROOT, 'tests/examples')
assert os.path.exists(EXAMPLES), EXAMPLES

HELLO_WORLD = os.path.join(RESOURCES, 'helloworld')
NEGATIVE = os.path.join(RESOURCES, 'negative')
SINGLE = os.path.join(RESOURCES, 'single')
SPEC = os.path.join(RESOURCES, 'spec')
FONTS = os.path.join(RESOURCES, 'fonts')

NO_PDF = os.path.join(NEGATIVE, 'no_pdf')

VIM_PAGE_COUNT = 13
VIM_OUTLINES = 42

HELLO_WORLD_PDF = os.path.join(HELLO_WORLD, 'hello_world.pdf')
HELLO_WORLD_PAGES = 1
HELLO_WORLD_OUTLINES = 0

TWINE_PAGES = 35

INCREASING_FONT = os.path.join(RESOURCES, 'increasing_fonts')
INCREASING_FONT_A3 = os.path.join(INCREASING_FONT, 'increasing_fonts_a3.pdf')
INCREASING_FONT_A4 = os.path.join(INCREASING_FONT, 'increasing_fonts_a4.pdf')
INCREASING_FONT_A5 = os.path.join(INCREASING_FONT, 'increasing_fonts_a5.pdf')
INCREASING_ZZZ = os.path.join(INCREASING_FONT, 'increasing_fonts_a4_10_20_30_40.pdf') # yapf:disable

FONTS_SCALED_PDF = os.path.join(FONTS, 'scaled.pdf')
FONTS_SCALED = power.generated(folder='scaled')
FONTS_SCALED_PERCENT033 = os.path.join(FONTS_SCALED, 'page0_first.pdf')
FONTS_SCALED_PERCENT050 = os.path.join(FONTS_SCALED, 'page0_second.pdf')
FONTS_SCALED_PERCENT200 = os.path.join(FONTS_SCALED, 'page1_first.pdf')

HOW_TO_CPORTING_BOX_COUNT = 10
HOW_TO_CPORTING_HORIZONTAL_COUNT = 2

PDF2008 = os.path.join(SPEC, 'PDF32000_2008.pdf')

GOLDEN = os.path.join(RESOURCES, 'golden')
GOLDEN_VIM = os.path.join(GOLDEN, 'vim')

REQUIRED_RESOURCES = [
    # FONTS_SCALED_PERCENT033,
    # FONTS_SCALED_PERCENT050,
    # FONTS_SCALED_PERCENT200,
    GOLDEN_VIM,
    HELLO_WORLD_PDF,
    INCREASING_FONT,
    INCREASING_FONT_A3,
    INCREASING_FONT_A4,
    INCREASING_FONT_A5,
    NEGATIVE,
    NO_PDF,
    PDF2008,
    RESOURCES,
    # power.link(power.BACHELOR090_PDF),
    # power.link(power.BOOK007_PDF),
    # power.link(power.DOCU13_PDF),
]
