#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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

PDF = utila.Pattern('*', 'pdf')

CHAR_MARGIN = utila.Value('char_margin', float, defaultvar=2.0, minimum=0.1)
LINE_OVERLAP = utila.Value('line_overlap', float, defaultvar=0.5, minimum=0.1)
LINE_MARGIN = utila.Value('line_margin', float, defaultvar=0.5, minimum=0.1)
WORD_MARGIN = utila.Value('word_margin', float, defaultvar=0.1, minimum=0.1)
BOXES_FLOW = utila.Value('boxes_flow', float, defaultvar=0.5, minimum=0.1)

PDF_INPUT = [PDF]

CONFIG_INPUTS = [
    PDF,
    BOXES_FLOW,
    CHAR_MARGIN,
    LINE_MARGIN,
    LINE_OVERLAP,
    WORD_MARGIN,
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
        inputs=PDF_INPUT,
        output=(
            'boxes',
            'horizontal',
        ),
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
        'text',
        inputs=CONFIG_INPUTS,
        output=(
            'text',
            'positions',
        ),
    ),
    utila.create_step(
        'toc',
        inputs=PDF_INPUT,
        output=('toc',),
    ),
]

RAWMAKER_DESCRIPTION = """
Extract features from pdf document.
"""

LINTER_FLAG = 'linter'


def main():
    flags = [
        (LINTER_FLAG, 'write linter result'),
    ]
    with linter():
        utila.featurepack(
            description=RAWMAKER_DESCRIPTION,
            errorhook=errorhook,
            featurepackage='rawmaker.features',
            flags=flags,
            multiprocessed=True,
            name=rawmaker.PROCESS_NAME,
            pages=True,
            root=rawmaker.ROOT,
            singleinput=True,
            version=rawmaker.__version__,
            workplan=WORKPLAN,
        )


def errorhook(exception, source):  # pylint:disable=W0613
    logger = errorhook.linter

    if isinstance(exception, rawmaker.error.InvalidPDF):
        logger.add_finding(msgid='F0000', confidence=1.0)


@contextlib.contextmanager
def linter():
    """Write result of linting when using `--linter` parameter.

    Args:
        write_result(bool): if active create developer.lin and user.lin
    """
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
