# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""ImageExtractor

The ImageExtractor provides the possibility to extract all images out of
a pdf file.

Support formats:
    - png?
    - jpg?

"""

import collections
import os
import typing

import configo
import utila

import rawmaker
import rawmaker.miner.images
import rawmaker.reader

PageContentImages = collections.namedtuple('PageContentImages', 'content, page')
PageContentImagesList = typing.List[PageContentImages]


def work(document: str, pages: tuple = None) -> str:  # pylint:disable=W0613
    extracted = extract_pages(document, pages=None)
    return ''


def extract_pages(
        document: str,
        outputfolder: str = None,
        pages=None,
) -> PageContentImagesList:
    # TODO: REPLACE AFTER UPGRADING UTILA
    if outputfolder is None:
        outputfolder = utila.tmpfile(rawmaker.ROOT)
        os.makedirs(outputfolder)

    with rawmaker.reader.read(document) as loaded:
        result = rawmaker.miner.images.extract_images(
            loaded,
            outputfolder=outputfolder,
            pages=pages,
        )
    result = [
        PageContentImages(page=page, content=content)
        for page, content in result.items()
    ]
    return result
