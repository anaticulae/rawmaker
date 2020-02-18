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

WORKPLAN = [
    utila.create_step(
        'table',
        [
            utila.ResultFile('rawmaker', 'line_line'),
        ],
        ('table',),
    ),
    utila.create_step(
        'figure',
        [
            utila.ResultFile('rawmaker', 'line_line'),
        ],
        ('figure',),
    )
]


def main():
    utila.featurepack(
        description=linero.DESCRIPTION,
        featurepackage='linero.features',
        multiprocessed=True,
        name=linero.PROCESS,
        pages=True,
        profileflag=True,
        root=linero.ROOT,
        singleinput=True,
        version=linero.__version__,
        workplan=WORKPLAN,
    )
