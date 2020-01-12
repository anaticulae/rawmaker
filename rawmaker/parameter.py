# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pdfminer.layout import LAParams
from utila import Level
from utila import log


def create_layout(
        boxes_flow: float = 0.5,
        char_margin: float = 2.0,
        line_margin: float = 0.5,
        line_overlap: float = 0.5,
        word_margin: float = 0.1,
) -> LAParams:
    # char_margin = get(parameter, 'char_margin', default=5.0, min_value=0.1)
    # boxes_flow: 1.0 only the vertical position matters
    result = LAParams(
        boxes_flow=boxes_flow,
        char_margin=char_margin,
        line_margin=line_margin,
        line_overlap=line_overlap,
        word_margin=word_margin,
    )
    return result


def from_config(config: rawmaker.features.ParsingConfiguration):
    result = create_layout(
        boxes_flow=config.boxes_flow,
        char_margin=config.char_margin,
        line_margin=config.line_margin,
        line_overlap=config.line_overlap,
        word_margin=config.word_margin,
    )
    return result


def print_layout(layout: LAParams = None):
    assert layout, 'missing layout'
    log('   layout:', end=' ', level=Level.INFORMATION)
    information = [
        ('boxes_flow', layout.boxes_flow),
        ('char_margin', layout.char_margin),
        ('line_margin', layout.line_margin),
        ('line_overlap', layout.line_overlap),
        ('word_margin', layout.word_margin),
    ]
    for (text, value) in information:
        log('%s %.2f' % (text, value), end=' ', level=Level.INFORMATION)
    log(level=Level.INFORMATION)  # newline
