# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pdfminer.layout import LAParams
from utila import Level
from utila import logging
from utila import logging_error


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


def print_layout(layout: LAParams = None):
    if layout is None:
        logging_error('Missing layout')
        return
    logging('   layout:', end=' ', level=Level.INFORMATION)
    for (text, value) in [
        ('boxes_flow', layout.boxes_flow),
        ('char_margin', layout.char_margin),
        ('line_margin', layout.line_margin),
        ('line_overlap', layout.line_overlap),
        ('word_margin', layout.word_margin),
    ]:
        logging('%s %.2f' % (text, value), end=' ', level=Level.INFORMATION)
    logging(level=Level.INFORMATION)  # newline
