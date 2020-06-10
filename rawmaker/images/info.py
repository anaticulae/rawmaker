# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import functools
import typing

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


ImageInformations = typing.List[ImageInformation]


def imageinfo(path: str, page: int, bounding: tuple) -> ImageInformation:
    assert isinstance(bounding, (iamraw.BoundingBox, tuple)), type(bounding)
    try:
        image = PIL.Image.open(path)
        image.load()
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
    assert isinstance(info, ImageInformation)
    result = {}
    if info.height is not None:
        result['height'] = info.height
    if info.width is not None:
        result['width'] = info.width
    if info.page is not None:
        result['page'] = info.page
    if info.bounding:
        result['bounding'] = utila.from_tuple(info.bounding)
    if info.dpi:
        result['dpi'] = utila.from_tuple(info.dpi)
    dumped = yaml.safe_dump(result)
    return dumped


def load_info(content: str) -> ImageInformation:
    source = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.safe_load(source)
    parsed = ImageInformation()
    loader = [
        ('page', int),
        ('width', float),
        ('height', float),
        ('dpi', functools.partial(utila.parse_tuple, length=2)),
        ('bounding', functools.partial(utila.parse_tuple, length=4)),
    ]
    for key, typ in loader:
        try:
            value = typ(loaded[key])
        except KeyError:
            continue
        setattr(parsed, key, value)
    return parsed
