#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from os.path import exists
from os.path import join

from rawmaker import ROOT

DATA = join(ROOT, 'tests/data')
assert exists(DATA), DATA

NEGATIVE = join(DATA, 'negative')

NO_PDF = join(NEGATIVE, 'no_pdf.pdf')

VIM_GUIDE_PDF = join(DATA, 'vimguide.pdf')
VIM_GUIDE_PAGES = 13
VIM_GUIDE_OUTLINES = 42

HELLO_WORLD = join(DATA, 'helloworld')
HELLO_WORLD_PDF = join(HELLO_WORLD, 'hello_world.pdf')
HELLO_WORLD_PAGES = 1
HELLO_WORLD_OUTLINES = 0

DOCUMENTATION_TWINE = join(DATA, 'technical/twine')
DOCUMENTATION_TWINE_PDF = join(DOCUMENTATION_TWINE, 'documentation_twine.pdf')
DOCUMENTATION_TWINE_PAGES = 35

for item in [NO_PDF, VIM_GUIDE_PDF]:
    assert exists(item), item

INCREASING_FONT = join(DATA, 'increasing_fonts')
INCREASING_FONT_A3 = join(INCREASING_FONT, 'increasing_fonts_a3.pdf')
INCREASING_FONT_A4 = join(INCREASING_FONT, 'increasing_fonts_a4.pdf')
INCREASING_FONT_A5 = join(INCREASING_FONT, 'increasing_fonts_a5.pdf')

for item in [
        INCREASING_FONT,
        INCREASING_FONT_A3,
        INCREASING_FONT_A4,
        INCREASING_FONT_A5,
]:
    assert exists(item), item
