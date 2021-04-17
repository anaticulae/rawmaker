# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdfminer.pdfpage
import utila


def parse_tuple(raw: str, length: int = 4, typ=float) -> tuple:
    """Convert `raw` to tuple of `typ`.

    >>> parse_tuple('True false True False true', length=5, typ=bool)
    (True, False, True, False, True)
    >>> parse_tuple('9.0', length=1, typ=int)
    (9,)
    """
    if typ is int:
        typ = utila.str2int
    if typ is bool:
        typ = utila.str2bool
    items = (typ(item) for item in raw.split())
    if typ is float:
        items = utila.math.roundme(*items, convert=False)
    items = tuple(items)
    assert len(items) == length, f'could not parse {raw}'
    return items


utila.parse_tuple = parse_tuple

before = pdfminer.pdfpage.PDFPage.create_pages  # pylint:disable=C0103


def create_pages(document):
    try:
        yield from before(document)
    except IndexError:
        utila.error('pdfminer parsing error: IndexError')
        exit(1)
    except RecursionError:
        utila.error('pdfminer parsing error: RecursionError')
        exit(1)


pdfminer.pdfpage.PDFPage.create_pages = create_pages
