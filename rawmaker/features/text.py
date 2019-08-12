#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Extract text out of pdf document to gather information"""

from typing import Tuple

from serializeraw import dump_document
from utila import Flag

from rawmaker.features import extract_content
from rawmaker.miner.position import dump_hasher
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

    positions = hash_positions(document)

    dumped_text = dump_document(document)
    dumped_positions = dump_hasher(positions)

    return dumped_text, dumped_positions


def commandline():
    return Flag(longcut=name(), message='Extract text of document.')


def name():
    return 'text'
