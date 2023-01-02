# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import pdfinfo
import serializeraw
import utila

import rawmaker.parameter


def superfast(
    document: str,
    config: rawmaker.parameter.ParsingConfiguration,
    workdir: str,
    pages: list = None,
) -> iamraw.Document:
    if pages is None:
        pagecount = pdfinfo.pagecount(document)
        pages = utila.make_tuple(pagecount)
    chunks = utila.chunks(pages, size=10)
    parameter = config.cmdline()
    todo = []
    for index, chunk in enumerate(chunks):
        joined_pages = utila.from_tuple(chunk, separator=',')
        cmd = (f'rawmaker -i {document} -o {workdir} --prefix {index}'
               f' --text --pages {joined_pages} {parameter}')
        utila.log(cmd)
        todo.append(cmd)
    # run in parallel
    completed = utila.run_parallel(todo, workdir, worker=12)
    assert completed == utila.SUCCESS, completed
    # merge document
    document = merge_document(workdir, len(chunks))
    return document


def merge_document(path: str, size: int) -> iamraw.Document:
    """Merge chunks of extract document.

    A little bit diry, but ok for now. XXX
    """
    text_files = [
        os.path.join(path, f'rawmaker__{item}_text_text.yaml')
        for item in range(size)
    ]
    posi_files = [
        os.path.join(path, f'rawmaker__{item}_text_positions.yaml')
        for item in range(size)
    ]

    text = [serializeraw.load_document(item) for item in text_files]
    positions = [serializeraw.load_textpositions(item) for item in posi_files]

    for item in text_files + posi_files:
        utila.info(f'remove {item}')
        utila.file_remove(item)

    for docs, pos in zip(text, positions):
        for page in docs:
            index = 0
            for item in page:
                if not isinstance(item, iamraw.TextContainer):
                    continue
                # bounding, mean
                bounding, mean = utila.select_page(pos, page.page).content[index] # yapf:disable
                fake_text_mean_height(item, bounding, mean)
                item.box = bounding
                index += 1

    document = iamraw.Document(dimension=text[0].dimension)
    for chunk in text:
        for page in chunk:
            document.append(page)
    return document


def fake_text_mean_height(item, bounding, mean):
    # TODO: REMOVE THIS HACK LATER
    for line in item.lines:
        for char in line:
            # Fake mean char height
            char.box = iamraw.BoundingBox(0, bounding.y1 - mean, 0, bounding.y1)
