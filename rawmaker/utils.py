# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math


def chunks(items, chunk_size: int = 10) -> tuple:
    """Split `items` by `chunk_size`.

    Args:
        items(iterable): content to split
        chunk_size(int): maximal length of splitted chunk
    Returns:
        Tuple of splitted chunks.
    """
    result = tuple([
        items[index * chunk_size:(index + 1) * chunk_size]
        for index in range(math.ceil(len(items) / chunk_size))
    ])
    return result
