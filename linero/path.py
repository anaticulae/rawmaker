# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import linero
import rawmaker.path


def table(path: str, prefix: str = '') -> str:
    return rawmaker.path.pathconnector(
        path,
        linero.PROCESS,
        'table_table',
        prefix,
    )


def figure(path: str, prefix: str = '') -> str:
    return rawmaker.path.pathconnector(
        path,
        linero.PROCESS,
        'figure_figure',
        prefix,
    )
