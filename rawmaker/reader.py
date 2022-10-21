#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import sys
from contextlib import contextmanager
from os.path import exists
from os.path import isfile

import utila
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdocument import PDFEncryptionError
from pdfminer.pdfdocument import PDFSyntaxError
from pdfminer.pdfparser import PDFParser

# from rawmaker.error import InvalidPDF
# from rawmaker.error import PDFParserImplementationError


@contextmanager
def read(path: str, password: str = None, verify: bool = True) -> PDFDocument:
    """Open pdf from `path`.

    Args:
        path(str): path to pdf-file
        password(str): optional password to extract encrypted data
        verify(bool): ensure that file starts with `%PDF-`
    Raises:
        TextExtractNotAllowed: if no extraction is allowed - currently disabled
        FileNotFoundError: `path` does not exists
        ValueError: `path` is not a file
    Yields:
        PDFDocument: open pdf file
    """
    if not exists(path):
        raise FileNotFoundError(f'Path does not exists: {path}')
    if not isfile(path):
        raise ValueError(f'Read requires an pdf document, not {path}')
    if verify:
        header = open(path, 'rb').read(5)
        if header != b'%PDF-':
            # TODO: MOVE TO def before() method after upgrading utila
            utila.error('invalid pdf header')
            sys.exit(1)
    with open(path, 'rb') as fp:
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)
        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        document = open_document(parser, password)
        yield document


def open_document(parser: PDFParser, password: str) -> PDFDocument:
    """Open pdf document base on selected `parser`.

    Hint:
        Using fallback as default mode is very slow. Therefore we try
        without fallback and if this does not work, we try it with
        fallback again.
        Try first without using fallback because this is much faster on
        valid documents. If the run without fallback fails, start it
        with fallback again.
    """
    password = password if password is not None else ''
    try:
        document = PDFDocument(parser, password, fallback=False)
    except PDFSyntaxError:
        pass  # try with fallback again
    except PDFEncryptionError as encryption:
        utila.error('encryption not supported')
        utila.debug(encryption)
        sys.exit(1)
    except Exception:  # pylint:disable=broad-except
        utila.print_stacktrace()
        sys.exit(2)
        # raise PDFParserImplementationError(path) from exc
    else:
        return document

    try:
        utila.info('try to use `fallback` pdf loader')
        document = PDFDocument(parser, password, fallback=True)
    except PDFSyntaxError:
        utila.print_stacktrace()
        sys.exit(3)
        # raise InvalidPDF(path) from exc
    except Exception:  # pylint:disable=broad-except
        # raise PDFParserImplementationError(path) from exc
        utila.print_stacktrace()
        sys.exit(2)
    return document
