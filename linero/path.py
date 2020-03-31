# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import linero

# TODO: ENABLE DOCTEST AFTER FIXING UTILA


def table(path: str, prefix: str = '') -> str:
    """Path to extraction result of linero --table step.
    >>> table('/data/resources') # doctest: +SKIP
    '/data/resources/linero__table_table.yaml
    """
    return utila.pathconnector(
        path,
        linero.PROCESS,
        'table_table',
        prefix,
    )


def figure(path: str, prefix: str = '') -> str:
    """Path to extraction result of linero --figure step.
    >>> table('/data/resources') # doctest: +SKIP
    '/data/resources/linero__figure_figure.yaml
    """
    return utila.pathconnector(
        path,
        linero.PROCESS,
        'figure_figure',
        prefix,
    )
