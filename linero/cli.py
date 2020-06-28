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
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'line_line'),
        ],
        ('table',),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=linero.ROOT,
        featurepackage='linero.features',
        config=utila.FeaturePackConfig(
            description=linero.DESCRIPTION,
            multiprocessed=True,
            name=linero.PROCESS,
            pages=True,
            profileflag=True,
            singleinput=True,
            verboseflag=True,
            version=linero.__version__,
        ),
    )
