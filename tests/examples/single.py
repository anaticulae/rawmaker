# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import tests.resources

SINGLE = os.path.join(tests.resources.RESOURCES, 'single')
assert os.path.exists(SINGLE), SINGLE

HEADLINE_MOVINGFOOTER_FOOTNOTES_PDF = os.path.join(
    SINGLE,
    'headline_movingfooter_footnotes.pdf',
)

EXAMPLES = [
    HEADLINE_MOVINGFOOTER_FOOTNOTES_PDF,
    tests.resources.HELLO_WORLD_PDF,
]

for item in EXAMPLES:
    assert os.path.exists(item), str(item)
