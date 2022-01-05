# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import spacestation

WORKPLAN = [
    utila.create_step(
        name='wspace',
        inputs=[utila.Pattern('*', 'pdf')],
        output=('wspace', 'words'),
    ),
    utila.create_step(
        name='chardist',
        inputs=[
            utila.ResultFile(producer='spacestation', name='wspace_words'),
        ],
        output=('chardist',),
    ),
    utila.create_step(
        name='worddist',
        inputs=[
            utila.ResultFile(producer='spacestation', name='wspace_wspace'),
        ],
        output=('worddist',),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=spacestation.ROOT,
        featurepackage='spacestation.features',
        config=utila.FeaturePackConfig(
            description=spacestation.DESCRIPTION,
            multiprocessed=True,
            name=spacestation.PROCESS,
            pages=True,
            profileflag=True,
            singleinput=True,
            version=spacestation.__version__,
        ),
    )
