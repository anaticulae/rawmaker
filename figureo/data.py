# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import itertools
import os
import typing

import PIL
import utila
import yaml


@dataclasses.dataclass
class Figure:

    data: PIL.Image = None
    bounding: tuple = None
    page: int = None
    index: int = None


Figures = typing.List[Figure]

EXT = 'png'


def dump_figures(figures: Figures, path: str):
    """Group list of figures by page number and write `raw figure` and
    `figure information` to `path`."""
    assert os.path.exists(path), str(path)

    for page, values in itertools.groupby(figures, key=lambda item: item.page):
        for index, figure in enumerate(values):
            write_image_raw(figure.data, path, page, index)
            write_image_info(figure.bounding, path, page, index)


def load_figures(path: str, skip_raw: bool = True):
    assert os.path.exists(path)
    files = utila.file_list(path, include='yaml')
    files = utila.files_sort(files)  # pylint:disable=R0204
    result = []
    for item in files:
        figure = _load_figure(item)
        name = filename(figure.page, figure.index, EXT)
        if not skip_raw:
            raw_path = os.path.join(path, name)
            raw = _load_image_raw(raw_path)
            figure.data = raw
        result.append(figure)
    return result


def write_image_raw(data: PIL.Image, path: str, page: int, index: int):
    name = filename(page, index, ext=EXT)
    outpath = os.path.join(path, name)
    with open(outpath, mode='wb') as output:
        data.save(output)


def write_image_info(bounding, path: str, page: int, index: int):
    name = filename(page, index, ext='yaml')
    raw = {
        'page': page,
        'bounding': '%s %s %s %s' % bounding,
        'index': index,
    }
    dumped = yaml.dump(raw)
    outpath = os.path.join(path, name)
    utila.file_create(outpath, dumped)


def _load_figure(path: str) -> Figure:
    content = utila.from_raw_or_path(path, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)

    page = int(loaded['page'])
    bounding = utila.parse_tuple(loaded['bounding'])
    index = int(loaded['index'])
    return Figure(page=page, index=index, bounding=bounding)


def _load_image_raw(path: str) -> PIL.Image:
    try:
        image = PIL.Image.open(path)
        image.load()
        return image
    except OSError as err:
        utila.error(err)
        return None


def filename(page, index, ext):
    page = f'{page}'.zfill(3)
    index = f'{index}'.zfill(2)
    return f'{page}_{index}.{ext}'
