# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import os

import iamraw
import serializeraw
import utila

import rawmaker.cleanup.dump
import rawmaker.cleanup.load


def work(
    postfix: str,
    inputs: str,
    outputs: str,
    prefix: str = '',
    pages: tuple = None,
):
    # POSTFIX as value first!
    cleanup(
        inputs,
        outputs,
        prefix,
        postfix,
        pages=pages,
    )
    return utila.NO_RESULT


def cleanup(  # pylint:disable=R0914
    inpaths: list,
    outpath: str,
    prefix: str = '',
    postfix: str = '',
    pages=None,
):
    if not inpaths:
        inpaths = [os.getcwd()]
    if not outpath:
        outpath = inpaths[0]
    ptns = rawmaker.cleanup.load.ptn_frompath(inpaths, prefix, pages)
    horizontals, lines = rawmaker.cleanup.load.lines_frompath(
        inpaths,
        prefix,
        pages,
    )
    # remove content here
    ptns, horizontals, lines, images = remove_skip_area(
        ptns,
        horizontals,
        lines,
        inpaths=inpaths,
        prefix=prefix,
        pages=pages,
    )
    fontstore = rawmaker.cleanup.load.fontstore_frompath(inpaths, prefix, pages)
    document, textpositions, fontheader, fontcontent = rawmaker.cleanup.dump.dump_ptn(
        ptns,
        fontstore,
    )
    write_result(
        outpath,
        document,
        textpositions,
        fontheader,
        fontcontent,
        horizontals,
        lines,
        images=images,
        prefix=prefix,
        postfix=postfix,
    )


def remove_skip_area(
    ptns,
    horizontals,
    lines,
    inpaths: list,
    prefix,
    pages: tuple = None,
):
    codes = rawmaker.cleanup.load.codes_frompath(inpaths, prefix, pages)
    formulas = rawmaker.cleanup.load.formulas_frompath(inpaths, prefix, pages)
    captions = rawmaker.cleanup.load.captions_frompath(inpaths, prefix, pages)
    images, tables = rawmaker.cleanup.load.load_images_tables(
        inpaths,
        pages=pages,
    )
    invalids = create_invalid_area(images, tables, codes, formulas, captions)
    ptns = cleanup_ptn(ptns, invalids)
    horizontals = cleanup_horizontals(horizontals, invalids)
    lines = cleanup_lines(lines, invalids)
    noimages = create_invalid_area(
        images=[],
        tables=tables,
        codes=codes,
        formulas=formulas,
        captions=captions,
    )
    images = cleanup_images(images, noimages)
    return ptns, horizontals, lines, images


def cleanup_ptn(ptns, invalids):
    for ptn in ptns:
        if ptn.page not in invalids:
            # no invalid possible
            continue
        # line intersects with invalid area
        invalid_lines = [
            item for item in ptn
            if not valid_bounding(item.bounding, invalids, ptn.page)
        ]
        for line in invalid_lines:
            line.hide()
    return ptns


def cleanup_horizontals(horizontals, invalids):
    if not horizontals:
        return horizontals
    horizontals = [
        iamraw.PageContentHorizontals(
            page=page.page,
            content=[
                item
                for item in page.content
                if valid_bounding(item.box, invalids, page.page)
            ])
        for page in horizontals
    ]
    return horizontals


def cleanup_lines(lines, invalids):
    if not lines:
        return lines
    lines = [
        iamraw.PageContentLine(
            page=page.page,
            content=[
                item
                for item in page.content
                if valid_bounding(item, invalids, page.page)
            ],
        )
        for page in lines
    ]
    return lines


def cleanup_images(images, invalids):
    """Skip images which are overlapped by table, formula, code or
    something else.

    We prefare these extraction over image extraction.
    """
    if not images:
        return images
    for page in images:
        for image in page.content:
            if valid_bounding(image.bounding, invalids, page.page):
                continue
            # image is overlapped by table, formula, code or something,
            # skip image
            image.hidden = True
    return images


def valid_bounding(bounding, invalids, page: int) -> bool:
    try:
        invalid_area = invalids[page]
    except KeyError:
        return True
    for invalid in invalid_area:
        overlapping_rate = utila.rectangle_overlapping(invalid, bounding)
        if overlapping_rate > 0.9:  # TODO: HOLY VALUE
            return False
    return True


def create_invalid_area(images, tables, codes, formulas, captions) -> dict:
    invalid = collections.defaultdict(list)
    for page in images:
        invalid[page.page].extend([item.bounding for item in page.content])
    for page in tables:
        invalid[page.page].extend([item.bounding for item in page.content])
    for page in codes:
        tokens = utila.flatten([item.tokens_bounding for item in page.content])
        invalid[page.page].extend(tokens)
        # caption = utila.flatten([it.caption_bounding for it in page.content])
        # invalid[page.page].extend(caption)
    for page in formulas:
        invalid[page.page].extend([item.bounding for item in page.content])
    for page in captions:
        invalid[page.page].extend([item.bounding for item in page.content])
    # reduce rectangle count
    result = {
        key: utila.rectangle_merge(value) for key, value in invalid.items()
    }
    return result


def write_result(
    outpath: str,
    document: iamraw.Document,
    textpositions: iamraw.TextPositions,
    fontheader: dict,
    fontcontent: list,
    horizontals: list,
    lines: list,
    images: list,
    prefix: str = '',
    postfix: str = '',
):
    prefix = prefix or ''
    postfix = postfix or ''
    # write document
    utila.file_replace(
        iamraw.path.text(outpath, prefix=prefix + postfix),
        document,
    )
    utila.file_replace(
        iamraw.path.textposition(outpath, prefix=prefix + postfix),
        textpositions,
    )
    # write reduced font store
    utila.file_replace(
        iamraw.path.fontheader(outpath, prefix=prefix + postfix),
        fontheader,
    )
    utila.file_replace(
        iamraw.path.fontcontent(outpath, prefix=prefix + postfix),
        fontcontent,
    )
    write_images(outpath, images)
    # write lines
    if horizontals is not None:
        # None signals that the source does not contain any horizontal file
        utila.file_replace(
            iamraw.path.horizontals(outpath, prefix=postfix),
            serializeraw.dump_horizontals(horizontals),
        )
    if lines is not None:
        # None signals that the source does not contain any line file
        utila.file_replace(
            iamraw.path.line(outpath, prefix=postfix),
            serializeraw.dump_lines(lines),
        )


def write_images(outpath, images):
    if not images:
        return
    # TODO: REMOVE ftype later
    baseimage = iamraw.path.images(outpath, ftype='')
    os.makedirs(baseimage, exist_ok=True)
    for page in images:
        for image in page.content:
            if not image.hidden:
                continue
            imagepath = utila.join(baseimage, f'{image.hashedimage}.yaml')
            dumped = serializeraw.dump_image_info(image)
            utila.file_replace(imagepath, dumped)
