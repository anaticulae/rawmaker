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
from utila import create_step
from utila import featurepack

from rawmaker import PROCESS_NAME
from rawmaker import ROOT
from rawmaker import __version__

PDF = Pattern('*', 'pdf')
CHAR_MARGIN = Value('char_margin', float, defaultvar=5.0, minimum=0.1)
step = create_step  #pylint:disable=C0103

WORKPLAN = [
    step(
        'annotation',
        inputs=[PDF],
        output=('annotation',),
    ),
    step(
        'border',
        inputs=[PDF],
        output=(
            'pages',
            'boundingboxes',
        ),
    ),
    step(
        'boxes',
        inputs=[PDF],
        output=(
            'boxes',
            'horizontal',
        ),
    ),
    step(
        'fonts',
        inputs=[
            PDF,
            CHAR_MARGIN,
        ],
        output=(
            'header',
            'content',
        ),
    ),
    step(
        'text',
        inputs=[
            PDF,
            CHAR_MARGIN,
        ],
        output=(
            'text',
            'positions',
        ),
    ),
    step(
        'toc',
        inputs=[
            PDF,
        ],
        output=('toc',),
    ),
]

RAWMAKER_DESCRIPTION = """
Extract features from pdf document.
"""


def main():
    result = featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='rawmaker.features',
        name=PROCESS_NAME,
        description=RAWMAKER_DESCRIPTION,
        version=__version__,
        singleinput=True,
    )
    return result
