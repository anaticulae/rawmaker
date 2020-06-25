# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

TABLE_MIN_HEIGHT = 50  # TODO: HOLY VALUE
MAX_SINGLE_LINE_QUOTE = 0.2


def valid_table(bounding, navigator) -> bool:
    top, bottom = bounding[1], bounding[3]

    height = bottom - top
    if height < TABLE_MIN_HEIGHT:
        # remove to small tables
        return False

    table_content = navigator.between(
        top / navigator.height,
        bottom / navigator.height,
    )
    if not table_content:
        # no content in table
        return False

    boundings = [item.bounding for item in table_content]
    clustered = utila.same_line_cluster(
        boundings,
        min_elements=1,
    )
    singles = len([item for item in clustered if len(item) == 1])
    single_quote = singles / len(clustered)
    if singles >= 2 and single_quote > MAX_SINGLE_LINE_QUOTE:
        # invalid table content
        return False

    # table seems to be valid
    return True
