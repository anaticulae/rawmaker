#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Extract text out of pdf document to gather information"""

import os
from typing import Tuple

import iamraw
import serializeraw
import utila
from serializeraw import dump_document
from serializeraw import dump_textpositions
from serializeraw import load_document
from serializeraw import load_textpositions
from utila import Flag

import pdfinfo.pages
import rawmaker.cli
import rawmaker.features
import rawmaker.utils
from rawmaker.features import extract_content
from rawmaker.miner.position import hash_positions
from rawmaker.parameter import create_layout
from rawmaker.parameter import print_layout
from rawmaker.reader import read


def work(
        document: str,
        boxes_flow: float = 0.5,
        char_margin: float = 2.0,
        line_margin: float = 0.5,
        line_overlap: float = 0.5,
        word_margin: float = 0.1,
        pages: list = None,
) -> Tuple[str, str]:
    """Extract structured text out of document

    Args:
        document: pdf-document to run parsing
        char_margin(float): XXX Why 5.0?
    Returns:
        parsed document as yaml output
        parsed positions of text container
    """
    config = rawmaker.features.ParsingConfiguration(
        boxes_flow=boxes_flow,
        char_margin=char_margin,
        line_margin=line_margin,
        line_overlap=line_overlap,
        word_margin=word_margin,
    )

    if rawmaker.cli.superfast():
        result = os.getcwd()
        document = superfast(document, config, result, pages)
    else:
        document = extract_document(
            document,
            boxes_flow,
            char_margin,
            line_margin,
            line_overlap,
            word_margin,
            pages,
        )

    positions = hash_positions(document, pages=pages)

    dumped_text = dump_document(document)
    dumped_positions = dump_textpositions(positions)

    return dumped_text, dumped_positions


def superfast(
        document: str,
        config: rawmaker.features.ParsingConfiguration,
        result: str,
        pages: list = None,
) -> iamraw.Document:
    pagecount = pdfinfo.pages.determine(document)
    if pages is None:
        pages = tuple(range(pagecount))
    chunks = rawmaker.utils.chunks(pages, chunk_size=10)

    parameter = ' '.join(
        [f'--{item}={value}' for item, value in vars(config).items()])
    todo = []
    for index, chunk in enumerate(chunks):
        joined_pages = ','.join([str(item) for item in chunk])
        cmd = (f'rawmaker -i {document} -o {result} --prefix {index}'
               f' --text --pages {joined_pages} {parameter}')
        utila.log(cmd)
        todo.append(cmd)

    completed = rawmaker.utils.run_parallel(todo, result, worker=12)
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
                item.box = utila.select_page(pos, page.page).content[index]
                index += 1

    document = iamraw.Document(dimension=text[0].dimension)
    for chunk in text:
        for page in chunk:
            # page.content = [item for item in page if item.box]
            document.pages.append(page)  # pylint:disable=E1101
    return document


def extract_document(
        document,
        boxes_flow: float = 0.5,
        char_margin: float = 2.0,
        line_margin: float = 0.5,
        line_overlap: float = 0.5,
        word_margin: float = 0.1,
        pages: list = None,
) -> iamraw.Document:
    layout = create_layout(
        boxes_flow=boxes_flow,
        char_margin=char_margin,
        line_margin=line_margin,
        line_overlap=line_overlap,
        word_margin=word_margin,
    )
    print_layout(layout)
    # Diff between chars which build a word

    assert isinstance(document, str), str(document)
    with read(document) as pdf:
        document = extract_content(pdf, layout_parameter=layout, pages=pages)
    return document


def commandline():
    return Flag(longcut=name(), message='Extract text of document.')


def name():
    return 'text'
