# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import PIL.Image
import utila

DEFAULT_DPI = (96, 96)


def imageinfo(path: str, page: int, bounding: tuple) -> iamraw.ImageInformation:
    assert isinstance(bounding, (iamraw.BoundingBox, tuple)), type(bounding)
    try:
        image = PIL.Image.open(path)
        image.load()
    except OSError as err:
        utila.error(err)
        return None
    width, height = image.size
    # add default DPI to distinguish images and figures
    dpi = image.info.get('dpi', DEFAULT_DPI)
    result = iamraw.ImageInformation(
        width=width,
        height=height,
        dpi=dpi,
        page=page,
        bounding=bounding,
    )
    return result
