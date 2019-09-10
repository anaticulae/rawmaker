#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
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

from utila import Pattern
from utila import Value
from utila import create_step as step
from utila import featurepack

from rawmaker import PROCESS_NAME
from rawmaker import ROOT
from rawmaker import __version__

PDF = Pattern('*', 'pdf')

CHAR_MARGIN = Value('char_margin', float, defaultvar=2.0, minimum=0.1)
LINE_OVERLAP = Value('line_overlap', float, defaultvar=0.5, minimum=0.1)
LINE_MARGIN = Value('line_margin', float, defaultvar=0.5, minimum=0.1)
WORD_MARGIN = Value('word_margin', float, defaultvar=0.1, minimum=0.1)
BOXES_FLOW = Value('boxes_flow', float, defaultvar=0.5, minimum=0.1)

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
    step(
        'annotation',
        inputs=PDF_INPUT,
        output=('annotation',),
    ),
    step(
        'border',
        inputs=PDF_INPUT,
        output=(
            'pages',
            'boundingboxes',
        ),
    ),
    step(
        'boxes',
        inputs=PDF_INPUT,
        output=(
            'boxes',
            'horizontal',
        ),
    ),
    step(
        'fonts',
        inputs=CONFIG_INPUTS,
        output=(
            'header',
            'content',
        ),
    ),
    step(
        'text',
        inputs=CONFIG_INPUTS,
        output=(
            'text',
            'positions',
        ),
    ),
    step(
        'toc',
        inputs=PDF_INPUT,
        output=('toc',),
    ),
]

RAWMAKER_DESCRIPTION = """
Extract features from pdf document.
"""


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='rawmaker.features',
        name=PROCESS_NAME,
        description=RAWMAKER_DESCRIPTION,
        version=__version__,
        multiprocessed=True,
        singleinput=True,
        pages=True,
    )
