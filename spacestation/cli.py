# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import spacestation

WORKPLAN = [
    utilo.create_step(
        name='wspace',
        inputs=[utilo.Pattern('*', 'pdf')],
        output=('wspace', 'words'),
    ),
    utilo.create_step(
        name='chardist',
        inputs=[
            utilo.ResultFile(producer='spacestation', name='wspace_words'),
        ],
        output=('chardist',),
    ),
    utilo.create_step(
        name='worddist',
        inputs=[
            utilo.ResultFile(producer='spacestation', name='wspace_wspace'),
        ],
        output=('worddist',),
    ),
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=spacestation.ROOT,
        featurepackage='spacestation.features',
        config=utilo.FeaturePackConfig(
            description=spacestation.DESCRIPTION,
            multiprocessed=True,
            name=spacestation.PROCESS,
            pages=True,
            profileflag=True,
            singleinput=True,
            version=spacestation.__version__,
        ),
    )
