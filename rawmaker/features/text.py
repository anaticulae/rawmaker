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
