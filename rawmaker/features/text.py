#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Extract text out of pdf document to gather information."""

import os
import typing

import iamraw
import serializeraw
import utila

import pdfinfo.pages
import rawmaker.cli
import rawmaker.features
import rawmaker.miner.position
import rawmaker.parameter
import rawmaker.reader
import rawmaker.utils


def work(  # pylint:disable=W9015
        document: str,
        boxes_flow: float = 0.5,
        char_margin: float = 2.0,
        line_margin: float = 0.5,
        line_overlap: float = 0.5,
        word_margin: float = 0.1,
        nostrip: bool = rawmaker.parameter.STRIP is False,
        detect_vertical: bool = False,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    """Extract structured text out of document

    Args:
        document: pdf-document to run parsing
        char_margin(float): XXX Why 5.0?
        pages(list): List of processed pages.
    Returns:
        parsed document as yaml output
        parsed positions of text container
    """
    config = rawmaker.parameter.ParsingConfiguration(
        boxes_flow=boxes_flow,
        char_margin=char_margin,
        detect_vertical=detect_vertical,
        line_margin=line_margin,
        line_overlap=line_overlap,
        nostrip=nostrip,
        word_margin=word_margin,
    )

    if rawmaker.cli.superfast():
        result = os.getcwd()
        document = superfast(document, config, result, pages)
    else:
        document = extract_document(document, config, pages)

    positions = rawmaker.miner.position.hash_positions(document, pages=pages)

    dumped_text = serializeraw.dump_document(document)
    dumped_positions = serializeraw.dump_textpositions(positions)

    return dumped_text, dumped_positions


def superfast(
        document: str,
        config: rawmaker.parameter.ParsingConfiguration,
        result: str,
        pages: list = None,
) -> iamraw.Document:
    pagecount = pdfinfo.pages.determine(document)
    if pages is None:
        pages = tuple(range(pagecount))
    chunks = rawmaker.utils.chunks(pages, chunk_size=10)

    parameter = config.cmdline()
    todo = []
    for index, chunk in enumerate(chunks):
        joined_pages = ','.join([str(item) for item in chunk])
        cmd = (f'rawmaker -i {document} -o {result} --prefix {index}'
               f' --text --pages {joined_pages} {parameter}')
        utila.log(cmd)
        todo.append(cmd)

    completed = utila.run_parallel(todo, result, worker=12)
    assert completed == utila.SUCCESS, completed

    document = merge_document(result, len(chunks))
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


def extract_document(
        document: str,
        config: rawmaker.parameter.ParsingConfiguration = None,
        pages: tuple = None,
) -> iamraw.Document:
    strip = rawmaker.parameter.STRIP
    if config:
        strip = config.nostrip is False
        rawmaker.parameter.print_layout(config)

    assert isinstance(document, str), str(document)
    with rawmaker.reader.read(document) as pdf:
        document = rawmaker.features.extract_content(
            pdf,
            config=config,
            strip=strip,
            pages=pages,
        )
    return document


def commandline():
    return utila.Flag(longcut=name(), message='Extract text of document.')


def name():
    return 'text'
