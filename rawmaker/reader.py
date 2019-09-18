#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from contextlib import contextmanager
from os.path import exists
from os.path import isfile

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdocument import PDFSyntaxError
from pdfminer.pdfparser import PDFParser

from rawmaker.error import InvalidPDF
from rawmaker.error import PDFParserImplementationError
from rawmaker.error import TextExtractionNotAllowed


@contextmanager
def read(path: str, password: str = '') -> PDFDocument:
    """Read pdf from files

    Args:
        path(str): path to pdf-file
        password(str): optional password to extract encrypted data
    Raises:
        TextExtractNotAllowed if not extraction is allowed"""
    if not exists(path):
        raise FileNotFoundError('Path does not exists %s' % path)
    if not isfile(path):
        raise ValueError('Read requires an pdf document, not %s' % path)

    with open(path, 'rb') as fp:
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)
        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        document = open_document(parser, path, password)

        # Check if the document allows text extraction. If not, abort.
        # TODO: SHOULD WE RESPECT THIS FLAG?
        # if not document.is_extractable:
        #     raise TextExtractionNotAllowed(path)

        yield document


def open_document(parser: PDFParser, path: str, password: str) -> PDFDocument:
    """
    Hint:
        Using fallback as default mode is very slow. Therefore we try
        without fallback and if this does not work, we try it with
        fallback again.
        Try first without using fallback because this is much faster on
        valid documents. If the run without fallback fails, start it
        with fallback again.
    """
    try:
        document = PDFDocument(parser, password, fallback=False)
    except PDFSyntaxError:
        pass  # try with fallback again
    except Exception as exc:
        raise PDFParserImplementationError(path) from exc
    else:
        return document

    try:
        document = PDFDocument(parser, password, fallback=True)
    except PDFSyntaxError as exc:
        raise InvalidPDF(path) from exc
    except Exception as exc:
        raise PDFParserImplementationError(path) from exc
    else:
        return document
