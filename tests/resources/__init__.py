#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import rawmaker

RESOURCES = os.path.join(rawmaker.ROOT, 'tests/resources')
assert os.path.exists(RESOURCES), RESOURCES

GENERATED = os.path.join(RESOURCES, 'generated')

EXAMPLES = os.path.join(rawmaker.ROOT, 'tests/examples')
assert os.path.exists(EXAMPLES), EXAMPLES

BACHELOR = os.path.join(RESOURCES, 'bachelor')
BOOK = os.path.join(RESOURCES, 'book')
DOCU = os.path.join(RESOURCES, 'docu')
HELLO_WORLD = os.path.join(RESOURCES, 'helloworld')
MASTER = os.path.join(RESOURCES, 'master')
NEGATIVE = os.path.join(RESOURCES, 'negative')
ORDER = os.path.join(RESOURCES, 'order')
SINGLE = os.path.join(RESOURCES, 'single')
TECHNICAL = os.path.join(RESOURCES, 'technical')
SPEC = os.path.join(RESOURCES, 'spec')

NO_PDF = os.path.join(NEGATIVE, 'no_pdf')

LEFTRIGHT = os.path.join(BOOK, 'leftright.pdf')
LEFTRIGHT_GENERATED = os.path.join(GENERATED, 'leftright')

VIM_PDF = os.path.join(DOCU, 'vimguide.pdf')
VIM_GENERATED = os.path.join(GENERATED, 'vim')

VIM_PAGE_COUNT = 13
VIM_OUTLINES = 42

HELLO_WORLD_PDF = os.path.join(HELLO_WORLD, 'hello_world.pdf')
HELLO_WORLD_PAGES = 1
HELLO_WORLD_OUTLINES = 0

TWINE_PDF = os.path.join(DOCU, 'twine.pdf')
TWINE_PAGES = 35

RESTRUCTURED_PDF = os.path.join(DOCU, 'restructuredtext.pdf')

INCREASING_FONT = os.path.join(RESOURCES, 'increasing_fonts')
INCREASING_FONT_A3 = os.path.join(INCREASING_FONT, 'increasing_fonts_a3.pdf')
INCREASING_FONT_A4 = os.path.join(INCREASING_FONT, 'increasing_fonts_a4.pdf')
INCREASING_FONT_A5 = os.path.join(INCREASING_FONT, 'increasing_fonts_a5.pdf')
INCREASING_ZZZ = os.path.join(INCREASING_FONT, 'increasing_fonts_a4_10_20_30_40.pdf') # yapf:disable

HOW_TO_CPORTING_PDF = os.path.join(DOCU, 'porting_extension_modules.pdf')

HOW_TO_CPORTING_BOX_COUNT = 10
HOW_TO_CPORTING_HORIZONTAL_COUNT = 2

MASTER72 = os.path.join(MASTER, 'page_72_noimages_toc.pdf')

HOWTOREAD_PDF = os.path.join(ORDER, 'howtowrite_pages9.pdf')

BACHELOR37 = os.path.join(BACHELOR, 'page_37_tables.pdf')
BACHELOR56 = os.path.join(BACHELOR, 'page_56_hard_to_read.pdf')
BACHELOR63 = os.path.join(BACHELOR, 'page_63_images_toc.pdf')
PDF2008 = os.path.join(SPEC, 'PDF32000_2008.pdf')

MASTER116 = os.path.join(MASTER, 'page_116_images_toc_formular.pdf')

REQUIRED_RESOURCES = [
    BACHELOR,
    BACHELOR37,
    BACHELOR56,
    BACHELOR63,
    GENERATED,
    HELLO_WORLD_PDF,
    HOWTOREAD_PDF,
    HOW_TO_CPORTING_PDF,
    INCREASING_FONT,
    INCREASING_FONT_A3,
    INCREASING_FONT_A4,
    INCREASING_FONT_A5,
    LEFTRIGHT,
    MASTER116,
    MASTER72,
    NEGATIVE,
    NO_PDF,
    PDF2008,
    RESOURCES,
    RESTRUCTURED_PDF,
    TECHNICAL,
    TWINE_PDF,
    VIM_PDF,
]
