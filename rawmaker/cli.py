#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
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

import protocol
import utila

import rawmaker
import rawmaker.error
import rawmaker.features

PDF = utila.Pattern('*', 'pdf')

CHAR_MARGIN = utila.Value('char_margin', float, defaultvar=2.0, minimum=0.1)
LINE_OVERLAP = utila.Value('line_overlap', float, defaultvar=0.5, minimum=0.1)
LINE_MARGIN = utila.Value('line_margin', float, defaultvar=0.5, minimum=0.1)
WORD_MARGIN = utila.Value('word_margin', float, defaultvar=0.1, minimum=0.1)
BOXES_FLOW = utila.Value('boxes_flow', float, defaultvar=0.5, minimum=0.1)
NOSTRIP = utila.Bool('nostrip')
DETECT_VERTICAL = utila.Bool('detect_vertical')

PDF_INPUT = [PDF]

CONFIG_INPUTS = [
    PDF,
    BOXES_FLOW,
    CHAR_MARGIN,
    LINE_MARGIN,
    LINE_OVERLAP,
    WORD_MARGIN,
    NOSTRIP,
    DETECT_VERTICAL,
]

WORKPLAN = [
    utila.create_step(
        'annotation',
        inputs=PDF_INPUT,
        output=('annotation',),
    ),
    utila.create_step(
        'border',
        inputs=PDF_INPUT,
        output=(
            'pages',
            'boundingboxes',
        ),
    ),
    utila.create_step(
        'boxes',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='line_line'),
        ],
        output=('boxes',),
    ),
    utila.create_step(
        'figures',
        inputs=PDF_INPUT + [
            utila.ResultFile(producer='rawmaker', name='boxes_boxes'),
            utila.Pattern('rawmaker__images_images/*', 'yaml'),
        ],
        output=[
            ('figures/{FILEHASH_1}', 'yaml'),
            ('figures/{FILEHASHS}', 'png'),
        ],
    ),
    utila.create_step(
        'horizontals',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='line_line'),
        ],
        output=('horizontals',),
    ),
    utila.create_step(
        'fonts',
        inputs=CONFIG_INPUTS,
        output=(
            'header',
            'content',
        ),
    ),
    utila.create_step(
        'formula',
        inputs=PDF_INPUT,
        output=('formula',),
    ),
    utila.create_step(
        'images',
        inputs=PDF_INPUT,
        output=[
            ('images/{FILEHASH_1}', 'yaml'),
            ('images/{FILEHASHS}', '???'),
        ],
    ),
    utila.create_step(
        'line',
        inputs=[
            PDF,
            utila.ResultFile(producer='rawmaker', name='annotation_annotation'),
        ],
        output=('line',),
    ),
    utila.create_step(
        'text',
        inputs=CONFIG_INPUTS,
        output=(
            'text',
            'positions',
        ),
    ),
    utila.create_step(
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
    config = utila.FeaturePackConfig(
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
        utila.featurepack(
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
    solver = protocol.Solver()
    for msg, solution in protocol.solution.SOLUTION.items():
        solver.add_solution(msg, solution)

    active = [protocol.MessageStatus(msgid='F0000', active=True)]

    # init linter
    errorhook.linter = protocol.Linter(solver=solver, active=active)

    try:
        yield
    except SystemExit as exc:
        if f'--{LINTER_FLAG}' in sys.argv:
            errorhook.linter.write(root)
        raise exc
