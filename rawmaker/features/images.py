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
import dataclasses
import os
import typing

import PIL.Image
import utila
import yaml

import rawmaker
import rawmaker.miner.images
import rawmaker.reader

PageContentImages = collections.namedtuple('PageContentImages', 'content, page')
PageContentImagesList = typing.List[PageContentImages]

ImageInformations = typing.List[typing.Tuple[str, bytes]]


def work(
        document: str,
        pages: tuple = None,
        # ) -> typing.List[typing.Tuple[str, bytes]]:
) -> ImageInformations:
    extracted = extract_pages(document, pages=pages)
    result = []
    for page in extracted:
        for info, rawimage in page.content:
            info = dump_info(info)
            result.append((info, rawimage))
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
        for image in images:
            path = os.path.join(outputfolder, image)
            loaded = utila.file_read_binary(path)
            info = imageinfo(path, page)
            pagecontent.append((info, loaded))
        if pagecontent:
            result.append(PageContentImages(page=page, content=pagecontent))
    return result


@dataclasses.dataclass
class ImageInformation:
    width: int = None
    height: int = None
    page: int = None
    dpi: tuple = None
    bounding: tuple = None


def imageinfo(path: str, page: int):
    try:
        image = PIL.Image.open(path)
        image.load()
        # result.append(image)
    except OSError as err:
        utila.error(err)
        return None
    width, height = image.size
    dpi = image.info.get('dpi', None)

    result = ImageInformation(
        width=width,
        height=height,
        dpi=dpi,
        page=page,
    )
    return result


def dump_info(info: ImageInformation) -> str:
    result = {}
    for key, value in vars(info).items():
        if value is None:
            continue
        result[key] = value
    dumped = yaml.dump(result)
    return dumped
