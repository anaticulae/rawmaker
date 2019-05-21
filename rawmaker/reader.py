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

    with open(path, 'rb') as fp:
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)
        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        try:
            document = PDFDocument(parser, password)
        except PDFSyntaxError:
            raise InvalidPDF(path)
        except Exception:
            raise PDFParserImplementationError(path)

        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise TextExtractionNotAllowed(path)

        yield document
