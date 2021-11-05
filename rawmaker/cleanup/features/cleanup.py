# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
    codes = rawmaker.cleanup.load.codes_frompath(inpaths, prefix, pages)
    # remove content here
    ptns, horizontals, lines = remove_skip_area(
        ptns,
        horizontals,
        lines,
        codes=codes,
        inpaths=inpaths,
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
        prefix=prefix,
        postfix=postfix,
    )


def remove_skip_area(
    ptns,
    horizontals,
    lines,
    codes,
    inpaths: list,
    pages: tuple = None,
):
    images, tables = rawmaker.cleanup.load.load_images_tables(
        inpaths,
        pages=pages,
    )
    invalids = create_invalid_area(images, tables, codes)

    def valid_bounding(bounding, page: int) -> bool:
        try:
            invalid_area = invalids[page]
        except KeyError:
            return True
        if utila.rectangles_intersecting(invalid_area, bounding):
            return False
        return True

    for ptn in ptns:
        if ptn.page not in invalids:
            # no invalid possible
            continue
        # line intersects with invalid area
        invalid_lines = [
            item for item in ptn if not valid_bounding(item.bounding, ptn.page)
        ]
        for line in invalid_lines:
            ptn.remove(line)
    if horizontals:
        horizontals = [
            iamraw.PageContentHorizontals(
                page=page.page,
                content=[
                    item
                    for item in page.content
                    if valid_bounding(item.box, page.page)
                ])
            for page in horizontals
        ]
    if lines:
        lines = [
            iamraw.PageContentLine(
                page=page.page,
                content=[
                    item
                    for item in page.content
                    if valid_bounding(item, page.page)
                ],
            )
            for page in lines
        ]
    return ptns, horizontals, lines


def create_invalid_area(images, tables, codes) -> dict:
    invalid = collections.defaultdict(list)
    for page in images:
        invalid[page.page].extend([item.bounding for item in page.content])
    for page in tables:
        invalid[page.page].extend([item.bounding for item in page.content])
    for page in codes:
        tokens = utila.flatten([it.tokens_bounding for it in page.content])
        invalid[page.page].extend(tokens)
        caption = utila.flatten([it.caption_bounding for it in page.content])
        invalid[page.page].extend(caption)
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
