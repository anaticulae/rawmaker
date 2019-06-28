#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Extract text out of pdf document to gather information"""

from typing import Tuple

from iamraw import Document
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from serializeraw import dump_document
from utila import Flag

from rawmaker.miner.mining import IAmRawConverter
from rawmaker.miner.position import dump_hasher
from rawmaker.miner.position import hash_positions
from rawmaker.parameter import create_layout
from rawmaker.parameter import print_layout
from rawmaker.reader import read


def work(
        document: str,
        boxes_flow: float = 0.5,
        char_margin: float = 2.0,
        line_margin: float = 0.5,
        line_overlap: float = 0.5,
        word_margin: float = 0.1,
) -> Tuple[str, str]:
    """Extract structured text out of document

    Args:
        document: pdf-document to run parsing
        char_margin(float): XXX Why 5.0?
    Returns:
        parsed document as yaml output
        parsed positions of text container
    """
    layout = create_layout(
        boxes_flow=boxes_flow,
        char_margin=char_margin,
        line_margin=line_margin,
        line_overlap=line_overlap,
        word_margin=word_margin,
    )
    print_layout(layout)
    # Diff between chars which build a word

    assert isinstance(document, str), str(document)
    with read(document) as pdf:
        document = extract_content(pdf, layout_parameter=layout)

    positions = hash_positions(document)

    dumped_text = dump_document(document)
    dumped_positions = dump_hasher(positions)

    return dumped_text, dumped_positions


def extract_content(
        document: PDFDocument,
        layout_parameter: LAParams = None,
) -> Document:
    """Extract content from PDF file

    Args:
        document(PDFDocument): PDF file to work on
        layout_parameter(LAParams): Parameterization for layout analysis. This
                                    parameter defines how chars are matched
                                    together in words and sentences.
    Returns:
        Document: parsed and layouted document
    """
    if layout_parameter is None:
        layout_parameter = LAParams()
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    device = IAmRawConverter(rsrcmgr, laparams=layout_parameter)
    device.new_document()
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Processing layout
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
    document = device.finish_document()
    return document


def commandline():
    return Flag(longcut=name(), message='Extract text of document.')


def name():
    return 'text'
