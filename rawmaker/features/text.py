#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Extract text out of pdf document to gather information."""

import os
import typing

import iamraw
import serializeraw
import texmex
import utila

import rawmaker.cli
import rawmaker.features
import rawmaker.miner.position
import rawmaker.miner.text
import rawmaker.parameter
import rawmaker.reader
import rawmaker.text.superfast


def work(  # pylint:disable=W9015,W0613
    document: str,
    xhorizontals: str = None,
    boxes_flow: float = 0.5,
    char_margin: float = 2.0,
    line_margin: float = 0.5,
    line_overlap: float = 0.5,
    word_margin: float = 0.1,
    nostrip: bool = not rawmaker.parameter.STRIP,
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
    # TODO: CHANGE BEHAVIOR OF --detect_vertical. Convert to PARAMETER
    # with True as default.
    detect_vertical = True  # TODO: REMOVE?
    config = rawmaker.parameter.ParsingConfiguration.from_dict(**locals())
    if rawmaker.cli.superfast():
        document = rawmaker.text.superfast.superfast(
            document,
            config,
            workdir=os.getcwd(),
            pages=pages,
        )
    else:
        document = extract_document(source=document, config=config, pages=pages)
    document = underline_chars(document, xhorizontals, pages=pages)
    positions = rawmaker.miner.position.hash_positions(document, pages=pages)
    # dump result
    dumped_text = serializeraw.dump_document(document)
    dumped_positions = serializeraw.dump_textpositions(positions)
    return dumped_text, dumped_positions


def extract_document(
    source: str,
    config: rawmaker.parameter.ParsingConfiguration = None,
    converter=None,
    pages: tuple = None,
) -> iamraw.Document:
    if config:
        rawmaker.parameter.print_layout(config)
    if converter is None:
        converter = rawmaker.miner.text.PrecisePDFConverter
    assert isinstance(source, str), str(source)
    with rawmaker.reader.read(source) as pdf:
        document = rawmaker.features.extract_content(
            pdf,
            config=config,
            converter=converter,
            pages=pages,
        )
    return document


def underline_chars(
    document: iamraw.Document,
    underlinex: str = None,
    pages: tuple = None,
):
    # TODO: MARK HORIZONTAL AS TEXT UNDERLINE HORIZONTAL!
    # TODO: SUPPORT PARTIAL UNDERLINES
    # TODO: UPDATE STYLE RANGE AFTER SETTING ONLY SOME CHARS AS UNDERLINED
    # TODO: REPLACE UNDERLINE WITH STYLE(NONE, UNDERLINE, CROSSED, OVERLINED)
    if not utila.exists(underlinex):
        utila.log(f'missing underlines: {underlinex}, skipping char underline')
        return document
    underlinex = serializeraw.load_horizontals(
        underlinex,
        pages=pages,
    )
    for underlines, pagenumber in underlinex:
        current_page = utila.select_page(document.pages, page=pagenumber)
        if not current_page:
            continue
        for underline in underlines:
            for textcontainer in current_page:
                if not underlined(textcontainer.box, underline.box):
                    continue
                # TODO: REMOVE APPEND AFTER SHRINKING TEXTCONTAINER TO
                # SINGLE LINE
                # update chars
                for char in utila.flatten(textcontainer, append=True):
                    char.underline = True
                break
    return document


def underlined(text: utila.Rectangle, horizontal: utila.Rectangle) -> bool:
    # TODO: SUPPORT CROSSED ETC.
    hline_inside = text[1] < horizontal[1] < text[3]
    if not hline_inside:
        return False
    near_bottom = utila.near(
        expected=text[3],
        current=horizontal[1],
        diff=3.0,
    )
    if not near_bottom:
        return False
    # start and end of horizontal and text matches
    leftright = utila.near(text[0], horizontal[0], diff=5.0)
    leftright &= utila.near(text[2], horizontal[2], diff=5.0)
    if not leftright:
        return False
    return True
