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

EXAMPLES = os.path.join(rawmaker.ROOT, 'tests/examples')
assert os.path.exists(EXAMPLES), EXAMPLES

BACHELOR = os.path.join(RESOURCES, 'bachelor')
MASTER = os.path.join(RESOURCES, 'master')
NEGATIVE = os.path.join(RESOURCES, 'negative')
HELLO_WORLD = os.path.join(RESOURCES, 'helloworld')
TECHNICAL = os.path.join(RESOURCES, 'technical')
SINGLE = os.path.join(RESOURCES, 'single')

NO_PDF = os.path.join(NEGATIVE, 'no_pdf')

VIM_PDF = os.path.join(RESOURCES, 'vimguide.pdf')
VIM_PAGE_COUNT = 13
VIM_OUTLINES = 42

HELLO_WORLD_PDF = os.path.join(HELLO_WORLD, 'hello_world.pdf')
HELLO_WORLD_PAGES = 1
HELLO_WORLD_OUTLINES = 0

TWINE = os.path.join(TECHNICAL, 'twine')
TWINE_PDF = os.path.join(TWINE, 'documentation_twine.pdf')
TWINE_PAGES = 35

TOC_PDF = os.path.join(RESOURCES, 'toc/restructuredtext.pdf')
RESTRUCTURED_PDF = TOC_PDF

PORTING_PYTHON3 = os.path.join(RESOURCES, 'broken/broken_annotation/porting_python3.pdf') # yapf:disable


INCREASING_FONT = os.path.join(RESOURCES, 'increasing_fonts')
INCREASING_FONT_A3 = os.path.join(INCREASING_FONT, 'increasing_fonts_a3.pdf')
INCREASING_FONT_A4 = os.path.join(INCREASING_FONT, 'increasing_fonts_a4.pdf')
INCREASING_FONT_A5 = os.path.join(INCREASING_FONT, 'increasing_fonts_a5.pdf')
INCREASING_ZZZ = os.path.join(INCREASING_FONT, 'increasing_fonts_a4_10_20_30_40.pdf') # yapf:disable

HOW_TO_CPORTING = os.path.join(RESOURCES, 'boxes')
HOW_TO_CPORTING_PDF = os.path.join(HOW_TO_CPORTING, 'howto_cporting.pdf')
assert os.path.exists(HOW_TO_CPORTING), HOW_TO_CPORTING
assert os.path.exists(HOW_TO_CPORTING_PDF), HOW_TO_CPORTING_PDF

HOW_TO_CPORTING_BOX_COUNT = 10
HOW_TO_CPORTING_HORIZONTAL_COUNT = 2

MASTER72 = os.path.join(MASTER, 'page_72_noimages_toc.pdf')
assert os.path.exists(MASTER72), str(MASTER72)

BACHELOR63 = os.path.join(BACHELOR, 'page_63_images_toc.pdf')

SINGLE_HEADLINE_MOVINGFOOTER = os.path.join(
    SINGLE,
    'headline_movingfooter_footnotes.pdf',
)

MASTER116 = os.path.join(MASTER, 'page_116_images_toc_formular.pdf')

REQUIRED_RESOURCES = [
    BACHELOR,
    BACHELOR63,
    TWINE_PDF,
    HELLO_WORLD_PDF,
    INCREASING_FONT,
    INCREASING_FONT_A3,
    INCREASING_FONT_A4,
    INCREASING_FONT_A5,
    MASTER116,
    MASTER72,
    NEGATIVE,
    NO_PDF,
    PORTING_PYTHON3,
    RESOURCES,
    SINGLE_HEADLINE_MOVINGFOOTER,
    TECHNICAL,
    TOC_PDF,
    VIM_PDF,
]

MISSING = [item for item in REQUIRED_RESOURCES if not os.path.exists(item)]
assert not MISSING, f'missing: {MISSING}'
