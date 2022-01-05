# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator


def sort_leftright_topdown(items):
    # left to right
    items = sorted(items, key=operator.itemgetter(0))
    # top down
    items = sorted(items, key=operator.itemgetter(3))
    return items
