# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import serializeraw
import utila


def ptn_frompath(inpaths, prefix, pages):
    for inpath in inpaths:
        utila.debug(f'ptn: {inpath}')
        ptns = serializeraw.ptn_frompath(
            inpath,
            prefix=prefix,
            pages=pages,
            sort=False,
        )
        if ptns:
            return ptns
    return None


def codes_frompath(inpaths, prefix, pages):  # pylint:disable=W0613
    result = []
    for inpath in inpaths:
        utila.debug(f'ptn: {inpath}')
        path = iamraw.path.codero_result(inpath)
        if os.path.exists(path):
            loaded = serializeraw.load_codes(path, pages=pages)
            result.extend(loaded)
    return result


def lines_frompath(inpaths: list, prefix: str, pages: tuple) -> tuple:
    """\
    Args:
        inpaths(list): list of possible sources
        prefix(str): prefix inpath data
        pages(tuple): selected pages
    Returns:
        Filtered horizontals and lines

    Hint: It is only required to write the result file if the source
    file exists. We have to destingush between non existing, empty
    source file and empty remove source file.
    It is enough to have two groups, we only want to know if we must
    write the empty file.
    """
    prefix = ''  # DISABLE PREFIX
    horizontals, lines = None, None
    for inpath in inpaths:
        utila.debug(f'lines: {inpath}')
        if utila.exists(iamraw.path.horizontals(inpath)):
            # if utila.exists(iamraw.path.horizontals(inpath, prefix)):
            # use list, to signal that line source file exists.
            horizontals = horizontals or []
            horizontals.extend(
                serializeraw.load_horizontals(
                    inpath,
                    prefix=prefix,
                    pages=pages,
                ))
        if utila.exists(iamraw.path.line(inpath)):
            # if utila.exists(iamraw.path.line(inpath, prefix)):
            # use list, to signal that line source file exists.
            lines = lines or []
            lines.extend(
                serializeraw.load_lines(
                    inpath,
                    prefix=prefix,
                    pages=pages,
                ))
    return horizontals, lines


def fontstore_frompath(inpaths, prefix, pages):
    for inpath in inpaths:
        utila.debug(f'fontstore: {inpath}')
        fontstore = serializeraw.create_fontstore_frompath(
            inpath,
            prefix=prefix,
            pages=pages,
        )
        if fontstore:
            return fontstore
    return None


def load_images_tables(inpaths: list, pages: tuple = None):
    images, tables = [], []
    # load images and tables from multiple `inpaths`
    for inpath in inpaths:
        imagepath = os.path.join(inpath, 'rawmaker__images_images')
        if utila.exists(imagepath):
            images.extend(
                serializeraw.load_image_infos_frompath(
                    imagepath,
                    pages=pages,
                ))
        tableropath = iamraw.path.tablero_result(inpath)
        utila.debug(f'tablero: {tableropath}')
        if utila.exists(tableropath):
            tables.extend(serializeraw.load_tables(tableropath, pages=pages))
    return images, tables
