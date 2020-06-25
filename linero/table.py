# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

TABLE_MIN_HEIGHT = 50  # TODO: HOLY VALUE


def valid_table(bounding, navigator) -> bool:
    height = bounding[3] - bounding[1]
    if height < TABLE_MIN_HEIGHT:
        # remove to small tables
        return False
    return True
