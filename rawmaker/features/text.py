#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Extract text out of pdf document to gather information"""

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


def work(document: PDFDocument) -> str:
    """Extract structured text out of document

    Args:
        document: pdf-document to run parsing
    Returns:
        parsed document as yaml output
        parsed positions of text container
    """
    document = extract_content(document)
    positions = hash_positions(document)

    return {
        'text': dump_document(document),
        'positions': dump_hasher(positions),
    }


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
