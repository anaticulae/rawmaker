# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import rawmaker

PROCESS = 'rawmaker_cleanup'
DESCRIPTION = """\
Load PageTextNavigators, codes, figures and tables.

It removes text which is inside codes, figures and or tables and writes
PageTextNavigators afterwards.
"""

WORKPLAN = [
    utila.create_step('backup'),
    utila.create_step(
        'cleanup',
        inputs=[
            utila.Value('postfix', str, defaultvar=''),
        ],
    ),
    utila.create_step(
        'translate',
        inputs=[
            utila.ResultFile(
                producer='rawmaker',
                name='text_text',
                optional=True,
            ),
            utila.ResultFile(
                producer='rawmaker',
                name='text_text',
                ext='baml',
                optional=True,
            ),
            utila.ResultFile(
                producer='rawmaker',
                name='oneline_text_text',
                optional=True,
            ),
            utila.ResultFile(
                producer='rawmaker',
                name='oneline_text_text',
                ext='baml',
                optional=True,
            ),
        ],
        output=('text',),
    ),
]


@utila.saveme
def main():
    utila.featurepack(
        root=rawmaker.ROOT,
        workplan=WORKPLAN,
        featurepackage='rawmaker.cleanup.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=False,
            name=PROCESS,
            pages=True,
            version=rawmaker.__version__,
        ),
    )
