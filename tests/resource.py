#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
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

VIM_GUIDE = join(DATA, 'vimguide.pdf')
VIM_GUIDE_PAGES = 13
VIM_GUIDE_OUTLINES = 42

for item in [NO_PDF, VIM_GUIDE]:
    assert exists(item), item
