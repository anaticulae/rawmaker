# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import file_create

from rawmaker import read
from rawmaker.features.fonts import work
from tests.resource import DOCUMENTATION_TWINE_PDF


def test_mining_fonts(testdir):
    header, content = None, None
    with read(DOCUMENTATION_TWINE_PDF) as pdf:
        result = work(pdf)
        header, content = result['header'], result['content']

    assert len(header) > 100
    assert len(content) > 300

    file_create('header.yaml', header)
    file_create('content.yaml', content)
