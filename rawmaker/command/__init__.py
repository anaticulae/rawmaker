#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""The `rawmaker` takes pdf's from the input folder an parse the raw structure
of the pdf and provide them as yaml file for further analysation-processes.

- toc:    tableofcontent
- text:   text content from pdf file
- border: determine page size and bounding boxes from page content

"""
from dataclasses import dataclass
from glob import glob
from multiprocessing import Process
from os import makedirs
from os.path import isfile
from os.path import join

from pdfminer.pdfdocument import PDFDocument
from utila import FAILURE
from utila import SUCCESS
from utila import Parameter
from utila import Pattern
from utila import Value
from utila import create_step
from utila import featurepack
from utila import file_replace
from utila import logging
from utila import logging_error
from utila import logging_stacktrace
from utila import parse
from utila import saveme
from utila import sources

from rawmaker import PROCESS_NAME
from rawmaker import ROOT
from rawmaker import __version__
from rawmaker.features import commandline
from rawmaker.features import find_features
from rawmaker.features.annotation import work as annotation_work
from rawmaker.reader import read

PDF = Pattern('*', 'pdf')
CHAR_MARGIN = Value('char_margin', float, defaultvar=0.11, minimum=0.1)

WORKPLAN = [
    create_step(
        'annotation',
        inputs=[PDF],
        output=('annotation',),
    ),
    create_step(
        'border',
        inputs=[PDF],
        output=(
            'pages',
            'boundingboxes',
        ),
    ),
    create_step(
        'boxes',
        inputs=[PDF],
        output=(
            'boxes',
            'horizontal',
        ),
    ),
    create_step(
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
    create_step(
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
    create_step(
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
