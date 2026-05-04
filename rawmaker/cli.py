#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""The `rawmaker` takes pdf's from the input folder or direct file and parse
the raw structure of the pdf and provide them as yaml file for further
analyze-processes.

- toc:    tableofcontent
- text:   text content from pdf file
- border: determine page size and bounding boxes from page content

"""

import contextlib
import os
import sys

import protoerror
import utilo

import rawmaker
import rawmaker.error
import rawmaker.features

PDF = utilo.Pattern('*', 'pdf')

CHAR_MARGIN = utilo.Value('char_margin', float, defaultvar=2.0, minimum=0.1)
LINE_OVERLAP = utilo.Value('line_overlap', float, defaultvar=0.5, minimum=0.1)
LINE_MARGIN = utilo.Value('line_margin', float, defaultvar=0.5, minimum=0.1)
WORD_MARGIN = utilo.Value('word_margin', float, defaultvar=0.1, minimum=0.1)
BOXES_FLOW = utilo.Value('boxes_flow', float, defaultvar=0.5, minimum=0.1)
NOSTRIP = utilo.Bool('nostrip')
DETECT_VERTICAL = utilo.Bool('detect_vertical')

PDF_INPUT = [PDF]

CONFIG_INPUTS = [
    BOXES_FLOW,
    CHAR_MARGIN,
    LINE_MARGIN,
    LINE_OVERLAP,
    WORD_MARGIN,
    NOSTRIP,
    DETECT_VERTICAL,
]

WORKPLAN = [
    utilo.create_step(
        'annotation',
        inputs=PDF_INPUT,
        output=('annotation',),
    ),
    utilo.create_step(
        'border',
        inputs=PDF_INPUT,
        output=(
            'pages',
            'boundingboxes',
        ),
    ),
    utilo.create_step(
        'boxes',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='line_line'),
        ],
        output=('boxes',),
    ),
    utilo.create_step(
        'figures',
        inputs=PDF_INPUT + [
            utilo.ResultFile(producer='rawmaker', name='boxes_boxes'),
            utilo.Pattern('rawmaker__images_images/*', 'yaml'),
        ],
        output=[
            ('figures/{FILEHASH_1}', 'yaml'),
            ('figures/{FILEHASHS}', 'png'),
        ],
    ),
    utilo.create_step(
        'horizontals',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='line_line'),
        ],
        output=('horizontals',),
    ),
    utilo.create_step(
        'fonts',
        inputs=[PDF] + CONFIG_INPUTS,
        output=(
            'header',
            'content',
        ),
    ),
    utilo.create_step(
        'formula',
        inputs=PDF_INPUT,
        output=('formula',),
    ),
    utilo.create_step(
        'images',
        inputs=PDF_INPUT,
        output=[
            ('images/{FILEHASH_1}', 'yaml'),
            ('images/{FILEHASHS}', '???'),
        ],
    ),
    utilo.create_step(
        'line',
        inputs=[
            PDF,
            utilo.ResultFile(producer='rawmaker', name='annotation_annotation'),
        ],
        output=('line',),
    ),
    utilo.create_step(
        'text',
        inputs=[PDF] + [
            utilo.ResultFile(
                producer='rawmaker',
                name='horizontals_horizontals',
            ),
        ] + CONFIG_INPUTS,
        output=(
            'text',
            'positions',
        ),
    ),
    utilo.create_step(
        'outlines',
        inputs=PDF_INPUT,
        output=('outlines',),
    ),
]

RAWMAKER_DESCRIPTION = """
Extract features from pdf document.
"""

LINTER_FLAG = 'linter'
SUPERFAST_FLAG = 'sf'


def main():
    flags = [
        (LINTER_FLAG, 'write linter result'),
        (SUPERFAST_FLAG, 'use superfast to fork processes and merge results'),
    ]
    config = utilo.FeaturePackConfig(
        configflag=True,
        description=RAWMAKER_DESCRIPTION,
        errorhook=errorhook,
        flags=flags,
        multiprocessed=True,
        name=rawmaker.PROCESS,
        pages=True,
        profileflag=True,
        singleinput=True,
        verboseflag=True,
        version=rawmaker.__version__,
    )
    with linter():
        utilo.featurepack(
            workplan=WORKPLAN,
            config=config,
            root=rawmaker.ROOT,
            featurepackage='rawmaker.features',
        )


def errorhook(exception, source):  # pylint:disable=W0613
    logger = errorhook.linter

    if isinstance(exception, rawmaker.error.InvalidPDF):
        logger.add_finding(msgid='F0000', confidence=1.0)


def superfast() -> bool:
    return '--sf' in sys.argv


@contextlib.contextmanager
def linter():
    """Write result of linting when using `--linter` parameter."""
    # path to write error report
    root = str(os.getcwd())
    # setup linter
    solver = protoerror.Solver()
    for msg, solution in protoerror.solution.SOLUTION.items():
        solver.add_solution(msg, solution)

    active = [protoerror.MessageStatus(msgid='F0000', active=True)]

    # init linter
    errorhook.linter = protoerror.Linter(solver=solver, active=active)

    try:
        yield
    except SystemExit as exc:
        if f'--{LINTER_FLAG}' in sys.argv:
            errorhook.linter.write(root)
        raise exc
