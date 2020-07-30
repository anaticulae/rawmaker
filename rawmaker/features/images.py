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

import serializeraw
import utila

import rawmaker
import rawmaker.images.info
import rawmaker.miner.images
import rawmaker.reader

PageContentImages = collections.namedtuple('PageContentImages', 'content, page')
PageContentImagesList = typing.List[PageContentImages]

DumpedImageInformations = typing.List[typing.Tuple[str, bytes]]


def work(document: str, pages: tuple = None) -> DumpedImageInformations:
    extracted = extract_pages(document, pages=pages)
    result = []
    for page in extracted:
        for info, (rawimage, ext) in page.content:
            info = serializeraw.dump_image_info(info)
            result.append((info, (rawimage, ext)))
    return result


def extract_pages(
        document: str,
        outputfolder: str = None,
        pages=None,
) -> PageContentImagesList:
    # TODO: REPLACE AFTER UPGRADING UTILA
    if outputfolder is None:
        outputfolder = utila.tmpfile(rawmaker.ROOT)

    with rawmaker.reader.read(document) as loaded:
        extracted = rawmaker.miner.images.extract_images(
            loaded,
            outputfolder=outputfolder,
            pages=pages,
        )
    result = []
    for page, images in extracted.items():
        pagecontent = []
        for parsed in images:
            bounding = parsed.bounding
            path = os.path.join(outputfolder, parsed.filename)
            if not os.path.exists(path):
                # TODO: FIX IMAGE EXTRACTION
                utila.error(f'missing image: {path}')
                continue
            loaded = utila.file_read_binary(path)
            info = rawmaker.images.info.imageinfo(path, page, bounding)
            ext = utila.file_ext(path)
            pagecontent.append((info, (loaded, ext)))
        if pagecontent:
            result.append(PageContentImages(page=page, content=pagecontent))
    return result
