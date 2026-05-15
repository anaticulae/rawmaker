# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
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
import io
import os

import PIL.Image
import serializeraw
import ughost
import utilo

import rawmaker
import rawmaker.images.info
import rawmaker.miner.images
import rawmaker.reader

PageContentImages = collections.namedtuple('PageContentImages', 'content, page')
PageContentImagesList = list[PageContentImages]

DumpedImageInformations = list[tuple[str, bytes]]


def work(document: str, pages: tuple = None) -> DumpedImageInformations:
    extracted = extract_images(document, pages=pages)
    extracted = beautify_images(extracted, document)
    result = []
    for page in extracted:
        for info, (rawimage, ext) in page.content:
            info = serializeraw.dump_image_info(info)
            result.append((info, (rawimage, ext)))
    return result


def extract_images(
    document: str,
    outputfolder: str = None,
    pages=None,
) -> PageContentImagesList:
    # TODO: REPLACE AFTER UPGRADING utilo
    if outputfolder is None:
        outputfolder = utilo.tmpfile(rawmaker.ROOT)
    with rawmaker.reader.read(document) as loaded:
        extracted = rawmaker.miner.images.extract_images(
            loaded,
            outputfolder=outputfolder,
            pages=pages,
        )
    result = convert_images(
        extracted,
        outputfolder,
        pages=pages,
    )
    return result


def convert_images(
    extracted: dict,
    outputfolder: str,
    pages: tuple = None,
) -> list:
    result = []
    for page, images in extracted.items():
        # convert selected pages to global pages
        page = convert_pages(page, pages)
        pagecontent = []
        for parsed in images:
            bounding = parsed.bounding
            path = os.path.join(outputfolder, parsed.filename)
            if not os.path.exists(path):
                # TODO: FIX IMAGE EXTRACTION
                utilo.error(f'missing image: {path}')
                continue
            loaded = utilo.file_read_binary(path)
            info = rawmaker.images.info.imageinfo(path, page, bounding)
            if info is None:
                utilo.error(f'could not extract {path}, {page}, {bounding}')
                continue
            ext = utilo.file_ext(path)
            pagecontent.append((info, (loaded, ext)))
        if not pagecontent:
            continue
        result.append(PageContentImages(page=page, content=pagecontent))
    return result


def beautify_images(images, path: str):
    """Use ghost to render pdf and crop image area."""
    result = []
    for page in images:
        boundings = [item[0] for item in page.content]
        extracted = run_ghost(path, boundings)
        content = []
        for raw, bounding in zip(extracted, boundings):
            content.append((bounding, (raw, 'png')))
        result.append(PageContentImages(content=content, page=page.page))
    return result


def run_ghost(path: str, boundings: list) -> list:
    """Extract images out of pdf.

    If ghost is not installed, we return a empty white image.
    """
    if ughost.HAS_GHOST:
        extracted = ughost.images(path, boundings)
        return extracted
    utilo.error('could not beautify images: install ghost')
    result = []
    for bounding in boundings:
        size = (int(bounding.width), int(bounding.height))
        # white image backup bock box
        raw = PIL.Image.new('RGB', size, color=1)
        png = convert_topng(raw)
        result.append(png)
    return result


def convert_topng(image) -> bytes:
    raw = io.BytesIO()
    image.save(raw, format='png')
    # rewind the buffer
    raw.seek(0)
    # convert to bytes
    result = raw.getvalue()
    return result


def convert_pages(page: int, pages: tuple) -> int:
    """Pdfminer produces directly ascending pages.

    If we select pages=('0:5,28') pdfminer produces 0, 1, 2, 3, 4, 5.
    This method convert this to 0, 1, 2, 3, 4, 28.
    """
    # TODO: INVESTIGATE HERE
    if pages is None:
        return page
    # starting with starting offset
    offset = min(pages, default=0)
    return pages[page - offset]
