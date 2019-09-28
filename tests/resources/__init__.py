#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os
from os.path import exists
from os.path import join

from rawmaker import ROOT

RESOURCES = os.path.join(ROOT, 'tests/resources')
assert exists(RESOURCES), RESOURCES

BACHELOR = os.path.join(RESOURCES, 'bachelor')
MASTER = os.path.join(RESOURCES, 'master')
NEGATIVE = os.path.join(RESOURCES, 'negative')
HELLO_WORLD = join(RESOURCES, 'helloworld')
TECHNICAL = os.path.join(RESOURCES, 'technical')

NO_PDF = join(NEGATIVE, 'no_pdf')

VIM_GUIDE_PDF = join(RESOURCES, 'vimguide.pdf')
VIM_GUIDE_PAGE_COUNT = 13
VIM_GUIDE_OUTLINES = 42

HELLO_WORLD_PDF = join(HELLO_WORLD, 'hello_world.pdf')
HELLO_WORLD_PAGES = 1
HELLO_WORLD_OUTLINES = 0

DOCUMENTATION_TWINE = join(TECHNICAL, 'twine')
DOCUMENTATION_TWINE_PDF = join(DOCUMENTATION_TWINE, 'documentation_twine.pdf')
DOCUMENTATION_TWINE_PAGES = 35

TOC_PDF = join(RESOURCES, 'toc/restructuredtext.pdf')
RESTRUCTURED_PDF = TOC_PDF

PORTING_PYTHON3 = os.path.join(RESOURCES, 'broken/broken_annotation/porting_python3.pdf') # yapf:disable


INCREASING_FONT = join(RESOURCES, 'increasing_fonts')
INCREASING_FONT_A3 = join(INCREASING_FONT, 'increasing_fonts_a3.pdf')
INCREASING_FONT_A4 = join(INCREASING_FONT, 'increasing_fonts_a4.pdf')
INCREASING_FONT_A5 = join(INCREASING_FONT, 'increasing_fonts_a5.pdf')

HOW_TO_CPORTING = join(RESOURCES, 'boxes')
HOW_TO_CPORTING_PDF = join(HOW_TO_CPORTING, 'howto_cporting.pdf')
assert exists(HOW_TO_CPORTING), HOW_TO_CPORTING
assert exists(HOW_TO_CPORTING_PDF), HOW_TO_CPORTING_PDF

HOW_TO_CPORTING_BOX_COUNT = 10
HOW_TO_CPORTING_HORIZONTAL_COUNT = 2

MASTER_72_NOIMAGES_TOC = os.path.join(MASTER, 'page_72_noimages_toc.pdf')
assert os.path.exists(MASTER_72_NOIMAGES_TOC), str(MASTER_72_NOIMAGES_TOC)

REQUIRED_RESOURCES = [
    BACHELOR,
    DOCUMENTATION_TWINE_PDF,
    HELLO_WORLD_PDF,
    INCREASING_FONT,
    INCREASING_FONT_A3,
    INCREASING_FONT_A4,
    INCREASING_FONT_A5,
    MASTER_72_NOIMAGES_TOC,
    NEGATIVE,
    NO_PDF,
    PORTING_PYTHON3,
    RESOURCES,
    TECHNICAL,
    TOC_PDF,
    VIM_GUIDE_PDF,
]

MISSING = [item for item in REQUIRED_RESOURCES if not os.path.exists(item)]
assert not MISSING, f'missing: {MISSING}'
