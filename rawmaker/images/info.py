# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import iamraw
import PIL.Image
import utila
import yaml


@dataclasses.dataclass
class ImageInformation:
    width: int = None
    height: int = None
    page: int = None
    dpi: tuple = None
    bounding: tuple = None


def imageinfo(path: str, page: int, bounding: tuple) -> ImageInformation:
    assert isinstance(bounding, iamraw.BoundingBox), type(bounding)
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
        bounding=bounding,
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


def load_info(content: str) -> ImageInformation:
    source = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(source, Loader=yaml.FullLoader)
    parsed = ImageInformation()
    for key, value in loaded.items():
        setattr(parsed, key, value)
    return parsed
