# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import pdfminer.layout
import utila

STRIP = True


@dataclasses.dataclass
class ParsingConfiguration:
    boxes_flow: float = 0.5
    char_margin: float = 2.0
    line_margin: float = 0.5
    line_overlap: float = 0.5
    word_margin: float = 0.1
    detect_vertical: bool = False
    nostrip: bool = STRIP is False

    def cmdline(self) -> str:
        """Convert configuration to `linix` command line parameter syntax."""
        parameter = []
        for item, value in vars(self).items():
            if isinstance(value, bool):
                if value:
                    parameter.append(f'--{item}')
            else:
                parameter.append(f'--{item}={value}')
        return ' '.join(parameter)

    def laparams(self) -> pdfminer.layout.LAParams:
        result = pdfminer.layout.LAParams(
            boxes_flow=self.boxes_flow,
            char_margin=self.char_margin,
            detect_vertical=self.detect_vertical,
            line_margin=self.line_margin,
            line_overlap=self.line_overlap,
            word_margin=self.word_margin,
        )
        return result


def from_config(config: ParsingConfiguration) -> pdfminer.layout.LAParams:
    boxes_flow: float = 0.5
    char_margin: float = 2.0
    line_margin: float = 0.5
    line_overlap: float = 0.5
    word_margin: float = 0.1

    if config:
        boxes_flow = config.boxes_flow
        char_margin = config.char_margin
        line_margin = config.line_margin
        line_overlap = config.line_overlap
        word_margin = config.word_margin

    result = pdfminer.layout.LAParams(
        boxes_flow=boxes_flow,
        char_margin=char_margin,
        line_margin=line_margin,
        line_overlap=line_overlap,
        word_margin=word_margin,
    )
    return result


def print_layout(layout: ParsingConfiguration = None):
    assert layout, 'missing layout'
    layout = from_config(layout)
    utila.log('   layout:', end=' ', level=utila.Level.INFORMATION)
    information = [
        ('boxes_flow', layout.boxes_flow),
        ('char_margin', layout.char_margin),
        ('line_margin', layout.line_margin),
        ('line_overlap', layout.line_overlap),
        ('word_margin', layout.word_margin),
    ]
    for (text, value) in information:
        utila.log(
            '%s %.2f' % (text, value),
            end=' ',
            level=utila.Level.INFORMATION,
        )
    utila.log(level=utila.Level.INFORMATION)  # newline
