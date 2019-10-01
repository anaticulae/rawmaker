# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
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
import os

import rawmaker.miner.images
import rawmaker.reader


def work(document: str, writeimages: str, pages=None):
    # experimental feature, not active yet
    return
    with rawmaker.reader.read(document) as loaded:
        result = rawmaker.miner.images.extract_images(loaded, pages=pages)

    for pagenumber, page in result.items():
        for imagenumber, image in enumerate(page):
            raw, ext = rawmaker.miner.images.raw_image(loaded, image)
            filename = f'page{pagenumber}_{imagenumber}'
            fileoutpath = os.path.join(writeimages, filename)
            with open(f'{fileoutpath}.{ext}', mode='wb') as output:
                output.write(raw)
    # TODO: Return list with image information, size, resolution...


def extract_pages(document: str, pages=None):
    with rawmaker.reader.read(document) as loaded:
        result = rawmaker.miner.images.extract_images(loaded, pages=pages)

    result = dict(result)
    for page, content in result.items():
        result[page] = rawmaker.miner.images.merge_images(
            content,
            loaded,
        )

    return result
