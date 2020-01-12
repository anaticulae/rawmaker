# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import rawmaker.utils


def test_rawmaker_utils_chunks():
    items = list(range(12))
    splitted = rawmaker.utils.chunks(items, chunk_size=5)
    assert len(splitted) == 3
    assert len(splitted[-1]) == 2
